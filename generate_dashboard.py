# -*- coding: utf-8 -*-
import json, base64, sys

with open('/mnt/user-data/uploads/logo_small.png','rb') as f:
    LOGO = base64.b64encode(f.read()).decode()

COLORS = ['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#10b981']
DAYS7  = ['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت']
DR     = {'Online Paid':25,'Taker Wallet':20}

def e(s):   # HTML entity encode Arabic
    return ''.join('&#%d;' % ord(c) if ord(c)>127 else c for c in str(s))
def n(v):
    v=float(v or 0)
    return ('%.2fM'%(v/1e6)) if abs(v)>=1e6 else ('%.1fK'%(v/1e3)) if abs(v)>=1e3 else '{:,}'.format(int(round(v)))
def sar(v): return 'SAR '+n(v)
def pct(v): return '%.1f%%'%float(v or 0)
def dtag(v):
    v=float(v or 0)
    arr='&#9650;' if v>=0 else '&#9660;'
    return '<span class="tag %s">%s %.1f%%</span>' % ('tg' if v>=0 else 'tr', arr, abs(v))
def stag(v,c): return '<span class="tag %s">%s</span>'%(c,v)
def dot(i):    return '<span style="display:inline-block;width:10px;height:10px;background:%s;border-radius:2px;margin-left:8px"></span>'%COLORS[i%8]
def kc(lbl,val,sub,clr):
    return '<div class="kc" style="border-top:3px solid %s"><div class="kl">%s</div><div class="kv">%s</div><div class="ks">%s</div></div>'%(clr,lbl,val,sub)

# ── Fetch data from GitHub ─────────────────────────────────────────────────
import urllib.request, json as _j
try:
    with open('data.json','r',encoding='utf-8') as f:
        D = _j.load(f)
    print('Loaded data.json: %d branches' % len(D.get('branches',[])))
except Exception as ex:
    print('data.json load failed:', ex)
    D = {}

B  = D.get('branches',[])
YB = D.get('ytd_branches',[])
PR = D.get('products',[])
HR = D.get('hourly',[0]*24)
DY = D.get('daily',[0]*7)
PT = D.get('payment_totals',{})
DA = D.get('delivery_apps',{})
EX = D.get('expenses',{})

TR   = sum(b['total'] for b in B)
TGP  = sum(b.get('gross_profit_real',b['total']*.77) for b in B)
TXN  = sum(b.get('total_txn',0) for b in B)
ATK  = TR/TXN if TXN else 0
TEX  = sum(ed.get('total',0) for ed in EX.values())
YR   = sum(b['total'] for b in YB)
YGP  = sum(b.get('gross_profit_real',b['total']*.77) for b in YB)
YTX  = sum(b.get('total_txn',0) for b in YB)
DLT  = sum(v.get('total',0) for v in DA.values())
DLC  = sum(round(v.get('total',0)*DR.get(k,25)/100) for k,v in DA.items())
DLN  = DLT-DLC
Bsrt = sorted(B, key=lambda x:-x['total'])

# ── KPIs ──────────────────────────────────────────────────────────────────
KPIS=(
    kc(e('إجمالي الإيرادات'), sar(TR),  '%d %s'%(len(B),e('فروع')), '#2ba9ed')+
    kc(e('إجمالي الأرباح'),   sar(TGP), pct(TGP/TR*100) if TR else '0%', '#22c55e')+
    kc(e('المعاملات'),         n(TXN),   e('طلب'), '#f59e0b')+
    kc(e('متوسط الفاتورة'),    sar(ATK), e('لكل طلب'), '#8b5cf6')+
    kc(e('أفضل فرع'), e(Bsrt[0]['name']) if Bsrt else '-', sar(Bsrt[0]['total']) if Bsrt else '-', '#e92c30')
)
YTDK=(
    kc('YTD '+e('إيرادات'), sar(YR), '%s - %s'%(D.get('ytd_from',''),D.get('ytd_to','')), '#2ba9ed')+
    kc('YTD '+e('أرباح'),   sar(YGP), pct(YGP/YR*100) if YR else '0%', '#22c55e')+
    kc('YTD '+e('معاملات'), n(YTX),  e('طلب'), '#f59e0b')+
    kc('YTD '+e('متوسط'),   sar(YR/YTX if YTX else 0), e('لكل طلب'), '#8b5cf6')
)

# ── Tables ────────────────────────────────────────────────────────────────
def ths(*a): return ''.join('<th>%s</th>'%e(h) for h in a)

BROWS=''.join(
    '<tr><td>%s<strong>%s</strong></td><td class="nm">%s</td><td class="nm">%s</td><td class="nm">%s</td>'
    '<td class="nm" style="color:#22c55e"><strong>%s</strong></td><td><strong>%s</strong></td>'
    '<td class="nm" style="color:#e92c30">%s</td></tr>' %
    (dot(i),e(b['name']),sar(b['total']),n(b.get('total_txn',0)),sar(b.get('avg_ticket',0)),
     sar(b.get('gross_profit_real',0)),pct(b.get('gross_margin_real',0)),sar(b.get('cogs_real',0)))
    for i,b in enumerate(B))

GROWS=''.join(
    '<tr><td>%s<strong>%s</strong></td><td class="nm">%s</td><td>%s</td><td>%s</td>'
    '<td><strong>%s</strong></td><td class="nm">%s</td><td class="nm">%s</td></tr>' %
    (dot(i),e(b['name']),sar(b['total']),dtag(b.get('qoq',0)),
     dtag(b.get('yoy',0)) if b.get('yoy',0) else stag(e('جديد'),'tn'),
     pct(b.get('gross_margin_real',0)),n(b.get('total_txn',0)),sar(b.get('avg_ticket',0)))
    for i,b in enumerate(B))

def get_exp(nm):
    nm=nm.lower()
    for k,ed in EX.items():
        k2=k.lower().split()[0]
        if k2 in nm or nm.split()[0] in k2 if nm.split() else False:
            return ed.get('total',0)
    return 0

PROWS=''.join(
    '<tr><td><strong>%s</strong></td><td class="nm">%s</td><td class="nm" style="color:#e92c30">%s</td>'
    '<td class="nm" style="color:#22c55e">%s</td><td><strong>%s</strong></td>'
    '<td class="nm" style="color:#e92c30">%s</td><td class="nm" style="color:%s"><strong>%s</strong></td></tr>' %
    (e(b['name']),sar(b['total']),sar(b.get('cogs_real',0)),sar(b.get('gross_profit_real',0)),
     pct(b.get('gross_margin_real',0)),sar(get_exp(b['name'])),
     '#22c55e' if b.get('gross_profit_real',0)-get_exp(b['name'])>=0 else '#e92c30',
     sar(b.get('gross_profit_real',0)-get_exp(b['name'])))
    for b in B)

