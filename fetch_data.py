import requests, json
from datetime import datetime, timedelta

URL = 'https://munchbakerydev-compass.odoo.com'
DB = 'munchbakerydev-compass-live-15510994'

auth = requests.post(f'{URL}/web/session/authenticate', json={
    'jsonrpc':'2.0','method':'call','id':1,
    'params':{'db':DB,'login':'HASSAN','password':'123bdf4e7b61fd73d3997b6a2155d7a8cf214526'}
})
s = auth.cookies

def q(model, method, args, kwargs):
    return requests.post(f'{URL}/web/dataset/call_kw', json={
        'jsonrpc':'2.0','method':'call','id':1,
        'params':{'model':model,'method':method,'args':args,'kwargs':kwargs}
    }, cookies=s).json().get('result', [])

now = datetime.now()
df = (now - timedelta(days=365)).strftime('%Y-%m-%d')
dt = now.strftime('%Y-%m-%d')
cfgs = q('pos.config','search_read',[[['active','=',True]]],{'fields':['id','name'],'limit':50})
branches = []

for c in cfgs:
    mo = {}; off = 0
    while True:
        orders = q('pos.order','search_read',
            [[['config_id','=',c['id']],['state','in',['done','invoiced']],
              ['date_order','>=',df],['date_order','<=',dt]]],
            {'fields':['date_order','amount_total'],'limit':5000,'offset':off})
        if not orders: break
        for o in orders:
            m = o['date_order'][:7]
            mo[m] = mo.get(m,0) + o['amount_total']
        off += len(orders)
        if len(orders) < 5000: break
    total = sum(mo.values())
    if not total: continue
    branches.append({'name':c['name'],'total':round(total),'monthly':mo,'cogs':round(total*0.225)})

branches.sort(key=lambda x: -x['total'])
json.dump({'updated':now.strftime('%Y-%m-%d %H:%M'),'date_from':df,'date_to':dt,'branches':branches},
    open('data.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'{len(branches)} branches saved')
