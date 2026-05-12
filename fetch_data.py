import xmlrpc.client, json
from datetime import datetime, timedelta
from collections import defaultdict

URL  = 'https://munchbakerydev-compass.odoo.com'
DB   = 'munchbakerydev-compass-live-15510994'
USER = 'HASSAN'
KEY  = '123bdf4e7b61fd73d3997b6a2155d7a8cf214526'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, KEY, {})
if not uid: print('Auth failed'); exit(1)
print(f'Auth OK: uid={uid}')

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def q(model, method, args, kw={}):
    return models.execute_kw(DB, uid, KEY, model, method, args, kw)

now = datetime.now()
df  = (now - timedelta(days=365)).strftime('%Y-%m-%d')
dt  = now.strftime('%Y-%m-%d')
print(f'Period: {df} -> {dt}')

# ── 1. POS Configs (Branches) ───────────────────────────────
cfgs = q('pos.config','search_read',[[['active','=',True]]],{'fields':['id','name'],'limit':50})
cfg_map = {c['id']: c['name'] for c in cfgs}
print(f'Branches: {list(cfg_map.values())}')

# ── 2. Fetch All Orders ────────────────────────────────────
print('Fetching orders...')
all_orders = []
for cid in cfg_map:
    off = 0
    while True:
        batch = q('pos.order','search_read',
            [[['config_id','=',cid],['state','in',['done','invoiced']],
              ['date_order','>=',df],['date_order','<=',dt]]],
            {'fields':['id','config_id','date_order','amount_total','nb_print'],'limit':5000,'offset':off})
        if not batch: break
        all_orders.extend(batch)
        off += len(batch)
        if len(batch) < 5000: break

print(f'Total orders: {len(all_orders)}')

# ── 3. Fetch Order Lines for Real COGS + Products ──────────
print('Fetching order lines...')
order_ids = [o['id'] for o in all_orders]
all_lines = []
batch_size = 2000
for i in range(0, len(order_ids), batch_size):
    batch_ids = order_ids[i:i+batch_size]
    lines = q('pos.order.line','search_read',
        [[['order_id','in',batch_ids]]],
        {'fields':['order_id','full_product_name','qty','price_subtotal_incl',
                   'margin','total_cost','discount'],'limit':10000})
    all_lines.extend(lines or [])
    print(f'  Lines fetched: {len(all_lines)}')

# ── 4. Fetch Payment Methods ───────────────────────────────
print('Fetching payments...')
all_payments = []
off = 0
while True:
    batch = q('pos.payment','search_read',
        [[['session_id.stop_at','>=',df]]],
        {'fields':['session_id','payment_method_id','amount'],'limit':5000,'offset':off})
    if not batch: break
    all_payments.extend(batch)
    off += len(batch)
    if len(batch) < 5000: break
print(f'Payments: {len(all_payments)}')

# ── 5. Map orders to config ────────────────────────────────
order_cfg = {o['id']: o['config_id'][0] for o in all_orders}
order_date = {o['id']: o['date_order'] for o in all_orders}