EXPHTML=''
for bn,ed in sorted(EX.items()):
    tot=ed.get('total',0)
    items=ed.get('items',[])[:15]
    if not items: continue
    rows=''.join('<tr><td style="color:#64748b">%s</td><td class="nm">%s</td></tr>'%(e(it.get('account','')),sar(it.get('amount',0))) for it in items)
    EXPHTML+='<div class="card" style="margin-bottom:12px"><div class="st" style="color:#e92c30">%s &mdash; %s: <strong>%s</strong></div><table class="dt"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>'%(e(bn),e('الإجمالي'),sar(tot),e('بند المصروف'),e('المبلغ'),rows)
if not EXPHTML:
    EXPHTML='<div class="card" style="text-align:center;padding:30px;color:#64748b">%s</div>'%e('لا توجد بيانات مصاريف')
# Add expenses warning at top
exp_note = D.get('expenses_note','')
exp_warning = ''
if exp_note:
    exp_warning = '<div class="rec" style="border-right-color:#f59e0b;margin-bottom:12px"><div class="rt">&#9888;&#65039; %s</div><div class="rb">%s</div></div>'%(e('تحذير: بيانات المصاريف'),e(exp_note))
EXPHTML = exp_warning + EXPHTML

# Build delivery rows with 3-tier commission structure
DELROWS = ''
total_rev_del=0; total_comm_del=0; total_net_del=0; total_cnt_del=0
for m, v in sorted(DA.items(), key=lambda x: -x[1].get('total',0)):
    rev  = v.get('total', 0)
    cnt  = v.get('count', 0)
    comm = v.get('commission', 0)
    net  = v.get('net', rev - comm)
    fr   = v.get('fee_rate', 0)
    pfr  = v.get('payment_fee', 2.5)
    dfr  = v.get('delivery_fee_sar', 0)
    eff  = v.get('effective_rate', round(comm/rev*100,1) if rev else 0)
    total_rev_del  += rev
    total_comm_del += comm
    total_net_del  += net
    total_cnt_del  += cnt
    if dfr:
        fee_txt = '%s%%+%s%%+%s' % (fr, pfr, dfr) + e('/') + e('\u0637\u0644\u0628')
    else:
        fee_txt = '%s%%+%s%%' % (fr, pfr)
    eff_tag = '<span class="tag tr">%.1f%%</span>' % eff
    DELROWS += (
        '<tr>'
        '<td><strong>%s</strong></td>'
        '<td class="nm">%s %s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:#64748b;font-size:11px">%s</td>'
        '<td class="nm" style="color:#e92c30">%s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:#22c55e"><strong>%s</strong></td>'
        '</tr>'
    ) % (e(m), n(cnt), e('\u0637\u0644\u0628'), sar(rev), fee_txt, sar(comm), eff_tag, sar(net))
if DELROWS:
    eff_tot = round(total_comm_del/total_rev_del*100,1) if total_rev_del else 0
    DELROWS += (
        '<tr style="background:#f0f9ff;font-weight:700">'
        '<td colspan="2"><strong>%s</strong></td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="font-size:11px;color:#64748b">%.1f%% %s</td>'
        '<td class="nm" style="color:#e92c30">%s</td>'
        '<td class="nm"><span class="tag tr">%.1f%%</span></td>'
        '<td class="nm" style="color:#22c55e">%s</td>'
        '</tr>'
    ) % (e('\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a'), sar(total_rev_del),
         eff_tot, e('\u0641\u0639\u0644\u064a'), sar(total_comm_del), eff_tot, sar(total_net_del))
DLT=total_rev_del; DLC=total_comm_del; DLN=total_net_del

# ── Excel P&L section ───────────────────────────────────────────────────
XL = D.get('excel_pnl', {})
xl_exp = XL.get('expenses', {})
xl_ns  = float(XL.get('net_sales', 0) or 0)
xl_gp  = float(XL.get('gross_profit', 0) or 0)
xl_gm  = float(XL.get('gross_margin', 0) or 0)
xl_op  = float(XL.get('op_expenses', 0) or 0)
xl_net = float(XL.get('net_profit', 0) or 0)
xl_nm  = float(XL.get('net_margin', 0) or 0)

# Per-branch P&L rows
XL_BR = ''
xl_tot = [0]*6  # rev, gp, sal, rent, del, net
for b in B:
    rev  = float(b.get('xl_revenue',     0) or 0)
    gp   = float(b.get('xl_gross_profit',0) or 0)
    gm   = float(b.get('xl_gross_margin',0) or 0)
    sal  = float(b.get('xl_salaries',    0) or 0)
    rnt  = float(b.get('xl_rent',        0) or 0)
    dlf  = float(b.get('xl_delivery_fee',0) or 0)
    opx  = float(b.get('xl_op_expenses', 0) or 0)
    netp = float(b.get('xl_net_profit',  0) or 0)
    netm = float(b.get('xl_net_margin',  0) or 0)
    if not rev: continue
    for i,v2 in enumerate([rev,gp,sal,rnt,dlf,netp]): xl_tot[i]+=v2
    nc = '#22c55e' if netp>=0 else '#e92c30'
    XL_BR += ('<tr><td><strong>%s</strong></td><td class="nm">%s</td><td class="nm" style="color:#22c55e">%s</td><td><strong>%s</strong></td><td class="nm" style="color:#e92c30">%s</td><td class="nm" style="color:#e92c30">%s</td><td class="nm" style="color:#f59e0b">%s</td><td class="nm" style="color:%s"><strong>%s</strong></td><td><span class="tag %s">%s</span></td></tr>') % (
        e(b['name']), sar(rev), sar(gp), pct(gm),
        sar(sal), sar(rnt), sar(dlf), nc, sar(netp),
        'tg' if netp>=0 else 'tr', pct(netm))
if xl_tot[0]:
    nc2='#22c55e' if xl_tot[5]>=0 else '#e92c30'
    xgm=round(xl_tot[1]/xl_tot[0]*100,1)
    xnm=round(xl_tot[5]/xl_tot[0]*100,1)
    XL_BR += ('<tr style="background:#f0f4f9;font-weight:700"><td><strong>%s</strong></td><td class="nm"><strong>%s</strong></td><td class="nm" style="color:#22c55e"><strong>%s</strong></td><td><strong>%s</strong></td><td class="nm" style="color:#e92c30"><strong>%s</strong></td><td class="nm" style="color:#e92c30"><strong>%s</strong></td><td class="nm" style="color:#f59e0b"><strong>%s</strong></td><td class="nm" style="color:%s"><strong>%s</strong></td><td><span class="tag %s">%s</span></td></tr>') % (
        e('\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a'), sar(xl_tot[0]), sar(xl_tot[1]), pct(xgm),
        sar(xl_tot[2]), sar(xl_tot[3]), sar(xl_tot[4]), nc2, sar(xl_tot[5]),
        'tg' if xl_tot[5]>=0 else 'tr', pct(xnm))

