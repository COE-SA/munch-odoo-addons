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
def kc(lbl, val, sub, clr):
    return '<div class="kc" style="--accent:%s"><div class="kl">%s</div><div class="kv">%s</div><div class="ks">%s</div></div>' % (clr, lbl, val, sub)

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

XL_PNL = D.get('excel_pnl', {})
XL_EXP = XL_PNL.get('expenses', {})
XL_NS  = float(XL_PNL.get('net_sales',    0) or 0)
XL_GP  = float(XL_PNL.get('gross_profit', 0) or 0)
XL_GM  = float(XL_PNL.get('gross_margin', 0) or 0)
XL_OP  = float(XL_PNL.get('op_expenses',  0) or 0)
XL_NET = float(XL_PNL.get('net_profit',   0) or 0)
XL_NM  = float(XL_PNL.get('net_margin',   0) or 0)
XL_SAL = float(XL_EXP.get('salaries',     0) or 0)
XL_RNT = float(XL_EXP.get('rent',         0) or 0)
XL_DLF = float(XL_EXP.get('delivery_fee', 0) or 0)
_Bxl2  = sorted([b for b in B if b.get('xl_revenue',0)>0], key=lambda x:-x.get('xl_net_profit',0))
_best  = _Bxl2[0] if _Bxl2 else {}

KPIS2 = (
    kc(e('\u0625\u064a\u0631\u0627\u062f\u0627\u062a \u0628\u062f\u0648\u0646 VAT'),
       sar(XL_NS), e('\u0645\u0644\u0641 \u0625\u0643\u0633\u0644'), '#06b6d4') +
    kc(e('\u0627\u0644\u0631\u0648\u0627\u062a\u0628'),
       sar(XL_SAL), pct(XL_SAL/XL_NS*100) if XL_NS else '0%', '#8b5cf6') +
    kc(e('\u0627\u0644\u0625\u064a\u062c\u0627\u0631\u0627\u062a'),
       sar(XL_RNT), pct(XL_RNT/XL_NS*100) if XL_NS else '0%', '#f59e0b') +
    kc(e('\u0631\u0633\u0648\u0645 \u0627\u0644\u062a\u0648\u0635\u064a\u0644'),
       sar(XL_DLF), pct(XL_DLF/XL_NS*100) if XL_NS else '0%', '#ec4899') +
    kc(e('\u0635\u0627\u0641\u064a \u0627\u0644\u0631\u0628\u062d'),
       sar(XL_NET), pct(XL_NM)+(' \u2705' if XL_NET>=0 else ' \u26a0\ufe0f')+' '+e('\u0635\u0627\u0641\u064a'),
       '#22c55e' if XL_NET>=0 else '#e92c30')
)
KPIS=(
    kc(e('\u0625\u064a\u0631\u0627\u062f\u0627\u062a (+VAT)'),
       sar(TR), '%d %s'%(len(B),e('\u0641\u0631\u0648\u0639')), '#2ba9ed')+
    kc(e('\u0631\u0628\u062d \u062e\u0627\u0645 (\u0628\u062f\u0648\u0646 VAT)'),
       sar(XL_GP if XL_GP else TGP), pct(XL_GM if XL_GP else TGP/TR*100 if TR else 0), '#22c55e')+
    kc(e('\u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0645\u0639\u0627\u0645\u0644\u0627\u062a'),
       n(TXN), e('\u0637\u0644\u0628'), '#f59e0b')+
    kc(e('\u0645\u062a\u0648\u0633\u0637 \u0627\u0644\u0641\u0627\u062a\u0648\u0631\u0629'),
       sar(ATK), e('\u0644\u0643\u0644 \u0637\u0644\u0628'), '#8b5cf6')+
    kc(e('\u0623\u0641\u0636\u0644 \u0641\u0631\u0639 (\u0635\u0627\u0641\u064a)'),
       e(_best.get('name','-') if _best else '-'),
       sar(_best.get('xl_net_profit',0) if _best else 0)+' | '+pct(_best.get('xl_net_margin',0) if _best else 0),
       '#22c55e')
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
    ('<tr><td>%s<strong>%s</strong></td><td class="nm">%s</td><td class="nm">%s</td>'
     '<td class="nm">%s</td>'
     '<td class="nm" style="color:#22c55e"><strong>%s</strong></td>'
     '<td><strong>%s</strong></td>'
     '<td class="nm" style="color:#e92c30">%s</td>'
     '<td class="nm" style="color:%s"><strong>%s</strong></td>'
     '<td><span class="tag %s">%s</span></td></tr>') % (
        dot(i), e(b['name']),
        sar(b['total']), n(b.get('total_txn',0)), sar(b.get('avg_ticket',0)),
        sar(b.get('xl_gross_profit') or b.get('gross_profit_real',0)),
        pct(b.get('xl_gross_margin') or b.get('gross_margin_real',0)),
        sar(b.get('cogs_real',0)),
        '#22c55e' if (b.get('xl_net_profit') or 0) >= 0 else '#e92c30',
        sar(b.get('xl_net_profit') or b.get('gross_profit_real',0)),
        'tg' if (b.get('xl_net_profit') or 0) >= 0 else 'tr',
        pct(b.get('xl_net_margin') or b.get('gross_margin_real',0))
    )
    for i, b in enumerate(B))

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
# ── Excel P&L variables (from excel_pnl in data.json) ──────────────────────



