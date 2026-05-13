import xmlrpc.client, json
from datetime import datetime, timezone, timedelta
from calendar import monthrange

URL  = 'https://munchbakerydev-compass.odoo.com'
DB   = 'munchbakerydev-compass-live-15510994'
USER = 'HASSAN'
KEY  = '123bdf4e7b61fd73d3997b6a2155d7a8cf214526'

# ── Riyadh timezone (UTC+3) ──────────────────────────────────────────────
RIYADH = timezone(timedelta(hours=3))

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, KEY, {})
if not uid: print('Auth failed'); exit(1)
print(f'Auth OK: uid={uid}')

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def q(model, method, args, kw={}):
    return models.execute_kw(DB, uid, KEY, model, method, args, kw)

# ── Date ranges (Riyadh time) ───────────────────────────────────────────
now  = datetime.now(RIYADH)
pm   = now.month - 1 if now.month > 1 else 12
py   = now.year  if now.month > 1 else now.year - 1
pm_start  = f'{py}-{pm:02d}-01'
pm_end    = f'{py}-{pm:02d}-{monthrange(py,pm)[1]:02d}'
ytd_start = f'{py}-01-01'
ytd_end   = pm_end

MONTHS_AR = ['يناير','فبراير','مارس','أبريل','مايو','يونيو',
             'يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر']
report_month = f'{MONTHS_AR[pm-1]} {py}'
print(f'Riyadh now: {now.strftime("%Y-%m-%d %H:%M")}')
print(f'Report month: {report_month}  |  {pm_start} to {pm_end}  |  YTD: {ytd_start} to {ytd_end}')

# ── Delivery apps config (name → commission %) ──────────────────────────
DELIVERY_APPS = {
    'Online Paid':   25,
    'Taker Wallet':  20,
}

# ── POS Configs ──────────────────────────────────────────────────────────
cfgs = q('pos.config','search_read',[[['active','=',True]]],
         {'fields':['id','name'],'limit':50})
cfg_map = {c['id']: c['name'] for c in cfgs}

analytic_accts = q('account.analytic.account','search_read',
                   [[['active','=',True]]],{'fields':['id','name']})
analytic_map = {str(a['id']): a['name'] for a in (analytic_accts or [])}
print(f'Branches: {list(cfg_map.values())}')