# Expense breakdown rows
exp_items = [
    (e('\u0631\u0648\u0627\u062a\u0628'),          xl_exp.get('salaries',0)),
    (e('\u0625\u064a\u062c\u0627\u0631\u0627\u062a'),  xl_exp.get('rent',0)),
    (e('\u0631\u0633\u0648\u0645 \u062a\u0648\u0635\u064a\u0644'), xl_exp.get('delivery_fee',0)),
    (e('\u0631\u0633\u0648\u0645 \u0627\u0645\u062a\u064a\u0627\u0632'), xl_exp.get('royalty_fee',0)),
    (e('\u062a\u0633\u0648\u064a\u0642'),           xl_exp.get('marketing',0)),
    (e('\u0643\u0647\u0631\u0628\u0627\u0621'),    xl_exp.get('electricity',0)),
    (e('\u0625\u0646\u062a\u0631\u0646\u062a + \u0627\u062a\u0635\u0627\u0644\u0627\u062a'),  xl_exp.get('internet',0)),
    (e('\u0623\u062e\u0631\u0649'),                 xl_exp.get('occ',0)),
]
EXP_TABLE = ''.join(
    '<tr><td>%s</td><td class="nm" style="color:#e92c30">%s</td><td class="nm" style="color:#64748b">%s</td></tr>' % (
        lbl, sar(amt), pct(amt/xl_ns*100) if xl_ns else '0%'
    ) for lbl, amt in exp_items if amt
)
EXP_TABLE += '<tr style="background:#f0f4f9;font-weight:700"><td><strong>%s</strong></td><td class="nm" style="color:#e92c30"><strong>%s</strong></td><td class="nm"><strong>%s</strong></td></tr>' % (
    e('\u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0645\u0635\u0627\u0631\u064a\u0641'), sar(xl_op), pct(xl_op/xl_ns*100) if xl_ns else '0%')

# Missing delivery apps warning

missing_apps = D.get('delivery_apps_missing', [])
DEL_MISSING = ''
if missing_apps:
    apps_str = ' &nbsp;|&nbsp; '.join('<strong>%s</strong>' % e(a) for a in missing_apps)
    DEL_MISSING = (
        '<div style="background:#fef2f2;border:1px solid #fca5a5;border-radius:9px;padding:14px;margin-top:12px">'
        '<div style="font-size:13px;font-weight:700;color:#991b1b;margin-bottom:8px">&#128683; %s (%d %s)</div>'
        '<div style="font-size:12px;color:#64748b;line-height:2">%s</div>'
        '<div style="font-size:11px;color:#991b1b;margin-top:8px;font-style:italic">%s</div>'
        '</div>'
    ) % (
        e('تطبيقات غير مسجّلة في Odoo'), len(missing_apps), e('تطبيق'),
        apps_str,
        e('لإضافتها: Odoo POS ← إعدادات ← طرق الدفع ← إضافة كل تطبيق')
    )

# Expense gap analysis
eg = D.get('expenses_gap', {})
jan_ref = D.get('expenses_jan_reference', {})
EXP_GAP = ''
if eg and jan_ref:
    recorded = eg.get('recorded_april', 0)
    jan_total = jan_ref.get('total', 0)
    missing_months = ' | '.join(eg.get('months_not_entered', []))
    jan_rows = ''.join(
        '<tr><td style="font-size:11px;color:#1e293b">%s</td><td class="nm" style="color:#e92c30">%s</td></tr>' % (e(item['account']), sar(item['amount']))
        for item in jan_ref.get('breakdown', [])[:15]
    )
    EXP_GAP = (
        '<div style="background:#fffbeb;border:2px solid #f59e0b;border-radius:10px;margin-bottom:14px;overflow:hidden">'
        '<div style="background:#fef3c7;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
        '<div><div style="font-size:14px;font-weight:700;color:#92400e">&#9888;&#65039; %s</div>'
        '<div style="font-size:11px;color:#78350f;margin-top:3px">%s: %s</div></div>'
        '<div style="display:flex;gap:20px"><div style="text-align:center"><div style="font-size:10px;color:#92400e;font-weight:700">%s</div><div style="font-size:19px;font-weight:700;font-family:monospace;color:#e92c30">%s</div></div>'
        '<div style="text-align:center"><div style="font-size:10px;color:#92400e;font-weight:700">%s</div><div style="font-size:19px;font-weight:700;font-family:monospace;color:#f59e0b">%s</div></div></div>'
        '</div>'
        '<div style="padding:14px"><div style="font-size:11px;font-weight:700;color:#64748b;margin-bottom:10px">%s</div>'
        '<table class="dt" style="font-size:12px"><thead><tr><th>%s</th><th>%s</th></tr></thead>'
        '<tbody>%s</tbody>'
        '<tfoot><tr><td><strong>%s</strong></td><td class="nm"><strong style="color:#e92c30">%s</strong></td></tr></tfoot>'
        '</table></div></div>'
    ) % (
        e('مصاريف أبريل غير مدخلة في Odoo'),
        e('أشهر ناقصة'), e(missing_months),
        e('مسجّل فعلياً أبريل'), sar(recorded),
        e('مرجع يناير 2026'), sar(jan_total),
        e('هيكل مصاريف يناير 2026 (آخر شهر مدخل بالكامل — يشمل دفعة إيجار ربع سنوية)'),
        e('البند'), e('المبلغ'),
        jan_rows,
        e('إجمالي يناير 2026'), sar(jan_total)
    )