RANK=''.join(
    ('<div class="rrow"><div class="rn">%d</div><div class="rnm">%s</div>'
     '<div class="rbb"><div class="rbf" style="width:%d%%;background:%s"></div></div>'
     '<div class="rv" style="color:%s"><strong>%s</strong></div>'
     '<span class="tag %s" style="font-size:10px">%s %s</span></div>') % (
        i+1, e(b['name']),
        max(0, int(abs(b.get('xl_net_profit',0)) / max(abs(_Bxl2[0].get('xl_net_profit',1)) if _Bxl2 else 1, 1) * 100)),
        COLORS[i%8],
        '#22c55e' if b.get('xl_net_profit',0)>=0 else '#e92c30',
        sar(b.get('xl_net_profit',0)),
        'tg' if b.get('xl_net_profit',0)>=0 else 'tr',
        pct(b.get('xl_net_margin',0)), e('\u0635\u0627\u0641\u064a')
    )
    for i,b in enumerate(_Bxl2))

MEDALS=['&#127947;','&#127948;','&#127949;','4.','5.','6.']
TOP3=''.join(
    ('<div class="card" style="margin-bottom:8px;border-right:4px solid %s">'
     '<div style="display:flex;justify-content:space-between">'
     '<span style="font-weight:700">%s %s</span>'
     '<span class="tag %s">%s</span></div>'
     '<div style="font-size:11px;color:#64748b;margin-top:5px">'
     '%s: %s | %s: %s | %s: %s | %s: %s</div></div>') % (
        COLORS[i%8],
        ['\U0001f947','\U0001f948','\U0001f949','4.'][i] if i<4 else '',
        e(b['name']),
        'tg' if b.get('xl_net_profit',0)>=0 else 'tr',
        sar(b.get('xl_net_profit',0)),
        e('\u0635\u0627\u0641\u064a%'), pct(b.get('xl_net_margin',0)),
        e('\u062e\u0627\u0645%'), pct(b.get('xl_gross_margin',0)),
        e('\u0631\u0648\u0627\u062a\u0628'), sar(b.get('xl_salaries',0)),
        e('\u0625\u064a\u062c\u0627\u0631'), sar(b.get('xl_rent',0))
    )
    for i, b in enumerate((_Bxl2 or Bsrt)[:4]))

# JS data (ensure_ascii=True → no Arabic in JS)
CL=json.dumps(COLORS)
BJ=json.dumps(B,  ensure_ascii=True)
YJ=json.dumps(YB, ensure_ascii=True)
HJ=json.dumps(HR)
DJ=json.dumps(DY)
PJ=json.dumps(PT, ensure_ascii=True)