# ── Fetch POS orders for a period ────────────────────────────────────────
def fetch_period_data(df, dt):
    branches = {}
    # Convert Riyadh date boundaries to UTC for Odoo query
    # Odoo stores dates in UTC; Riyadh is UTC+3
    # 2026-04-01 00:00 Riyadh = 2026-03-31 21:00 UTC → use df as-is but offset
    df_utc = (datetime.strptime(df, '%Y-%m-%d').replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    dt_utc = (datetime.strptime(dt + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
              .replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))

    for cid, cname in cfg_map.items():
        monthly_rev = {}; monthly_txn = {}
        hourly = [0]*24; daily = [0]*7
        real_cogs = 0.0; real_margin = 0.0; total_txn = 0
        all_orders = []
        off = 0
        while True:
            orders = q('pos.order','search_read',
                [[['config_id','=',cid],['state','in',['done','invoiced']],
                  ['date_order','>=',df_utc],['date_order','<=',dt_utc]]],
                {'fields':['id','date_order','amount_total'],'limit':5000,'offset':off})
            if not orders: break
            all_orders.extend(orders); off += len(orders)
            if len(orders) < 5000: break

        for o in all_orders:
            # Convert UTC order time to Riyadh (+3h)
            d_utc = datetime.strptime(o['date_order'], '%Y-%m-%d %H:%M:%S')
            d_ryd = d_utc + timedelta(hours=3)
            m     = d_ryd.strftime('%Y-%m')
            monthly_rev[m] = monthly_rev.get(m, 0) + o['amount_total']
            monthly_txn[m] = monthly_txn.get(m, 0) + 1
            hourly[d_ryd.hour]             += o['amount_total']
            daily[d_ryd.weekday()]         += o['amount_total']
            total_txn += 1

        total_rev = sum(monthly_rev.values())
        if not total_rev: continue

        order_ids = [o['id'] for o in all_orders]
        for i in range(0, len(order_ids), 2000):
            lines = q('pos.order.line','search_read',
                [[['order_id','in',order_ids[i:i+2000]]]],
                {'fields':['total_cost','margin'],'limit':10000})
            for l in (lines or []):
                real_cogs   += l.get('total_cost', 0) or 0
                real_margin += l.get('margin',     0) or 0

        branches[cname] = {
            'name': cname,
            'total': round(total_rev),
            'cogs_real': round(real_cogs),
            'gross_profit_real': round(real_margin),
            'gross_margin_real': round(real_margin/total_rev*100, 1) if total_rev else 0,
            'total_txn': total_txn,
            'avg_ticket': round(total_rev/total_txn, 1) if total_txn else 0,
            'monthly': dict(monthly_rev),
            'monthly_txn': dict(monthly_txn),
            'hourly': [round(v) for v in hourly],
            'daily':  [round(v) for v in daily],
        }
    return sorted(branches.values(), key=lambda x: -x['total'])

# ── Payment totals ────────────────────────────────────────────────────────
def fetch_payments(df, dt):
    df_utc = (datetime.strptime(df, '%Y-%m-%d').replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    dt_utc = (datetime.strptime(dt + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
              .replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    pays = []; off = 0
    while True:
        b = q('pos.payment','search_read',
              [[['session_id.stop_at','>=',df_utc],
                ['session_id.stop_at','<=',dt_utc]]],
              {'fields':['payment_method_id','amount'],'limit':5000,'offset':off})
        if not b: break
        pays.extend(b); off += len(b)
        if len(b) < 5000: break
    totals = {}
    for p in pays:
        m = (p['payment_method_id'][1] if isinstance(p['payment_method_id'], list)
             else str(p['payment_method_id']))
        totals[m] = totals.get(m, 0) + p['amount']
    return {k: round(v) for k, v in sorted(totals.items(), key=lambda x: -x[1])}

# ── Delivery apps — each separately ──────────────────────────────────────
def fetch_delivery(df, dt):
    df_utc = (datetime.strptime(df, '%Y-%m-%d').replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    dt_utc = (datetime.strptime(dt + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
              .replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    result = {}
    for app_name, commission_pct in DELIVERY_APPS.items():
        ms = q('pos.payment.method','search_read',
               [[['name','=',app_name]]],{'fields':['id'],'limit':1})
        if not ms:
            result[app_name] = {'total':0,'count':0,'commission_pct':commission_pct,
                                'commission':0,'net':0}
            continue
        mid = ms[0]['id']
        ps  = q('pos.payment','search_read',
                [[['payment_method_id','=',mid],
                  ['session_id.stop_at','>=',df_utc],
                  ['session_id.stop_at','<=',dt_utc]]],
                {'fields':['amount'],'limit':10000})
        total      = round(sum(p['amount'] for p in (ps or [])))
        cnt        = len(ps or [])
        commission = round(total * commission_pct / 100)
        net        = total - commission
        result[app_name] = {
            'total': total,
            'count': cnt,
            'commission_pct': commission_pct,
            'commission': commission,
            'net': net,
        }
    return result

# ── Expenses ─────────────────────────────────────────────────────────────
def fetch_expenses(df, dt):
    lines = []; off = 0
    while True:
        b = q('account.move.line','search_read',
              [[['account_id.account_type','=','expense'],
                ['move_id.state','=','posted'],
                ['date','>=',df],['date','<=',dt],['debit','>',0]]],
              {'fields':['account_id','debit','analytic_distribution','name'],
               'limit':5000,'offset':off})
        if not b: break
        lines.extend(b); off += len(b)
        if len(b) < 5000: break

    branch_exp = {}
    for l in lines:
        dist     = l.get('analytic_distribution') or {}
        acc_name = (l['account_id'][1] if isinstance(l['account_id'], list)
                    else str(l['account_id']))
        amt      = l.get('debit', 0) or 0
        if not dist:
            bn = 'عام'
            branch_exp.setdefault(bn, {})[acc_name] = branch_exp[bn].get(acc_name, 0) + amt
        else:
            for aid, pct in dist.items():
                bn    = analytic_map.get(str(aid), f'ID_{aid}')
                alloc = amt * (pct / 100.0)
                branch_exp.setdefault(bn, {})[acc_name] = branch_exp[bn].get(acc_name, 0) + alloc

    result = {}
    for bn, accs in branch_exp.items():
        items = sorted([{'account': k, 'amount': round(v, 2)} for k, v in accs.items()],
                       key=lambda x: -x['amount'])
        total = round(sum(accs.values()), 2)
        if total > 0:
            result[bn] = {'items': items, 'total': total}
    return result

# ── Products ─────────────────────────────────────────────────────────────
def fetch_products(df, dt):
    df_utc = (datetime.strptime(df, '%Y-%m-%d').replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    dt_utc = (datetime.strptime(dt + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
              .replace(tzinfo=RIYADH)
              .astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
    orders = q('pos.order','search_read',
               [[['state','in',['done','invoiced']],
                 ['date_order','>=',df_utc],['date_order','<=',dt_utc]]],
               {'fields':['id'],'limit':50000})
    if not orders: return []
    order_ids = [o['id'] for o in orders]
    prod_map  = {}
    for i in range(0, len(order_ids), 2000):
        lines = q('pos.order.line','search_read',
                  [[['order_id','in',order_ids[i:i+2000]]]],
                  {'fields':['full_product_name','qty','price_subtotal_incl','margin','total_cost'],
                   'limit':10000})
        for l in (lines or []):
            name = (l.get('full_product_name') or '').strip()
            if not name: continue
            p = prod_map.setdefault(name, {'revenue':0,'qty':0,'margin':0})
            p['revenue'] += l.get('price_subtotal_incl', 0) or 0
            p['qty']     += l.get('qty', 0) or 0
            p['margin']  += l.get('margin', 0) or 0
    products = []
    for name, d in prod_map.items():
        if d['revenue'] < 100: continue
        products.append({
            'name': name,
            'revenue': round(d['revenue']),
            'qty': round(d['qty']),
            'margin': round(d['margin']),
            'margin_pct': round(d['margin']/d['revenue']*100, 1) if d['revenue'] else 0,
        })
    return sorted(products, key=lambda x: -x['revenue'])[:80]

# ── Execute ───────────────────────────────────────────────────────────────
print('Fetching monthly data...')
monthly_b = fetch_period_data(pm_start, pm_end)
print(f'Monthly branches: {len(monthly_b)}')

print('Fetching YTD data...')
ytd_b = fetch_period_data(ytd_start, ytd_end)
print(f'YTD branches: {len(ytd_b)}')

print('Fetching payments...')
pay_totals = fetch_payments(pm_start, pm_end)

print('Fetching delivery apps...')
delivery     = fetch_delivery(pm_start, pm_end)
delivery_ytd = fetch_delivery(ytd_start, ytd_end)
print(f'Delivery apps: { {k:v["total"] for k,v in delivery.items()} }')

print('Fetching expenses...')
expenses     = fetch_expenses(pm_start, pm_end)
expenses_ytd = fetch_expenses(ytd_start, ytd_end)
exp_total    = sum(e['total'] for e in expenses.values())
print(f'Expenses (Odoo recorded): {exp_total:,.0f} SAR')

print('Fetching products...')
products = fetch_products(pm_start, pm_end)

# Aggregate hourly/daily (already Riyadh-adjusted inside fetch_period_data)
agg_h = [0]*24; agg_d = [0]*7
for b in monthly_b:
    for i in range(24): agg_h[i] += b['hourly'][i]
    for i in range(7):  agg_d[i] += b['daily'][i]

# Fetch POS returns
pos_ret = q('pos.order','search_read',
    [[['state','in',['done','invoiced']],['amount_total','<',0],
      ['date_order','>=',pm_start],['date_order','<=',pm_end+' 23:59:59']]],
    {'fields':['amount_total'],'limit':1000})
ret_total = round(sum(r['amount_total'] for r in pos_ret))
print(f'POS Returns: {len(pos_ret)} orders, total={ret_total}')

# Fixed list of delivery apps NOT in Odoo
DELIVERY_APPS_MISSING = [
    'HungerStation (\u0647\u0646\u0642\u0631\u0633\u062a\u064a\u0634\u0646)',
    'Ninja (\u0646\u064a\u0646\u062c\u0627)',
    'Keeta (\u0643\u064a\u062a\u0627)',
    'Jahez (\u062c\u0627\u0647\u0632)',
    'Marsool (\u0645\u0631\u0633\u0648\u0644)',
    'Careem Food (\u0643\u0631\u064a\u0645 \u0641\u0648\u062f)',
    'Toters (\u062a\u0648\u062a\u0631\u0632)',
    'Wssel (\u0648\u0635\u0644)',
    'Snoonu (\u0633\u0646\u0648\u0646\u0648)'
]

data = {
    'report_month':  report_month,
    'updated':       now.strftime('%Y-%m-%d %H:%M') + ' (توقيت الرياض)',
    'date_from':     pm_start,
    'date_to':       pm_end,
    'ytd_from':      ytd_start,
    'ytd_to':        ytd_end,
    'branches':      monthly_b,
    'ytd_branches':  ytd_b,
    'products':      products,
    'payment_totals':  pay_totals,
    'delivery_apps':   delivery,
    'delivery_ytd':    delivery_ytd,
    'expenses':        expenses,
    'expenses_ytd':    expenses_ytd,
    'expenses_note':   '\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0645\u0635\u0627\u0631\u064a\u0641 \u0627\u0644\u0645\u0633\u062c\u0644\u0629 \u0641\u064a Odoo \u0642\u062f \u0644\u0627 \u062a\u0639\u0643\u0633 \u0627\u0644\u0645\u0635\u0627\u0631\u064a\u0641 \u0627\u0644\u0641\u0639\u0644\u064a\u0629.',
    'delivery_apps_missing': DELIVERY_APPS_MISSING,
    'pos_returns':     {'count': len(pos_ret), 'total': ret_total},
    'expenses_note':   'تنبيه: بيانات المصاريف المسجلة في النظام قد لا تعكس المصاريف الفعلية الكاملة.',
    'hourly': [round(v) for v in agg_h],
    'daily':  [round(v) for v in agg_d],
}
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2, default=str)

total_rev = sum(b['total'] for b in monthly_b)
print(f'DONE | {report_month} | {len(monthly_b)} branches | revenue={total_rev:,.0f} | products={len(products)}')