# Menu engineering
MENU=''
if PR:
    avg_r=sum(p['revenue'] for p in PR)/len(PR)
    avg_m=sum(p.get('margin_pct',0) for p in PR)/len(PR)
    nm=lambda p:(p['name'].split('/')[-1].strip() or p['name'])[:28]
    stars=sorted([p for p in PR if p['revenue']>=avg_r and p.get('margin_pct',0)>=avg_m],key=lambda x:-x['revenue'])[:8]
    quest=sorted([p for p in PR if p['revenue']<avg_r  and p.get('margin_pct',0)>=avg_m],key=lambda x:-x.get('margin_pct',0))[:8]
    plow =sorted([p for p in PR if p['revenue']>=avg_r and p.get('margin_pct',0)<avg_m], key=lambda x:-x['revenue'])[:8]
    dogs =sorted([p for p in PR if p['revenue']<avg_r  and p.get('margin_pct',0)<avg_m], key=lambda x:x.get('margin_pct',0))[:6]
    def ptbl(items,tc):
        rows=''.join('<tr><td style="font-size:11px;max-width:140px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">%s</td><td class="nm">%s</td><td>%s</td></tr>'%(e(nm(p)),sar(p['revenue']),stag(pct(p.get('margin_pct',0)),tc)) for p in items)
        return '<table class="dt" style="font-size:12px"><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>'%(e('المنتج'),e('الإيرادات'),e('الهامش'),rows)
    def box(ic,ttl,sub,bc,tc,content):
        return '<div class="card" style="border-top:4px solid %s"><div style="background:%s22;border-radius:7px;padding:9px;margin-bottom:11px"><b style="color:%s">%s %s</b><br><small style="color:%s">%s</small></div>%s</div>'%(bc,bc,tc,ic,ttl,tc,sub,content)
    MENU='<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">'+\
        box('&#11088;',e('نجوم'),e('هامش عالٍ + مبيعات عالية'),'#22c55e','#166534',ptbl(stars,'tg'))+\
        box('&#10067;',e('علامات استفهام'),e('هامش عالٍ + مبيعات منخفضة'),'#2ba9ed','#1e40af',ptbl(quest,'tbl'))+\
        box('&#128004;',e('أبقار حلوب'),e('هامش منخفض + مبيعات عالية'),'#f59e0b','#92400e',ptbl(plow,'tn'))+\
        box('&#128021;',e('خسائر'),e('هامش منخفض + مبيعات منخفضة'),'#e92c30','#991b1b',ptbl(dogs,'tr'))+\
        '</div>'
else:
    MENU='<div class="card" style="text-align:center;padding:40px;color:#64748b">%s</div>'%e('لا توجد بيانات')

# Heatmap / timing
mH=max(HR) if max(HR)>0 else 1
mD=max(DY) if max(DY)>0 else 1
HCELLS=''.join('<div class="hcell" style="background:rgba(43,169,237,%.2f)" title="%02d:00 | SAR %s">%s</div>'%(0.06+v/mH*0.84,h,n(v),n(v) if v>mH*.3 else '') for h,v in enumerate(HR))
HLBLS =''.join('<div class="hlbl">%02d</div>'%h for h in range(24))
DCELLS=''.join('<div class="dcell" style="background:rgba(43,169,237,%.2f)"><div class="dcell-lbl">%s</div><div class="dcell-val">%s</div></div>'%(0.08+v/mD*.3,e(DAYS7[d]),n(v)) for d,v in enumerate(DY))
peakH=HR.index(max(HR))

# Payments
paySum=sum(PT.values()) or 1
PAYROWS=''.join('<tr><td>%s</td><td class="nm">%s</td><td class="nm">%s</td></tr>'%(e(m),sar(v),pct(v/paySum*100)) for m,v in sorted(PT.items(),key=lambda x:-x[1]))

# YTD
ytdMap={b['name']:b for b in YB}
YTDROWS=''.join(
    '<tr><td><strong>%s</strong></td><td class="nm">%s</td><td class="nm">%s</td><td class="nm">%s</td>'
    '<td class="nm" style="color:#22c55e">%s</td><td><strong>%s</strong></td></tr>'%(
    e(b['name']),sar(ytdMap.get(b['name'],{}).get('total',0)),
    n(ytdMap.get(b['name'],{}).get('total_txn',0)),sar(ytdMap.get(b['name'],{}).get('avg_ticket',0)),
    sar(ytdMap.get(b['name'],{}).get('gross_profit_real',0)),pct(ytdMap.get(b['name'],{}).get('gross_margin_real',0)))
    for b in B)
VSROWS=''.join(
    '<tr><td><strong>%s</strong></td><td class="nm">%s</td><td class="nm">%s</td><td class="nm" style="color:#2ba9ed">%s</td></tr>'%(
    e(b['name']),sar(b['total']),sar(ytdMap.get(b['name'],{}).get('total',0)),
    pct(b['total']/max(ytdMap.get(b['name'],{}).get('total',b['total']),1)*100))
    for b in B)

# Rankings
maxT=Bsrt[0]['total'] if Bsrt else 1
RANK=''.join(
    '<div class="rrow"><div class="rn">%d</div><div class="rnm">%s</div>'
    '<div class="rbb"><div class="rbf" style="width:%d%%;background:%s"></div></div>'
    '<div class="rv">%s</div>%s<span class="tag %s">%s</span></div>'%(
    i+1,e(b['name']),int(b['total']/maxT*100),COLORS[i%8],sar(b['total']),
    dtag(b.get('qoq',0)),'tg' if b.get('gross_margin_real',0)>=75 else 'tn',pct(b.get('gross_margin_real',0)))
    for i,b in enumerate(Bsrt))

MEDALS=['&#127947;','&#127948;','&#127949;','4.','5.','6.']
TOP3=''.join(
    '<div class="card" style="margin-bottom:8px;border-right:4px solid %s">'
    '<div style="display:flex;justify-content:space-between"><span style="font-weight:700">%s %s</span><span class="tag tg">%s</span></div>'
    '<div style="font-size:11px;color:#64748b;margin-top:5px">%s: %s | %s: %s | %s: %s</div></div>'%(
    COLORS[i%8],MEDALS[i] if i<len(MEDALS) else '',e(b['name']),sar(b['total']),
    e('هامش'),pct(b.get('gross_margin_real',0)),e('طلبات'),n(b.get('total_txn',0)),e('م.فاتورة'),sar(b.get('avg_ticket',0)))
    for i,b in enumerate(Bsrt[:4]))

# JS data (ensure_ascii=True → no Arabic in JS)
CL=json.dumps(COLORS)
BJ=json.dumps(B,  ensure_ascii=True)
YJ=json.dumps(YB, ensure_ascii=True)
HJ=json.dumps(HR)
DJ=json.dumps(DY)
PJ=json.dumps(PT, ensure_ascii=True)