CSS="""
/* ── Reset & Base ─────────────────────────────────────────────────────── */
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f0f2f7;
  --surface:#ffffff;
  --surface2:#f8fafc;
  --nav:#0f172a;
  --nav2:#1e293b;
  --blue:#2ba9ed;
  --blue-light:#eff8ff;
  --blue-mid:#bae6fd;
  --red:#e92c30;
  --green:#16a34a;
  --green-light:#dcfce7;
  --amber:#d97706;
  --amber-light:#fef3c7;
  --purple:#7c3aed;
  --purple-light:#ede9fe;
  --text:#0f172a;
  --text2:#475569;
  --text3:#94a3b8;
  --border:#e2e8f0;
  --border2:#f1f5f9;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.06);
  --shadow-md:0 4px 6px -1px rgba(0,0,0,.08),0 2px 4px -2px rgba(0,0,0,.06);
  --shadow-lg:0 10px 15px -3px rgba(0,0,0,.08),0 4px 6px -4px rgba(0,0,0,.05);
  --radius:12px;
  --radius-sm:8px;
  --radius-lg:16px;
}
html{overflow-x:hidden}
body{
  font-family:'Tajawal',sans-serif;
  background:var(--bg);
  color:var(--text);
  direction:rtl;
  font-size:14px;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
}
/* ── Top Navigation ────────────────────────────────────────────────────── */
.bar{
  background:linear-gradient(135deg,var(--nav) 0%,var(--nav2) 100%);
  padding:0 24px;
  height:66px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  position:sticky;
  top:0;
  z-index:200;
  box-shadow:0 4px 20px rgba(0,0,0,.25);
}
.lw{display:flex;align-items:center;gap:14px}
.logo-badge{
  background:var(--blue);
  border-radius:10px;
  padding:5px 10px;
  display:flex;
  align-items:center;
  overflow:hidden;
}
.logo-badge img{height:36px;width:auto;display:block;object-fit:contain}
.t1{
  font-size:14px;
  font-weight:700;
  color:#ffffff;
  letter-spacing:-.2px;
  line-height:1.3;
}
.t2{font-size:11px;color:rgba(255,255,255,.55);margin-top:2px;font-weight:400}
.badge{
  font-size:11px;
  background:rgba(43,169,237,.25);
  color:#7dd3fc;
  border:1px solid rgba(43,169,237,.35);
  padding:4px 14px;
  border-radius:20px;
  font-weight:600;
  letter-spacing:.3px;
}
.upd{font-size:11px;color:rgba(255,255,255,.4);font-family:'Cairo',monospace;font-weight:400}
/* ── Layout ───────────────────────────────────────────────────────────── */
.wrap{padding:20px 24px;max-width:1520px;margin:0 auto}
.phdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;flex-wrap:wrap;gap:10px}
.phdr h2{font-size:20px;font-weight:800;color:var(--text);letter-spacing:-.4px}
.phdr p{font-size:12px;color:var(--text2);margin-top:3px;font-weight:400}
.per{
  font-size:11px;color:var(--blue);
  background:var(--blue-light);
  border:1px solid var(--blue-mid);
  padding:5px 14px;border-radius:20px;font-weight:700;letter-spacing:.3px;
}
/* ── KPI Grids ─────────────────────────────────────────────────────────── */
.kg5{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:12px}
.kg4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:14px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}
/* ── KPI Cards ─────────────────────────────────────────────────────────── */
.kc{
  background:var(--surface);
  border-radius:var(--radius);
  padding:18px 20px;
  box-shadow:var(--shadow);
  border:1px solid var(--border2);
  position:relative;
  overflow:hidden;
  transition:transform .15s,box-shadow .15s;
}
.kc::before{
  content:'';
  position:absolute;top:0;right:0;left:0;height:3px;
  background:var(--accent,var(--blue));
}
.kc:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
.kl{
  font-size:10px;
  color:var(--text3);
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.8px;
  margin-bottom:10px;
}
.kv{
  font-size:22px;
  font-weight:800;
  color:var(--text);
  line-height:1;
  font-family:'Cairo','Tajawal',monospace;
  letter-spacing:-.5px;
}
.ks{font-size:11px;color:var(--text2);margin-top:6px;font-weight:500}
/* ── Tabs ──────────────────────────────────────────────────────────────── */
.tabs{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:5px;
  display:flex;
  gap:4px;
  margin-bottom:20px;
  overflow-x:auto;
  flex-wrap:wrap;
  box-shadow:var(--shadow);
}
.tab{
  padding:9px 16px;
  background:none;
  border:none;
  cursor:pointer;
  font-size:12px;
  color:var(--text2);
  border-radius:var(--radius-sm);
  font-family:'Tajawal',sans-serif;
  white-space:nowrap;
  font-weight:600;
  transition:all .15s;
  letter-spacing:.1px;
}
.tab:hover{background:var(--bg);color:var(--text)}
.tab.on{
  background:var(--blue);
  color:#ffffff;
  box-shadow:0 2px 8px rgba(43,169,237,.4);
}
/* ── Panes ─────────────────────────────────────────────────────────────── */
.pane{display:none}
/* ── Cards ─────────────────────────────────────────────────────────────── */
.card{
  background:var(--surface);
  border:1px solid var(--border2);
  border-radius:var(--radius);
  padding:18px 20px;
  margin-bottom:14px;
  box-shadow:var(--shadow);
}
.st{
  font-size:11px;
  font-weight:700;
  color:var(--text3);
  text-transform:uppercase;
  letter-spacing:.8px;
  margin-bottom:14px;
  display:flex;
  align-items:center;
  gap:10px;
}
.st::after{content:'';flex:1;height:1px;background:var(--border)}
.cw{position:relative;width:100%}
/* ── Tables ────────────────────────────────────────────────────────────── */
table.dt{width:100%;border-collapse:collapse;font-size:13px}
table.dt th{
  padding:10px 13px;
  font-size:10px;
  font-weight:700;
  color:var(--text3);
  border-bottom:2px solid var(--border);
  text-align:right;
  background:var(--surface2);
  text-transform:uppercase;
  letter-spacing:.6px;
  white-space:nowrap;
}
table.dt th:first-child{border-radius:8px 0 0 0}
table.dt th:last-child{border-radius:0 8px 0 0}
table.dt td{
  padding:11px 13px;
  border-bottom:1px solid var(--border2);
  vertical-align:middle;
  font-weight:400;
}
table.dt tbody tr:last-child td{border-bottom:none}
table.dt tbody tr:hover td{background:#f8faff}
table.dt tfoot td{
  background:var(--surface2);
  font-weight:700;
  border-top:2px solid var(--border);
  border-bottom:none;
}
/* ── Tags/Badges ───────────────────────────────────────────────────────── */
.tag{
  display:inline-flex;align-items:center;gap:3px;
  font-size:10px;padding:3px 8px;border-radius:6px;
  font-weight:700;font-family:'Cairo','Tajawal',monospace;
  letter-spacing:.2px;
}
.tg{background:var(--green-light);color:#15803d}
.tr{background:#fee2e2;color:#b91c1c}
.tn{background:var(--border2);color:var(--text2)}
.tbl{background:var(--purple-light);color:#6d28d9}
.nm{font-family:'Cairo','Tajawal',monospace;font-weight:600}
/* ── Heat Maps ─────────────────────────────────────────────────────────── */
.hmap{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-top:6px}
.hcell{
  height:40px;border-radius:6px;
  display:flex;align-items:center;justify-content:center;
  font-size:9px;color:var(--text);font-family:'Cairo',monospace;font-weight:700;
  transition:transform .1s;cursor:default;
}
.hcell:hover{transform:scale(1.1);z-index:1}
.hlabel{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-bottom:4px}
.hlbl{font-size:9px;color:var(--text3);text-align:center;font-family:'Cairo',monospace}
.dmap{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:8px}
.dcell{
  border-radius:var(--radius-sm);padding:14px 6px;text-align:center;
  border:1px solid var(--border2);background:var(--surface);
  transition:transform .1s,box-shadow .1s;
}
.dcell:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}
.dcell-lbl{font-size:10px;color:var(--text2);margin-bottom:6px;font-weight:600;letter-spacing:.3px}
.dcell-val{font-size:14px;font-weight:800;font-family:'Cairo',monospace;color:var(--text)}
/* ── Ranking Rows ──────────────────────────────────────────────────────── */
.rrow{
  display:flex;align-items:center;gap:12px;
  padding:12px 0;border-bottom:1px solid var(--border2);
  transition:background .1s;
}
.rrow:last-child{border-bottom:none}
.rrow:hover{background:var(--bg);margin:0 -8px;padding:12px 8px;border-radius:8px;border-bottom-color:transparent}
.rn{
  font-size:16px;font-weight:900;font-family:'Cairo',monospace;
  color:var(--text3);width:28px;text-align:center;flex-shrink:0;
}
.rrow:nth-child(1) .rn{color:var(--amber);font-size:20px}
.rrow:nth-child(2) .rn{color:var(--text2);font-size:18px}
.rrow:nth-child(3) .rn{color:#b45309;font-size:17px}
.rnm{min-width:140px;font-size:13px;font-weight:700;color:var(--text)}
.rbb{flex:1;height:8px;background:var(--border);border-radius:10px;overflow:hidden}
.rbf{height:100%;border-radius:10px;transition:width .6s ease}
.rv{font-size:12px;font-family:'Cairo',monospace;font-weight:700;min-width:90px;text-align:left;color:var(--text2)}
/* ── Delivery Cards ────────────────────────────────────────────────────── */
.del-box{display:flex;gap:14px;margin-bottom:18px;flex-wrap:wrap}
.dc{
  flex:1;min-width:150px;
  background:var(--surface);
  border-radius:var(--radius);
  padding:16px 18px;
  border:1px solid var(--border2);
  text-align:center;
  box-shadow:var(--shadow);
  transition:transform .15s;
}
.dc:hover{transform:translateY(-2px)}
.dl{font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.6px;margin-bottom:8px}
.dv{font-size:20px;font-weight:800;font-family:'Cairo',monospace;letter-spacing:-.5px}
/* ── Recommendation Cards ──────────────────────────────────────────────── */
.rec{
  padding:14px 16px;background:var(--surface);border-radius:var(--radius-sm);
  border:1px solid var(--border2);border-right:4px solid var(--amber);margin-bottom:10px;
  box-shadow:var(--shadow);transition:transform .1s;
}
.rec:hover{transform:translateX(-2px)}
.rec.gn{border-right-color:var(--green)}
.rec.rd{border-right-color:var(--red)}
.rec.bl{border-right-color:var(--blue)}
.rt{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px}
.rb{font-size:12px;color:var(--text2);line-height:1.7}
/* ── Executive Summary ─────────────────────────────────────────────────── */
.exec{
  background:linear-gradient(135deg,var(--blue-light) 0%,#f0f9ff 100%);
  border:1px solid var(--blue-mid);
  border-radius:var(--radius);
  padding:18px 20px;
  font-size:13px;
  color:var(--text2);
  line-height:2;
  margin-top:16px;
}
.exec strong{color:var(--text);font-weight:700}
/* ── Excel Banner ─────────────────────────────────────────────────────── */
.xl-banner{
  display:flex;justify-content:space-between;align-items:center;
  background:linear-gradient(135deg,#fef3c7,#fffbeb);
  border:1px solid #fde68a;border-radius:var(--radius-sm);
  padding:10px 16px;margin-bottom:16px;flex-wrap:wrap;gap:8px;
}
.xl-banner span{font-size:12px;color:#92400e;font-weight:700}
/* ── Responsive ─────────────────────────────────────────────────────────────
   Breakpoints:
     Tablet  : ≤ 1024px
     Mobile  : ≤ 768px
     Small   : ≤ 480px
─────────────────────────────────────────────────────────────────────────── */

/* ── Tablet (≤1024px) ─────────────────────────────────────────────────── */
@media(max-width:1024px){
  .wrap{padding:16px}
  .kg5{grid-template-columns:repeat(3,1fr)}
  .kg4{grid-template-columns:repeat(2,1fr)}
  .kv{font-size:20px}
  table.dt th,table.dt td{padding:9px 10px;font-size:12px}
}

/* ── Mobile (≤768px) ──────────────────────────────────────────────────── */
@media(max-width:768px){
  /* Critical overflow fixes */
  html,body{overflow-x:hidden;width:100%}
  *{max-width:100%;box-sizing:border-box}
  /* Navbar */
  .bar{height:56px;padding:0 12px;overflow:hidden}
  .logo-badge img{height:28px}
  .logo-badge{padding:4px 8px}
  .t1{font-size:12px}
  .t2{display:none}
  .upd{display:none}
  .badge{font-size:10px;padding:3px 10px}

  /* Layout */
  .wrap{padding:12px 10px;width:100%;max-width:100%}
  .phdr{flex-direction:column;gap:8px}
  .phdr h2{font-size:17px}
  .per{font-size:10px}

  /* KPI grids */
  .kg5{grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
  .kg4{grid-template-columns:1fr 1fr;gap:10px}
  .g2{grid-template-columns:1fr}
  .g3{grid-template-columns:1fr}
  .kc{padding:14px 16px}
  .kv{font-size:15px;line-height:1.1;word-break:break-word}
  .kl{font-size:9px}
  .ks{font-size:10px}

  /* Tabs */
  .tabs{
    gap:4px;padding:6px;margin-bottom:14px;
    display:grid;grid-template-columns:repeat(3,1fr);
  }
  .tab{padding:8px 6px;font-size:10px;text-align:center;border-radius:6px}

  /* Cards */
  .card{padding:14px 12px;margin-bottom:10px}
  .st{font-size:10px;margin-bottom:10px}

  /* Tables — horizontal scroll */
  .card:has(table.dt){overflow-x:auto;-webkit-overflow-scrolling:touch}
  table.dt{min-width:420px;width:max-content}
  table.dt th,table.dt td{padding:8px 9px;font-size:11px;white-space:nowrap}

  /* Fallback for browsers without :has() */
  .tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 -12px;padding:0 12px}

  /* Charts */
  .cw canvas{height:200px!important}

  /* Ranking */
  .rrow{gap:8px}
  .rnm{min-width:90px;font-size:11px}
  .rv{min-width:70px;font-size:11px}
  .rn{width:22px;font-size:14px}

  /* Delivery boxes */
  .del-box{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .dc{min-width:0;padding:12px 10px}
  .dv{font-size:16px}

  /* Heatmap */
  .hmap,.hlabel{grid-template-columns:repeat(12,1fr)}
  .hcell{height:32px;font-size:8px}
  .hlbl{font-size:8px}
  .hcell:nth-child(n+13){display:none}
  .hlabel span:nth-child(n+13){display:none}

  /* Day map */
  .dmap{grid-template-columns:repeat(4,1fr);gap:6px}
  .dcell{padding:10px 4px}
  .dcell-val{font-size:12px}

  /* Executive summary */
  .exec{font-size:12px;padding:14px 14px;line-height:1.9}

  /* Recommendation cards */
  .rec{padding:11px 12px}
  .rt{font-size:12px}
  .rb{font-size:11px}

  /* XL banner */
  .xl-banner{flex-direction:column;gap:6px}

  /* Header in panes */
  .phdr p{display:none}
}

/* ── Small phones (≤480px) ────────────────────────────────────────────── */
@media(max-width:480px){
  .kg5,.kg4{grid-template-columns:1fr 1fr}
  .kv{font-size:17px}
  .wrap{padding:10px 8px}
  .kv{font-size:17px}
  .tabs{grid-template-columns:repeat(3,1fr)}
  .tab{font-size:9px;padding:7px 4px}
  .bar{height:50px}
  .logo-badge img{height:24px}
  .t1{font-size:11px}
  .badge{display:none}
  .del-box{grid-template-columns:1fr 1fr}
  .dmap{grid-template-columns:repeat(3,1fr)}
  table.dt{min-width:380px}
  table.dt th,table.dt td{padding:6px 7px;font-size:10px}
  .rrow{flex-wrap:wrap}
  .rbb{width:100%;order:3}
  .rnm{order:1}
  .rv{order:2}
  .rn{order:0}
}
"""

