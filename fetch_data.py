import xmlrpc.client, json
from datetime import datetime, timedelta

URL = 'https://munchbakerydev-compass.odoo.com'
DB  = 'munchbakerydev-compass-live-15510994'
USER = 'HASSAN'
KEY  = '123bdf4e7b61fd73d3997b6a2155d7a8cf214526'

# Authenticate via XML-RPC
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, KEY, {})
print(f'Auth UID: {uid}')
if not uid:
    print('Auth failed')
    exit(1)

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
call = lambda model, method, args, kw={}: models.execute_kw(DB, uid, KEY, model, method, args, kw)

now = datetime.now()
df = (now - timedelta(days=365)).strftime('%Y-%m-%d')
dt = now.strftime('%Y-%m-%d')
print(f'Fetching data from {df} to {dt}')

cfgs = call('pos.config', 'search_read', [[['active','=',True]]], {'fields':['id','name'],'limit':50})
print(f'Found {len(cfgs)} POS configs: {[c["name"] for c in cfgs]}')

branches = []
for c in cfgs:
    mo = {}; off = 0; total_orders = 0
    while True:
        orders = call('pos.order', 'search_read',
            [[['config_id','=',c['id']],['state','in',['done','invoiced']],
              ['date_order','>=',df],['date_order','<=',dt]]],
            {'fields':['date_order','amount_total'],'limit':5000,'offset':off})
        if not orders: break
        for o in orders:
            m = o['date_order'][:7]
            mo[m] = mo.get(m, 0) + o['amount_total']
        off += len(orders); total_orders += len(orders)
        if len(orders) < 5000: break
    total = sum(mo.values())
    print(f'  {c["name"]}: {total_orders} orders, total={round(total)}')
    if not total: continue
    branches.append({'name':c['name'],'total':round(total),'monthly':mo,'cogs':round(total*0.225)})

branches.sort(key=lambda x: -x['total'])
data = {'updated':now.strftime('%Y-%m-%d %H:%M'),'date_from':df,'date_to':dt,'branches':branches}
with open('data.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'{len(branches)} branches saved successfully')