CSS="""*{margin:0;padding:0;box-sizing:border-box}body{font-family:"IBM Plex Sans Arabic",Arial,sans-serif;background:#f5f7fa;color:#1e293b;direction:rtl;font-size:14px}.bar{background:#fff;border-bottom:1px solid #e2e8f0;padding:0 20px;height:60px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;box-shadow:0 1px 3px rgba(0,0,0,.07)}.lw{display:flex;align-items:center;gap:12px}.lw img{height:38px;width:auto;mix-blend-mode:multiply}.t1{font-size:13px;font-weight:700}.t2{font-size:11px;color:#64748b}.badge{font-size:11px;background:#dcfce7;color:#166534;border:1px solid #bbf7d0;padding:3px 12px;border-radius:20px}.upd{font-size:11px;color:#94a3b8;font-family:monospace}.wrap{padding:18px 20px;max-width:1440px;margin:0 auto}.phdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-wrap:wrap;gap:8px}.phdr h2{font-size:17px;font-weight:700}.phdr p{font-size:12px;color:#64748b;margin-top:2px}.per{font-size:11px;color:#2ba9ed;background:#eff8ff;border:1px solid #bae6fd;padding:4px 12px;border-radius:20px;font-weight:600}.kg5{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:18px}.kg4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}.g2{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px}.kc{background:#fff;border-radius:10px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,.06);border:1px solid #e2e8f0}.kl{font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}.kv{font-size:20px;font-weight:700;font-family:monospace;color:#1e293b;line-height:1}.ks{font-size:11px;color:#64748b;margin-top:5px}.tabs{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:4px;display:flex;gap:3px;margin-bottom:18px;overflow-x:auto;flex-wrap:wrap}.tab{padding:8px 14px;background:none;border:none;cursor:pointer;font-size:12px;color:#64748b;border-radius:7px;font-family:inherit;white-space:nowrap;font-weight:500}.tab:hover{background:#f0f4f9}.tab.on{background:#eff8ff;color:#2ba9ed;font-weight:700}.pane{display:none}.card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;margin-bottom:12px}.st{font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px;display:flex;align-items:center;gap:8px}.st::after{content:"";flex:1;height:1px;background:#e2e8f0}.cw{position:relative;width:100%}table.dt{width:100%;border-collapse:collapse;font-size:12px}table.dt th{padding:9px 11px;font-size:10px;font-weight:700;color:#64748b;border-bottom:2px solid #e2e8f0;text-align:right;background:#f0f4f9;white-space:nowrap}table.dt td{padding:9px 11px;border-bottom:1px solid #e2e8f0;vertical-align:middle}table.dt tr:last-child td{border-bottom:none}table.dt tr:hover td{background:#f8fafc}table.dt tfoot td{background:#f0f4f9;font-weight:700;border-top:2px solid #e2e8f0}.tag{display:inline-flex;align-items:center;gap:2px;font-size:10px;padding:2px 6px;border-radius:4px;font-weight:600;font-family:monospace}.tg{background:#dcfce7;color:#166534}.tr{background:#fee2e2;color:#991b1b}.tn{background:#e2e8f0;color:#64748b}.tbl{background:#dbeafe;color:#1e40af}.nm{font-family:monospace}.hmap{display:grid;grid-template-columns:repeat(24,1fr);gap:2px;margin-top:5px}.hcell{height:36px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:9px;color:#1e293b;font-family:monospace;font-weight:600}.hlabel{display:grid;grid-template-columns:repeat(24,1fr);gap:2px;margin-bottom:3px}.hlbl{font-size:9px;color:#94a3b8;text-align:center}.dmap{display:grid;grid-template-columns:repeat(7,1fr);gap:7px;margin-top:7px}.dcell{border-radius:8px;padding:12px 5px;text-align:center;border:1px solid #e2e8f0}.dcell-lbl{font-size:10px;color:#64748b;margin-bottom:5px;font-weight:600}.dcell-val{font-size:13px;font-weight:700;font-family:monospace}.rrow{display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid #e2e8f0}.rrow:last-child{border-bottom:none}.rn{font-size:15px;font-weight:700;font-family:monospace;color:#94a3b8;width:26px;text-align:center;flex-shrink:0}.rnm{min-width:130px;font-size:13px;font-weight:600}.rbb{flex:1;height:9px;background:#e2e8f0;border-radius:5px;overflow:hidden}.rbf{height:100%;border-radius:5px}.rv{font-size:11px;font-family:monospace;min-width:85px;text-align:left;color:#64748b}.del-box{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}.dc{flex:1;min-width:160px;background:#fff;border-radius:9px;padding:14px;border:1px solid #e2e8f0;text-align:center}.dl{font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:7px}.dv{font-size:19px;font-weight:700;font-family:monospace}@media(max-width:860px){.kg5,.kg4{grid-template-columns:1fr 1fr}.g2,.g3{grid-template-columns:1fr}}"""

JS="""var C=CL,B=BJ,YB=YJ,H=HJ,D=DJ,P=PJ,CH={};
function fmt(v){return Math.abs(v)>=1e6?(v/1e6).toFixed(2)+"M":Math.abs(v)>=1e3?(v/1e3).toFixed(1)+"K":Math.round(v).toLocaleString();}
function sw(n){var i,t,p;for(i=0;i<9;i++){t=document.getElementById("t"+i);p=document.getElementById("p"+i);if(t)t.className="tab"+(i===n?" on":"");if(p)p.style.display=(i===n)?"block":"none";}if(n===0)setTimeout(dOv,50);else if(n===1)setTimeout(dGr,50);else if(n===2)setTimeout(dExp,50);else if(n===5)setTimeout(dTm,50);else if(n===6)setTimeout(dPy,50);else if(n===7)setTimeout(dYT,50);}
function mk(id,cfg){var el=document.getElementById(id);if(!el)return;if(CH[id])CH[id].destroy();try{CH[id]=new Chart(el,cfg);}catch(e){console.error(id,e);}}
function dOv(){if(CH.ch_rev)return;mk("ch_rev",{type:"bar",data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.total;}),backgroundColor:C,borderRadius:5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:"#64748b",font:{size:10}},grid:{display:false}},y:{ticks:{color:"#64748b",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.7)"}}}}});mk("ch_pie",{type:"doughnut",data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.total;}),backgroundColor:C,borderWidth:2,borderColor:"#fff"}]},options:{responsive:true,maintainAspectRatio:false,cutout:"62%",plugins:{legend:{display:true,position:"bottom",labels:{color:"#64748b",font:{size:10},boxWidth:10,padding:5}},tooltip:{callbacks:{label:function(c){return c.label+": "+fmt(c.raw);}}}}}});}
function dGr(){if(CH.ch_qoq)return;mk("ch_qoq",{type:"bar",data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.qoq||0;}),backgroundColor:B.map(function(b){return(b.qoq||0)>=0?"rgba(34,197,94,.8)":"rgba(233,44,48,.8)";}),borderRadius:5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:"#64748b",font:{size:10}},grid:{display:false}},y:{ticks:{color:"#64748b",font:{size:10},callback:function(v){return v+"%";}},grid:{color:"rgba(226,232,240,.7)"}}}}});mk("ch_margin",{type:"bar",data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.gross_margin_real||0;}),backgroundColor:B.map(function(b){var r=b.gross_margin_real||0;return r>=75?"rgba(34,197,94,.8)":r>=65?"rgba(245,158,11,.8)":"rgba(233,44,48,.8)";}),borderRadius:5,indexAxis:"y"}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:"#64748b",font:{size:10},callback:function(v){return v+"%";}},min:50,grid:{color:"rgba(226,232,240,.7)"}},y:{ticks:{color:"#64748b",font:{size:10}},grid:{display:false}}}}});}
function dTm(){if(CH.ch_hr)return;mk("ch_hr",{type:"line",data:{labels:Array.from({length:24},function(_,h){return(h<10?"0"+h:h)+":00";}),datasets:[{data:H,borderColor:"#2ba9ed",backgroundColor:"rgba(43,169,237,.1)",borderWidth:2,fill:true,tension:.4,pointRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:"#64748b",font:{size:9}},grid:{color:"rgba(226,232,240,.7)"}},y:{ticks:{color:"#64748b",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.7)"}}}}});}
function dPy(){if(CH.ch_pay)return;var ks=Object.keys(P),vs=ks.map(function(k){return P[k];});mk("ch_pay",{type:"doughnut",data:{labels:ks,datasets:[{data:vs,backgroundColor:C.slice(0,ks.length),borderWidth:2,borderColor:"#fff"}]},options:{responsive:true,maintainAspectRatio:false,cutout:"55%",plugins:{legend:{display:true,position:"right",labels:{color:"#64748b",font:{size:11},boxWidth:12}},tooltip:{callbacks:{label:function(c){var t=vs.reduce(function(a,b){return a+b;},0);return c.label+": "+fmt(c.raw)+" ("+(c.raw/t*100).toFixed(1)+"%)";}}}}}});}
function dExp(){
  if(CH.ch_exp)return;
  var EX=EX_JSON_PLACEHOLDER;
  mk("ch_exp",{type:"bar",data:{labels:EX.map(function(e){return e.label;}),datasets:[{data:EX.map(function(e){return e.amount;}),backgroundColor:["#e92c30","#f59e0b","#2ba9ed","#8b5cf6","#06b6d4","#22c55e","#ec4899","#10b981"],borderRadius:5}]},options:{responsive:true,maintainAspectRatio:false,indexAxis:"y",plugins:{legend:{display:false}},scales:{x:{ticks:{color:"#64748b",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.7)"}},y:{ticks:{color:"#64748b",font:{size:11}},grid:{display:false}}}}});
}
function dYT(){if(CH.ch_ytd)return;var mo={};YB.forEach(function(b){if(b.monthly)Object.keys(b.monthly).forEach(function(k){mo[k]=(mo[k]||0)+b.monthly[k];});});var ks=Object.keys(mo).sort();mk("ch_ytd",{type:"bar",data:{labels:ks,datasets:[{data:ks.map(function(k){return Math.round(mo[k]);}),backgroundColor:"rgba(43,169,237,.7)",borderRadius:5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{color:"#64748b",font:{size:10}},grid:{display:false}},y:{ticks:{color:"#64748b",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.7)"}}}}});}
dOv();"""