# JS data variables (ensure_ascii=True → no Arabic in JS strings)
CL = json.dumps(COLORS)
BJ = json.dumps([{k:v for k,v in b.items() if not isinstance(v,dict)} for b in B], ensure_ascii=True)
YJ = json.dumps(YB, ensure_ascii=True, default=str)
HJ = json.dumps(HR)
DJ = json.dumps(DY)
PJ = json.dumps(PT, ensure_ascii=True)

JS="""
var C=CL_VAR,B=BJ_VAR,YB=YJ_VAR,H=HJ_VAR,D=DJ_VAR,P=PJ_VAR,CH={};
function fmt(v){return Math.abs(v)>=1e6?(v/1e6).toFixed(2)+"M":Math.abs(v)>=1e3?(v/1e3).toFixed(1)+"K":Math.round(v).toLocaleString();}
/* ── Chart defaults ─────────────────────────────────────────────────── */
Chart.defaults.font.family="'Cairo','Tajawal',sans-serif";
Chart.defaults.color="#94a3b8";
Chart.defaults.plugins.tooltip.backgroundColor="#0f172a";
Chart.defaults.plugins.tooltip.titleColor="#ffffff";
Chart.defaults.plugins.tooltip.bodyColor="#94a3b8";
Chart.defaults.plugins.tooltip.borderColor="#1e293b";
Chart.defaults.plugins.tooltip.borderWidth=1;
Chart.defaults.plugins.tooltip.padding=10;
Chart.defaults.plugins.tooltip.cornerRadius=8;
/* ── Tab switch ─────────────────────────────────────────────────────── */
function sw(n){var i,t,p;for(i=0;i<9;i++){t=document.getElementById("t"+i);p=document.getElementById("p"+i);if(t)t.className="tab"+(i===n?" on":"");if(p)p.style.display=(i===n)?"block":"none";}if(n===0)setTimeout(dOv,60);else if(n===1)setTimeout(dGr,60);else if(n===2)setTimeout(dExp,60);else if(n===5)setTimeout(dTm,60);else if(n===6)setTimeout(dPy,60);else if(n===7)setTimeout(dYT,60);}
function mk(id,cfg){var el=document.getElementById(id);if(!el)return;if(CH[id])CH[id].destroy();try{CH[id]=new Chart(el,cfg);}catch(e){console.error(id,e);}}
/* ── Chart: Overview ─────────────────────────────────────────────────── */
function dOv(){
  if(CH.ch_rev)return;
  var gradient;
  try{
    var ctx=document.getElementById("ch_rev").getContext("2d");
    // Revenue bar chart - horizontal for better readability
    mk("ch_rev",{type:"bar",data:{
      labels:B.map(function(b){return b.name.replace(" (FR)","").replace("Jed - ","").replace("Jed- ","").replace("Medinah - ","");}),
      datasets:[{
        data:B.map(function(b){return b.total;}),
        backgroundColor:C,
        borderRadius:6,
        borderSkipped:false,
      }]
    },options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.raw)+" ر.س";}}}},
      scales:{
        x:{ticks:{color:"#64748b",font:{size:11,family:"'Cairo',monospace",weight:"600"}},grid:{display:false}},
        y:{ticks:{color:"#94a3b8",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.5)",drawBorder:false}}
      }
    }});
    // Donut chart
    mk("ch_pie",{type:"doughnut",data:{
      labels:B.map(function(b){return b.name.replace(" (FR)","");}),
      datasets:[{data:B.map(function(b){return b.total;}),backgroundColor:C,borderWidth:3,borderColor:"#ffffff",hoverOffset:6}]
    },options:{
      responsive:true,maintainAspectRatio:false,cutout:"65%",
      plugins:{
        legend:{display:true,position:"bottom",labels:{color:"#475569",font:{size:10,family:"'Tajawal',sans-serif"},boxWidth:10,padding:8,usePointStyle:true}},
        tooltip:{callbacks:{label:function(c){var t=B.reduce(function(s,b){return s+b.total;},0);return " "+fmt(c.raw)+" ("+((c.raw/t)*100).toFixed(1)+"%)";}}},
      }
    }});
  }catch(e){console.error("dOv",e);}
}
/* ── Chart: Growth ───────────────────────────────────────────────────── */
function dGr(){
  if(CH.ch_qoq)return;
  try{
    var names=B.map(function(b){return b.name.replace(" (FR)","").replace("Jed - ","").replace("Jed- ","").replace("Medinah - ","");});
    mk("ch_qoq",{type:"bar",data:{
      labels:names,
      datasets:[{
        data:B.map(function(b){return b.qoq||0;}),
        backgroundColor:B.map(function(b){return(b.qoq||0)>=0?"rgba(22,163,74,.8)":"rgba(220,38,38,.8)";}),
        borderRadius:6,borderSkipped:false,
      }]
    },options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+c.raw.toFixed(1)+"%";}}}},
      scales:{x:{ticks:{color:"#64748b",font:{size:11}},grid:{display:false}},y:{ticks:{color:"#94a3b8",font:{size:10},callback:function(v){return v+"%";}},grid:{color:"rgba(226,232,240,.5)"},zero:true}}
    }});
    mk("ch_margin",{type:"bar",data:{
      labels:names,
      datasets:[{
        data:B.map(function(b){return b.xl_gross_margin||b.gross_margin_real||0;}),
        backgroundColor:B.map(function(b){var r=b.xl_gross_margin||b.gross_margin_real||0;return r>=40?"rgba(22,163,74,.8)":r>=30?"rgba(217,119,6,.8)":"rgba(220,38,38,.8)";}),
        borderRadius:6,borderSkipped:false,indexAxis:"y",
      }]
    },options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+c.raw.toFixed(1)+"%";}}}},
      scales:{
        x:{ticks:{color:"#94a3b8",font:{size:10},callback:function(v){return v+"%";}},grid:{color:"rgba(226,232,240,.5)"},min:0},
        y:{ticks:{color:"#64748b",font:{size:11}},grid:{display:false}}
      }
    }});
  }catch(e){console.error("dGr",e);}
}
/* ── Chart: Expenses ─────────────────────────────────────────────────── */
function dExp(){
  if(CH.ch_exp)return;
  try{
    var EX=EX_JSON_PLACEHOLDER;
    mk("ch_exp",{type:"bar",data:{
      labels:EX.map(function(e){return e.label;}),
      datasets:[{data:EX.map(function(e){return e.amount;}),backgroundColor:["#e92c30","#f59e0b","#2ba9ed","#8b5cf6","#06b6d4","#22c55e","#ec4899","#10b981"],borderRadius:6,indexAxis:"y"}]
    },options:{
      responsive:true,maintainAspectRatio:false,indexAxis:"y",
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.raw)+" ر.س";}}}},
      scales:{
        x:{ticks:{color:"#94a3b8",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.5)"},drawBorder:false},
        y:{ticks:{color:"#475569",font:{size:12,weight:"600"}},grid:{display:false}}
      }
    }});
  }catch(e){console.error("dExp",e);}
}
/* ── Chart: Timing ───────────────────────────────────────────────────── */
function dTm(){
  if(CH.ch_hr)return;
  try{
    mk("ch_hr",{type:"line",data:{
      labels:Array.from({length:24},function(_,h){return(h<10?"0"+h:h)+":00";}),
      datasets:[{
        data:H,
        borderColor:"#2ba9ed",
        backgroundColor:"rgba(43,169,237,.08)",
        borderWidth:2.5,fill:true,tension:.4,pointRadius:0,pointHoverRadius:5,
        pointHoverBackgroundColor:"#2ba9ed",
      }]
    },options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.raw)+" ر.س";}}}},
      scales:{
        x:{ticks:{color:"#94a3b8",font:{size:9,family:"'Cairo',monospace"}},grid:{color:"rgba(226,232,240,.3)"}},
        y:{ticks:{color:"#94a3b8",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.5)"},drawBorder:false}
      }
    }});
  }catch(e){console.error("dTm",e);}
}
/* ── Chart: Payments ─────────────────────────────────────────────────── */
function dPy(){
  if(CH.ch_pay)return;
  try{
    var ks=Object.keys(P),vs=ks.map(function(k){return P[k];});
    mk("ch_pay",{type:"doughnut",data:{
      labels:ks,
      datasets:[{data:vs,backgroundColor:C.slice(0,ks.length),borderWidth:3,borderColor:"#ffffff",hoverOffset:6}]
    },options:{
      responsive:true,maintainAspectRatio:false,cutout:"60%",
      plugins:{
        legend:{display:true,position:"right",labels:{color:"#475569",font:{size:11,family:"'Tajawal',sans-serif"},boxWidth:12,padding:10,usePointStyle:true}},
        tooltip:{callbacks:{label:function(c){var t=vs.reduce(function(a,b){return a+b;},0);return " "+fmt(c.raw)+" ("+((c.raw/t)*100).toFixed(1)+"%)";}}},
      }
    }});
  }catch(e){console.error("dPy",e);}
}
/* ── Chart: YTD ──────────────────────────────────────────────────────── */
function dYT(){
  if(CH.ch_ytd)return;
  try{
    var mo={};YB.forEach(function(b){if(b.monthly)Object.keys(b.monthly).forEach(function(k){mo[k]=(mo[k]||0)+b.monthly[k];});});
    var ks=Object.keys(mo).sort();
    mk("ch_ytd",{type:"bar",data:{
      labels:ks,
      datasets:[{
        data:ks.map(function(k){return Math.round(mo[k]);}),
        backgroundColor:"rgba(43,169,237,.7)",
        borderColor:"rgba(43,169,237,1)",
        borderWidth:1.5,borderRadius:6,
      }]
    },options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return " "+fmt(c.raw)+" ر.س";}}}},
      scales:{
        x:{ticks:{color:"#64748b",font:{size:11}},grid:{display:false}},
        y:{ticks:{color:"#94a3b8",font:{size:10},callback:function(v){return fmt(v);}},grid:{color:"rgba(226,232,240,.5)"},drawBorder:false}
      }
    }});
  }catch(e){console.error("dYT",e);}
}
dOv();
"""
# Inject JSON data into JS
JS = (JS
    .replace('CL_VAR', CL)
    .replace('BJ_VAR', BJ)
    .replace('YJ_VAR', YJ)
    .replace('HJ_VAR', HJ)
    .replace('DJ_VAR', DJ)
    .replace('PJ_VAR', PJ)
)


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
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>"""+CSS+"""</style>
</head>
<body>
<div class="bar">
  <div class="lw">
    <div class="logo-badge"><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAEEAcIDASIAAhEBAxEB/8QAHAABAAIDAQEBAAAAAAAAAAAAAAUGAwQHCAIB/8QATxAAAQQBAgMEBAcNBQUIAwAAAQACAwQFBhESITEHE0FRImFxgRQVFjJVkdEIIzNCUmJylJWhscHSNlZ0k7IkN1NUsxc0c4KSorThJUTC/8QAGwEBAAIDAQEAAAAAAAAAAAAAAAMEAgUGAQf/xAAzEQACAQMBBQUHBAMBAAAAAAAAAQIDBBEFEiExQVETYXGBsSKRocHR4fAGFDJSI0Lx0v/aAAwDAQACEQMRAD8AkkRF9YPiIREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBEaC4hrQSTyAHir3e0JJh+z21ncs1zLzzGIYOnctLxuXfnEeHh7ekFa5p0XFTe+Twizb2lW4UpQW6Kbb6JFERXjSOiflNoi3eou4cnWtuaxpPoys4GHg9R3J2Pr5+YpViGWvPJBPG+KWNxa9jxsWkdQQlK5p1ZyhF748UK1pVowhUkvZkspnwiIpysEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREARoLiGtBJPIAeKNBcQ1oJJ5ADxXbOyjs+GNEWczkIN0+lXruH4D85353q8Pb0pX19Ts6e3PjyXU2Gm6bV1Cr2dPhzfRfnIdlHZ8MaIs5nIQbp9KvXcPwH5zvzvV4e3pM9tX+727/AOJF/rCui5z26ZvHwabdgzLxXrLmPEbefA1rgeJ3lvtsFxlvcVr3UITlveV5JM+gXdrb6fpdSnDctl+ba9WfP3Pn9k73+Pd/02Lc7UNBxaigdksaxkWVjb7BYA/FP53kfcfVAdgObx8NS1gppe7uSzmeIO5CQcLQQD5jh328veutrPUK1a01GVSG5596+hhpdChfaVClPesY8H8meSbEMteeSCeN8Usbi17HjYtI6ghfC772oaDi1FA7JY1jIsrG32CwB+KfzvI+4+rgtiGWvPJBPG+KWNxa9jxs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K37uJ7ty3b+HAmhqjLg8bH1I5/8AmI6ULZv/AFhvED6991GV7UsV0WyI5pQ4uPfsEgcT14g7cH3rAixjSpxzsxSyZyr1JtOUm8d5NfKS19HYX9mQ/wBK/HajtFpHxdhhuPDGQ/0qGRY/t6X9UZfuq39mSmPztylQFFsNGeBsjpWtsVI5eFzg0EguB23DW/Us3yktfR2F/ZkP9KhUXroU28uKPFc1ksKTJG1mbU89ecQUa8ld4kjNepHF6QII34QN+nitqTU1yR7nvoYZznElxONhJJ8/mqERHQpv/VBXNZZak95NfKS19HYX9mQ/0rUoZWanJNIyrQlMzuIiapHIG9fmhwPCOfQepaCIqNNJpRDuKrabk9xNfKS19HYX9mQ/0rWyOYnvV+4kqY2Ju4PFBSjid/6mgFRyIqFOLyoiVzVksOTM161PdtOs2X8crgATsB0AA6eoBYURSJJLCIm3J5Zt5XJXcpOye/YdPKyNsQe7rwtGw3Pj7TzWxSz2Sq1W1BJDPWZvwRWa7JmN38g8Hb3bKMRYOlBxUWlgzVaopOak8vnk3cnlb+S7sW5+KOP8HExjWRs/RY0Bo9wWelnLFWsyuyli5Gs6OloRPeefi4t3Ki0R0oOOzjceqvUUtraeSa+Ulr6Owv7Mh/pUfk70l+VskkFSEtbwgV67IgfaGgblaqJGjTi8xQnXqTWJSbQREUhEEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREB//Z" alt="Compass of Excellence"></div>
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
<div style="margin:-8px 0 12px;padding:7px 14px;background:#fffbeb;border-radius:7px;border:1px solid #fde68a;font-size:11px;color:#92400e;font-weight:600">&#128196; &#1576;&#1610;&#1575;&#1606;&#1575;&#1578; &#1575;&#1604;&#1605;&#1589;&#1575;&#1585;&#1610;&#1601; &#1605;&#1606; &#1605;&#1604;&#1601; &#1573;&#1603;&#1587;&#1604; &#8212; &#1575;&#1604;&#1571;&#1585;&#1602;&#1575;&#1605; &#1576;&#1583;&#1608;&#1606; &#1590;&#1585;&#1610;&#1576;&#1577; &#1575;&#1604;&#1602;&#1610;&#1605;&#1577; &#1575;&#1604;&#1605;&#1590;&#1575;&#1601;&#1577; 15%</div>
<div class="kg5">"""+KPIS2+"""</div>
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
  <thead><tr>"""+ths('الفرع','إيرادات+VAT','معاملات','م.فاتورة','ربح خام','هامش خام','تكلفة','صافي الربح','هامش صافي')+"""</tr></thead>
  <tbody>"""+BROWS+"""</tbody>
  <tfoot><tr><td><strong>"""+e('\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a')+"""</strong></td><td class="nm"><strong>"""+sar(TR)+"""</strong></td><td class="nm"><strong>"""+n(TXN)+"""</strong></td><td class="nm"><strong>"""+sar(ATK)+"""</strong></td><td class="nm" style="color:#22c55e"><strong>"""+sar(XL_GP if XL_GP else TGP)+"""</strong></td><td><strong>"""+pct(XL_GM if XL_GP else TGP/TR*100 if TR else 0)+"""</strong></td><td></td><td class="nm" style="color:""" + ("#22c55e" if True else "#e92c30") + """"><strong>"""+sar(XL_NET)+"""</strong></td><td><span class="tag tg">"""+pct(XL_NM)+"""</span></td></tr></tfoot>
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
        """+e('\u062d\u0642\u0642\u062a \u0627\u0644\u0634\u0631\u0643\u0629 \u0625\u064a\u0631\u0627\u062f\u0627\u062a')+' <strong>'+sar(TR)+'</strong> | '+e('\u0628\u062f\u0648\u0646 VAT:')+' <strong>'+sar(XL_NS)+'</strong><br>'+e('\u0631\u0628\u062d \u062e\u0627\u0645:')+' <strong>'+sar(XL_GP)+'</strong> ('+pct(XL_GM)+') | '+e('\u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0645\u0635\u0627\u0631\u064a\u0641:')+' <strong>'+sar(XL_OP)+'</strong><br>'+e('\u0631\u0648\u0627\u062a\u0628:')+' <strong>'+sar(XL_SAL)+'</strong> | '+e('\u0625\u064a\u062c\u0627\u0631:')+' <strong>'+sar(XL_RNT)+'</strong> | '+e('\u062a\u0648\u0635\u064a\u0644:')+' <strong>'+sar(XL_DLF)+'</strong><br>'+'<strong style="font-size:13px;color:'+('#22c55e' if XL_NET>=0 else '#e92c30')+'">'+e('\u0635\u0627\u0641\u064a \u0627\u0644\u0631\u0628\u062d \u0627\u0644\u0641\u0639\u0644\u064a:')+' '+sar(XL_NET)+' ('+pct(XL_NM)+')</strong><br>'+e('\u0645\u0639\u0627\u0645\u0644\u0627\u062a:')+' <strong>'+n(TXN)+'</strong> | '+e('\u0645\u062a\u0648\u0633\u0637:')+' <strong>'+sar(ATK)+'</strong> | YTD: <strong>'+sar(YR)+'</strong>.'+"""
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
def kc(lbl,val,sub,clr):
    return '<div class="kc" style="--accent:%s"><div class="kl">%s</div><div class="kv">%s</div><div class="ks">%s</div></div>'%(clr,lbl,val,sub)