# ── 6. Build Branch Data ───────────────────────────────────
now_y = now
branches_data = {}
for cid, cname in cfg_map.items():
    monthly_rev = defaultdict(float)
    monthly_txn = defaultdict(int)
    hourly = defaultdict(float)
    daily  = defaultdict(float)
    real_cogs = 0.0
    real_margin = 0.0
    total_txn = 0
    discount_count = 0

    for o in all_orders:
        if o['config_id'][0] != cid: continue
        d = datetime.strptime(o['date_order'], '%Y-%m-%d %H:%M:%S')
        m = o['date_order'][:7]
        monthly_rev[m] += o['amount_total']
        monthly_txn[m] += 1
        hourly[d.hour] += o['amount_total']
        daily[d.weekday()] += o['amount_total']
        total_txn += 1

    for l in all_lines:
        oid = l['order_id'][0] if isinstance(l['order_id'], list) else l['order_id']
        if order_cfg.get(oid) != cid: continue
        real_cogs   += l.get('total_cost', 0) or 0
        real_margin += l.get('margin', 0) or 0
        if (l.get('discount') or 0) > 0: discount_count += 1

    total_rev = sum(monthly_rev.values())
    if total_rev == 0: continue

    # QoQ
    vals = [monthly_rev.get(m, 0) for m in sorted(monthly_rev)]
    q3r  = sum(vals[-6:-3]) if len(vals)>=6 else 0
    q4r  = sum(vals[-3:])   if len(vals)>=3 else 0
    q1r  = sum(vals[:3])    if len(vals)>=3 else 0
    qoq  = round((q4r-q3r)/q3r*100,1) if q3r else 0
    yoy  = round((q4r-q1r)/q1r*100,1) if q1r else 0

    branches_data[cname] = {
        'name': cname,
        'total': round(total_rev),
        'cogs_real': round(real_cogs),
        'gross_profit_real': round(real_margin),
        'gross_margin_real': round(real_margin/total_rev*100,1) if total_rev else 0,
        'total_txn': total_txn,
        'avg_ticket': round(total_rev/total_txn,1) if total_txn else 0,
        'discount_rate': round(discount_count/len([l for l in all_lines if order_cfg.get(l['order_id'][0] if isinstance(l['order_id'],list) else l['order_id'])==cid])*100,1) if all_lines else 0,
        'monthly': dict(monthly_rev),
        'monthly_txn': dict(monthly_txn),
        'hourly': [round(hourly.get(h,0)) for h in range(24)],
        'daily': [round(daily.get(d,0)) for d in range(7)],
        'qoq': qoq, 'yoy': yoy,
    }

# ── 7. Payment Methods per Branch ─────────────────────────
print('Building payment data...')
sessions_cfg = {}
sessions = q('pos.session','search_read',[[['stop_at','>=',df]]],
    {'fields':['id','config_id'],'limit':5000})
for s in (sessions or []):
    sessions_cfg[s['id']] = s['config_id'][0]

pay_by_branch = defaultdict(lambda: defaultdict(float))
pay_totals = defaultdict(float)
for p in all_payments:
    sid = p['session_id'][0] if isinstance(p['session_id'],list) else p['session_id']
    cid = sessions_cfg.get(sid)
    cname = cfg_map.get(cid,'Unknown')
    method = p['payment_method_id'][1] if isinstance(p['payment_method_id'],list) else str(p['payment_method_id'])
    pay_by_branch[cname][method] += p['amount']
    pay_totals[method] += p['amount']

for cname in branches_data:
    branches_data[cname]['payments'] = {k: round(v) for k,v in pay_by_branch.get(cname,{}).items()}

# ── 8. Product Menu Engineering ────────────────────────────
print('Building product data...')
prod_map = defaultdict(lambda:{'revenue':0,'qty':0,'margin':0,'cost':0,'orders':0})
for l in all_lines:
    name = (l.get('full_product_name') or 'Unknown').strip()
    prod_map[name]['revenue'] += l.get('price_subtotal_incl',0) or 0
    prod_map[name]['qty']     += l.get('qty',0) or 0
    prod_map[name]['margin']  += l.get('margin',0) or 0
    prod_map[name]['cost']    += l.get('total_cost',0) or 0
    prod_map[name]['orders']  += 1

products = []
for name, d in prod_map.items():
    if d['revenue'] < 100: continue
    products.append({
        'name': name,
        'revenue': round(d['revenue']),
        'qty': round(d['qty']),
        'margin': round(d['margin']),
        'margin_pct': round(d['margin']/d['revenue']*100,1) if d['revenue'] else 0,
        'orders': d['orders']
    })
products.sort(key=lambda x: -x['revenue'])

# ── 9. Aggregate Hourly/Daily ──────────────────────────────
agg_hourly = [0]*24
agg_daily  = [0]*7
for b in branches_data.values():
    for h in range(24): agg_hourly[h] += b['hourly'][h]
    for d in range(7):  agg_daily[d]  += b['daily'][d]

# ── 10. Save ───────────────────────────────────────────────
data = {
    'updated': now.strftime('%Y-%m-%d %H:%M'),
    'date_from': df, 'date_to': dt,
    'branches': sorted(branches_data.values(), key=lambda x: -x['total']),
    'products': products[:80],
    'payment_totals': {k: round(v) for k,v in pay_totals.items()},
    'hourly': agg_hourly,
    'daily': agg_daily,
}
with open('data.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
total_rev = sum(b['total'] for b in branches_data.values())
print(f'Done: {len(branches_data)} branches | {len(products)} products | revenue={total_rev:,.0f}')