# Replace JS data placeholders
JS=JS.replace('CL',  CL).replace('BJ', BJ).replace('YJ', YJ).replace('HJ', HJ).replace('DJ', DJ).replace('PJ', PJ)

MN=e(D.get('report_month',''))
TTL=e('لوحة التحليل المالي - شركة بوصلة التميز التجارية')

HTML="""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>"""+TTL+"""</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>"""+CSS+"""</style>
</head>
<body>
<div class="bar">
  <div class="lw">
    <img src="data:image/jpeg;base64,"""+LOGO+"""" alt="" onerror="this.style.display='none'">
    <div>
      <div class="t1">"""+TTL+"""</div>
      <div class="t2">"""+e('تقرير شهر')+' '+MN+' | '+str(len(B))+' '+e('فروع')+' | Odoo POS'+"""</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px">
    <div class="badge">&#128197; """+MN+"""</div>
    <div class="upd">"""+e('تحديث:')+' '+D.get('updated','')+"""</div>
  </div>
</div>
<div class="wrap">
<div class="phdr">
  <div><h2>"""+e('التحليل المالي الشهري')+' &mdash; '+MN+"""</h2>
  <p>"""+str(len(B))+' '+e('فروع')+' | '+D.get('date_from','')+' &mdash; '+D.get('date_to','')+"""</p></div>
  <span class="per">&#128197; """+D.get('date_from','')+' &mdash; '+D.get('date_to','')+"""</span>
</div>
<div class="kg5">"""+KPIS+"""</div>
<div class="tabs">
  <button id="t0" class="tab on" onclick="sw(0)">&#128202; """+e('النظرة العامة')+"""</button>
  <button id="t1" class="tab" onclick="sw(1)">&#128200; """+e('الأداء والنمو')+"""</button>
  <button id="t2" class="tab" onclick="sw(2)">&#128176; """+e('الربحية والمصاريف')+"""</button>
  <button id="t3" class="tab" onclick="sw(3)">&#128661; """+e('تطبيقات التوصيل')+"""</button>
  <button id="t4" class="tab" onclick="sw(4)">&#129409; """+e('هندسة القائمة')+"""</button>
  <button id="t5" class="tab" onclick="sw(5)">&#8987; """+e('التوقيت')+"""</button>
  <button id="t6" class="tab" onclick="sw(6)">&#128179; """+e('طرق الدفع')+"""</button>
  <button id="t7" class="tab" onclick="sw(7)">&#128197; YTD</button>
  <button id="t8" class="tab" onclick="sw(8)">&#127942; """+e('التقرير النهائي')+"""</button>
</div>
<div id="p0" style="display:block">
  <div class="st">"""+e('ملخص أداء الفروع')+' &mdash; '+MN+"""</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
  <thead><tr>"""+ths('الفرع','الإيرادات','المعاملات','م.الفاتورة','إجمالي الربح','هامش%','تكلفة البضاعة')+"""</tr></thead>
  <tbody>"""+BROWS+"""</tbody>
  <tfoot><tr><td><strong>"""+e('الإجمالي')+"""</strong></td><td class="nm"><strong>"""+sar(TR)+"""</strong></td><td class="nm"><strong>"""+n(TXN)+"""</strong></td><td class="nm"><strong>"""+sar(ATK)+"""</strong></td><td class="nm" style="color:#22c55e"><strong>"""+sar(TGP)+"""</strong></td><td><strong>"""+pct(TGP/TR*100 if TR else 0)+"""</strong></td><td></td></tr></tfoot>
  </table></div>
  <div class="g2">
    <div class="card"><div class="st">"""+e('مقارنة الإيرادات')+"""</div><div class="cw"><canvas id="ch_rev" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">"""+e('توزيع الإيرادات')+"""</div><div class="cw"><canvas id="ch_pie" style="height:260px"></canvas></div></div>
  </div>
</div>
<div id="p1" style="display:none">
  <div class="st">"""+e('الأداء والنمو')+' &mdash; '+MN+"""</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
  <thead><tr>"""+ths('الفرع','الإيرادات','QoQ','YoY','هامش%','المعاملات','م.الفاتورة')+"""</tr></thead>
  <tbody>"""+GROWS+"""</tbody></table></div>
  <div class="g2">
    <div class="card"><div class="st">"""+e('نمو QoQ')+"""</div><div class="cw"><canvas id="ch_qoq" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">"""+e('الهامش الحقيقي')+"""</div><div class="cw"><canvas id="ch_margin" style="height:260px"></canvas></div></div>
  </div>
</div>
<div id="p2" style="display:none">
  <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:9px;padding:11px 14px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
    <div><strong style="color:#92400e">&#128196; &#1576;&#1610;&#1575;&#1606;&#1575;&#1578; &#1605;&#1575;&#1604;&#1610;&#1577; &#1605;&#1606; &#1605;&#1604;&#1601; &#1573;&#1603;&#1587;&#1604; (&#1605;&#1572;&#1602;&#1578;)</strong><div style="font-size:11px;color:#78350f;margin-top:3px">&#1575;&#1604;&#1571;&#1585;&#1602;&#1575;&#1605; &#1576;&#1583;&#1608;&#1606; &#1590;&#1585;&#1610;&#1576;&#1577; &#1575;&#1604;&#1602;&#1610;&#1605;&#1577; &#1575;&#1604;&#1605;&#1590;&#1575;&#1601;&#1577; 15% &#8212; &#1575;&#1604;&#1588;&#1607;&#1585; &#1575;&#1604;&#1602;&#1575;&#1583;&#1605; &#1578;&#1615;&#1587;&#1581;&#1576; &#1605;&#1606; Odoo &#1578;&#1604;&#1602;&#1575;&#1574;&#1610;&#1575;&#1611;</div></div>
    <span class="badge">&#128197; &#1571;&#1576;&#1585;&#1610;&#1604; 2026</span>
  </div>
  <div class="g3">
    <div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">&#1589;&#1575;&#1601;&#1610; &#1575;&#1604;&#1573;&#1610;&#1585;&#1575;&#1583;&#1575;&#1578; (&#1576;&#1583;&#1608;&#1606; VAT)</div><div class="kv">"""+sar(xl_ns)+"""</div></div>
    <div class="kc" style="border-top:3px solid #22c55e"><div class="kl">&#1573;&#1580;&#1605;&#1575;&#1604;&#1610; &#1575;&#1604;&#1585;&#1576;&#1581; &#1575;&#1604;&#1582;&#1575;&#1605;</div><div class="kv" style="color:#22c55e">"""+sar(xl_gp)+"""</div><div class="ks">"""+pct(xl_gm)+"""</div></div>
    <div class="kc" style="border-top:3px solid " + ("#2ba9ed" if xl_net>=0 else "#e92c30") + ""><div class="kl">&#1589;&#1575;&#1601;&#1610; &#1575;&#1604;&#1585;&#1576;&#1581; &#1576;&#1593;&#1583; &#1575;&#1604;&#1605;&#1589;&#1575;&#1585;&#1610;&#1601;</div><div class="kv" style="color:""" + ("#22c55e" if True else "#e92c30") + """">"""+sar(xl_net)+"""</div><div class="ks">"""+pct(xl_nm)+"""</div></div>
  </div>
  <div class="st">P&L &#1578;&#1601;&#1589;&#1610;&#1604;&#1610; &#1604;&#1603;&#1604; &#1601;&#1585;&#1593;</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
  <thead><tr>"""+ths('&#1575;&#1604;&#1601;&#1585;&#1593;','&#1575;&#1604;&#1573;&#1610;&#1585;&#1575;&#1583;&#1575;&#1578;','&#1573;&#1580;&#1605;&#1575;&#1604;&#1610; &#1575;&#1604;&#1585;&#1576;&#1581;','&#1607;&#1575;&#1605;&#1588;%','&#1575;&#1604;&#1585;&#1608;&#1575;&#1578;&#1576;','&#1575;&#1604;&#1573;&#1610;&#1580;&#1575;&#1585;','&#1585;&#1587;&#1608;&#1605; &#1575;&#1604;&#1578;&#1608;&#1589;&#1610;&#1604;','&#1589;&#1575;&#1601;&#1610; &#1575;&#1604;&#1585;&#1576;&#1581;','&#1607;&#1575;&#1605;&#1588; &#1589;&#1575;&#1601;&#1610;')+"""</tr></thead>
  <tbody>"""+XL_BR+"""</tbody></table></div>
  <div class="st">&#1578;&#1601;&#1589;&#1610;&#1604; &#1575;&#1604;&#1605;&#1589;&#1575;&#1585;&#1610;&#1601; &#1575;&#1604;&#1578;&#1588;&#1594;&#1610;&#1604;&#1610;&#1577;</div>
  <div class="g2">
    <div class="card"><div class="st">&#1578;&#1608;&#1586;&#1610;&#1593; &#1575;&#1604;&#1605;&#1589;&#1575;&#1585;&#1610;&#1601;</div><div class="cw"><canvas id="ch_exp" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">&#1580;&#1583;&#1608;&#1604; &#1575;&#1604;&#1605;&#1589;&#1575;&#1585;&#1610;&#1601;</div>
      <table class="dt"><thead><tr>"""+ths('&#1575;&#1604;&#1576;&#1606;&#1583;','&#1575;&#1604;&#1605;&#1576;&#1604;&#1594;','% &#1605;&#1606; &#1575;&#1604;&#1573;&#1610;&#1585;&#1575;&#1583;&#1575;&#1578;')+"""</tr></thead>
      <tbody>"""+EXP_TABLE+"""</tbody></table>
    </div>
  </div>
</div>
<div id="p3" style="display:none">
  <div class="del-box">
    <div class="dc"><div class="dl">"""+e('دخل التوصيل')+"""</div><div class="dv" style="color:#2ba9ed">"""+sar(DLT)+"""</div></div>
    <div class="dc"><div class="dl">"""+e('العمولات')+"""</div><div class="dv" style="color:#e92c30">"""+sar(DLC)+"""</div></div>
    <div class="dc"><div class="dl">"""+e('مستحق لك')+"""</div><div class="dv" style="color:#22c55e">"""+sar(DLN)+"""</div></div>
    <div class="dc"><div class="dl">"""+e('عدد الطلبات')+"""</div><div class="dv">"""+n(sum(v.get('count',0) for v in DA.values()))+"""</div></div>
  </div>
  <div class="card" style="overflow-x:auto"><table class="dt">
  <thead><tr>"""+ths('التطبيق','عدد الطلبات','إجمالي الدخل','هيكل الرسوم','إجمالي الرسوم','نسبة فعلية','الصافي لك')+"""</tr></thead>
  <tbody>"""+DELROWS+"""</tbody></table></div>
"""+DEL_MISSING+"""
</div>
<div id="p4" style="display:none">
  <div class="st">"""+e('مصفوفة هندسة القائمة')+"""</div>"""+MENU+"""
</div>
<div id="p5" style="display:none">
  <div class="card"><div class="st">"""+e('خريطة حرارة ساعية')+"""</div>
    <div class="hlabel">"""+HLBLS+"""</div><div class="hmap">"""+HCELLS+"""</div>
    <div style="margin-top:8px;font-size:11px;color:#64748b">&#128313; """+e('أعلى ساعة:')+' <strong style="color:#2ba9ed">'+('%02d:00'%peakH)+'</strong> &mdash; '+sar(max(HR))+"""</div>
  </div>
  <div class="g2">
    <div class="card"><div class="st">"""+e('أداء أيام الأسبوع')+"""</div><div class="dmap">"""+DCELLS+"""</div></div>
    <div class="card"><div class="st">"""+e('التوزيع الساعي')+"""</div><div class="cw"><canvas id="ch_hr" style="height:230px"></canvas></div></div>
  </div>
</div>
<div id="p6" style="display:none">
  <div class="g2">
    <div class="card"><div class="st">"""+e('توزيع طرق الدفع')+"""</div><div class="cw"><canvas id="ch_pay" style="height:280px"></canvas></div></div>
    <div class="card"><div class="st">"""+e('مبالغ طرق الدفع')+"""</div>
      <table class="dt"><thead><tr>"""+ths('طريقة الدفع','المبلغ','النسبة')+"""</tr></thead><tbody>"""+PAYROWS+"""</tbody>
      <tfoot><tr><td><strong>"""+e('الإجمالي')+"""</strong></td><td class="nm"><strong>"""+sar(paySum)+"""</strong></td><td class="nm"><strong>100%</strong></td></tr></tfoot></table>
    </div>
  </div>
</div>
<div id="p7" style="display:none">
  <div class="st">YTD &mdash; """+e('من')+' '+D.get('ytd_from','')+' '+e('إلى')+' '+D.get('ytd_to','')+"""</div>
  <div class="kg4">"""+YTDK+"""</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
  <thead><tr>"""+ths('الفرع','YTD إيرادات','المعاملات','م.الفاتورة','إجمالي الربح','هامش%')+"""</tr></thead>
  <tbody>"""+YTDROWS+"""</tbody>
  <tfoot><tr><td><strong>"""+e('الإجمالي')+"""</strong></td><td class="nm"><strong>"""+sar(YR)+"""</strong></td><td class="nm"><strong>"""+n(YTX)+"""</strong></td><td class="nm"><strong>"""+sar(YR/YTX if YTX else 0)+"""</strong></td><td class="nm" style="color:#22c55e"><strong>"""+sar(YGP)+"""</strong></td><td><strong>"""+pct(YGP/YR*100 if YR else 0)+"""</strong></td></tr></tfoot>
  </table></div>
  <div class="g2">
    <div class="card"><div class="st">YTD """+e('تطور الإيرادات')+"""</div><div class="cw"><canvas id="ch_ytd" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">"""+e('شهري vs YTD')+"""</div>
      <table class="dt"><thead><tr>"""+ths('الفرع','الشهر','YTD','نسبة')+"""</tr></thead><tbody>"""+VSROWS+"""</tbody></table>
    </div>
  </div>
</div>
<div id="p8" style="display:none">
  <div class="g2">
    <div><div class="st">&#127942; """+e('التصنيف')+"""</div><div class="card">"""+RANK+"""</div></div>
    <div>
      <div class="st">&#129351; """+e('أعلى الفروع')+"""</div>"""+TOP3+"""
      <div class="exec" style="background:#eff8ff;border:1px solid #bae6fd;border-radius:9px;padding:14px;font-size:12px;color:#64748b;line-height:2;margin-top:14px">
        <strong>&#128203; """+e('الملخص التنفيذي')+' &mdash; '+MN+"""</strong><br><br>
        """+e('حققت الشركة إيرادات')+' <strong>'+sar(TR)+'</strong> '+e('عبر')+' '+str(len(B))+' '+e('فروع بإجمالي ربح')+' <strong>'+sar(TGP)+'</strong> '+e('وهامش')+' <strong>'+pct(TGP/TR*100 if TR else 0)+'</strong>.<br>'+e('نُفّذت')+' <strong>'+n(TXN)+'</strong> '+e('معاملة بمتوسط')+' <strong>'+sar(ATK)+'</strong>.<br>'+e('إيرادات YTD:')+' <strong>'+sar(YR)+'</strong> | '+e('صافي التوصيل:')+' <strong>'+sar(DLN)+'</strong> | '+e('مصاريف:')+' <strong>'+sar(TEX)+'</strong>.'+"""
      </div>
    </div>
  </div>
</div>
</div>
<script>"""+JS+"""</script>
</body>
</html>"""

# Verify ASCII
is_ascii = all(ord(c)<128 for c in HTML)
print(f'HTML size: {len(HTML):,} chars')
print(f'100% ASCII: {is_ascii}')
print(f'Has sw(): {"function sw(" in HTML}')
chk0="id=\"p0\" style=\"display:block\"" in HTML
chk1="id=\"p1\" style=\"display:none\"" in HTML
print(f'Tabs count: {HTML.count("onclick=\"sw(")}')

# Final safety: convert any remaining non-ASCII to HTML entities
def ensure_ascii_html(s):
    return ''.join('&#%d;'%ord(c) if ord(c)>127 else c for c in s)
# Build expense chart JSON
EX_CHART = json.dumps([
    {'label': '\u0631\u0648\u0627\u062a\u0628', 'amount': xl_exp.get('salaries',0)},
    {'label': '\u0625\u064a\u062c\u0627\u0631\u0627\u062a', 'amount': xl_exp.get('rent',0)},
    {'label': '\u062a\u0648\u0635\u064a\u0644', 'amount': xl_exp.get('delivery_fee',0)},
    {'label': '\u0627\u0645\u062a\u064a\u0627\u0632', 'amount': xl_exp.get('royalty_fee',0)},
    {'label': '\u062a\u0633\u0648\u064a\u0642', 'amount': xl_exp.get('marketing',0)},
    {'label': '\u0643\u0647\u0631\u0628\u0627\u0621', 'amount': xl_exp.get('electricity',0)},
    {'label': '\u0625\u0646\u062a\u0631\u0646\u062a', 'amount': xl_exp.get('internet',0)},
], ensure_ascii=True)
HTML = HTML.replace('EX_JSON_PLACEHOLDER', EX_CHART)
HTML_ASCII = ensure_ascii_html(HTML)
with open('index.html','w',encoding='ascii') as f:
    f.write(HTML_ASCII)

