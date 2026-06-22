# -*- coding: utf-8 -*-
"""
Q1 2026 Dashboard Generator — Munch Bakery / Compass of Excellence
Builds index.html from data.json
"""
import json, base64, sys, os

REPO = '/tmp/repo'

# ── Load data ───────────────────────────────────────────────────────────────
with open(os.path.join(REPO, 'data.json'), 'r', encoding='utf-8') as f:
    D = json.load(f)

# ── Logo ────────────────────────────────────────────────────────────────────
LOGO = ''
logo_path = '/mnt/user-data/uploads/logo_v3_hex_2ba9ed.png'
if os.path.exists(logo_path):
    with open(logo_path, 'rb') as f:
        LOGO = base64.b64encode(f.read()).decode()

# ── Data shortcuts ──────────────────────────────────────────────────────────
B  = D['branches']
DA = D['delivery_apps']
PT = D['payment_totals']
PR = D['products']
ME = D['monthly_expenses']
CP = D['company_pnl']

COLORS = ['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4']
Q1M = ['2026-01','2026-02','2026-03']
ALL_M = ['2025-10','2025-11','2025-12','2026-01','2026-02','2026-03']
MN_AR = {'2025-10':'أكتوبر','2025-11':'نوفمبر','2025-12':'ديسمبر',
          '2026-01':'يناير','2026-02':'فبراير','2026-03':'مارس'}

# ── Helpers ──────────────────────────────────────────────────────────────────
def ae(s):
    """ASCII-encode Arabic string"""
    return ''.join('&#%d;' % ord(c) if ord(c) > 127 else c for c in str(s))

def sar(v):
    v = float(v or 0)
    sign = '-' if v < 0 else ''
    v = abs(v)
    if v >= 1e6: return sign + 'SAR %.1fM' % (v/1e6)
    if v >= 1e3: return sign + 'SAR %.1fK' % (v/1e3)
    return sign + 'SAR %d' % int(v)

def pct(v):
    return '%.1f%%' % float(v or 0)

def nfmt(v):
    v = float(v or 0)
    if abs(v) >= 1e3: return '%.1fK' % (v/1e3)
    return '%d' % int(v)

def npclr(v):
    return '#22c55e' if float(v or 0) >= 0 else '#e92c30'

def tag_np(v):
    v = float(v or 0)
    cls = 'tg' if v >= 0 else 'tr'
    return '<span class="tag %s">%s</span>' % (cls, pct(v))

def dot(c):
    return '<span style="display:inline-block;width:8px;height:8px;background:%s;border-radius:2px;margin-left:6px"></span>' % c

def th(*args):
    return ''.join('<th>%s</th>' % ae(a) for a in args)

# ── Aggregates ───────────────────────────────────────────────────────────────
T = {
    'rev':    sum(b['q1_revenue'] for b in B),
    'net':    sum(b['q1_net_revenue'] for b in B),
    'gp':     sum(b['q1_gross_profit'] for b in B),
    'opex':   sum(b['q1_opex'] for b in B),
    'np':     sum(b['q1_net_profit'] for b in B),
    'txn':    sum(b['q1_txn'] for b in B),
    'sal':    sum(b['q1_salaries'] for b in B),
    'rent':   sum(b['q1_rent'] for b in B),
    'del':    sum(b['q1_delivery_comm'] for b in B),
    'roy':    sum(b['q1_royalty'] for b in B),
    'mkt':    sum(b['q1_marketing'] for b in B),
}
T['avg_ticket'] = round(T['rev']/T['txn']) if T['txn'] else 0
T['del_total']  = sum(v['total'] for v in DA.values())
T['del_comm']   = sum(v['commission'] for v in DA.values())
T['del_net']    = sum(v['net'] for v in DA.values())
T['del_orders'] = sum(v['count'] for v in DA.values())

best  = max(B, key=lambda x: x['q1_net_profit'])
worst = min(B, key=lambda x: x['q1_net_profit'])

# ── KPI card helper ──────────────────────────────────────────────────────────
def kc(lbl, val, sub, accent='#2ba9ed', val_color='var(--text)'):
    return (
        '<div class="kc" style="--accent:%s">'
        '<div class="kl">%s</div>'
        '<div class="kv" style="color:%s">%s</div>'
        '<div class="ks">%s</div>'
        '</div>'
    ) % (accent, ae(lbl), val_color, val, ae(sub))

# ── Row 1 KPIs ───────────────────────────────────────────────────────────────
gm = round(T['gp']/T['net']*100,1) if T['net'] else 0
nm = round(T['np']/T['net']*100,1) if T['net'] else 0

KPIS1 = (
    kc('الإيرادات Q1 (+VAT)', sar(T['rev']), 'يناير — مارس 2026', '#2ba9ed') +
    kc('صافي الإيرادات', sar(T['net']), 'بدون ضريبة 15%', '#06b6d4') +
    kc('الربح الخام', sar(T['gp']), pct(gm) + ' هامش خام', '#22c55e', '#22c55e') +
    kc('إجمالي المصاريف', sar(T['opex']), 'تشغيلية + ثابتة', '#e92c30', '#e92c30') +
    kc('صافي الربح / الخسارة', sar(T['np']), pct(nm) + (' ✅' if T['np']>=0 else ' ⚠️'), '#22c55e' if T['np']>=0 else '#e92c30', npclr(T['np']))
)

# ── Row 2 KPIs ───────────────────────────────────────────────────────────────
KPIS2 = (
    kc('المعاملات Q1', nfmt(T['txn']), 'إجمالي الطلبات', '#f59e0b') +
    kc('متوسط الفاتورة', sar(T['avg_ticket']), 'لكل طلب', '#8b5cf6') +
    kc('إيرادات التوصيل', sar(T['del_total']), '%s طلب' % nfmt(T['del_orders']), '#2ba9ed') +
    kc('عمولات التوصيل', sar(T['del_comm']), 'مدفوعة للتطبيقات', '#e92c30', '#e92c30') +
    kc('أفضل فرع (صافي)', ae(best.get('name_ar','')), sar(best.get('q1_net_profit',0)), '#22c55e', '#22c55e')
)

# ── Branch P&L table rows ────────────────────────────────────────────────────
def branch_row(b):
    np_val = b['q1_net_profit']
    nc = npclr(np_val)
    return (
        '<tr>'
        '<td><div style="display:flex;align-items:center;gap:6px">%s<strong>%s</strong></div></td>'
        '<td class="nm">%s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:#22c55e;font-weight:700">%s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:#8b5cf6">%s</td>'
        '<td class="nm" style="color:#f59e0b">%s</td>'
        '<td class="nm" style="color:#e92c30">%s</td>'
        '<td class="nm" style="color:#06b6d4">%s</td>'
        '<td class="nm" style="color:#ec4899">%s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:%s;font-weight:700">%s</td>'
        '<td>%s</td>'
        '</tr>'
    ) % (
        dot(b['color']),
        ae(b['name_ar']),
        sar(b['q1_net_revenue']),
        nfmt(b['q1_txn']),
        sar(b['q1_gross_profit']),
        '<span class="tag tn">%s</span>' % pct(b['q1_gross_margin']),
        sar(b['q1_salaries']),
        sar(b['q1_rent']),
        sar(b['q1_delivery_comm']),
        sar(b['q1_royalty']),
        sar(b['q1_marketing']),
        sar(b['q1_opex']),
        nc, sar(np_val),
        tag_np(b['q1_net_margin'])
    )

total_row = (
    '<tr style="background:var(--surface2);font-weight:700">'
    '<td><strong>%s</strong></td>'
    '<td class="nm"><strong>%s</strong></td>'
    '<td class="nm"><strong>%s</strong></td>'
    '<td class="nm" style="color:#22c55e"><strong>%s</strong></td>'
    '<td class="nm"><span class="tag tn">%s</span></td>'
    '<td class="nm" style="color:#8b5cf6"><strong>%s</strong></td>'
    '<td class="nm" style="color:#f59e0b"><strong>%s</strong></td>'
    '<td class="nm" style="color:#e92c30"><strong>%s</strong></td>'
    '<td class="nm" style="color:#06b6d4"><strong>%s</strong></td>'
    '<td class="nm" style="color:#ec4899"><strong>%s</strong></td>'
    '<td class="nm"><strong>%s</strong></td>'
    '<td class="nm" style="color:%s"><strong>%s</strong></td>'
    '<td>%s</td>'
    '</tr>'
) % (
    ae('الإجمالي'), sar(T['net']), nfmt(T['txn']),
    sar(T['gp']), pct(gm),
    sar(T['sal']), sar(T['rent']), sar(T['del']),
    sar(T['roy']), sar(T['mkt']), sar(T['opex']),
    npclr(T['np']), sar(T['np']), tag_np(nm)
)

# Sort branches by net profit descending for display
B_sorted_np = sorted(B, key=lambda x: -x['q1_net_profit'])
BRANCH_ROWS = ''.join(branch_row(b) for b in B_sorted_np) + total_row

# ── Monthly revenue table ────────────────────────────────────────────────────
B_sorted_rev = sorted(B, key=lambda x: -x['q1_revenue'])

def mon_rev_row(b):
    cells = ''.join(
        '<td class="nm">%s</td>' % sar(b['monthly'].get(m, {}).get('revenue', 0))
        for m in ALL_M
    )
    qoq_val = float(b.get('qoq', 0))
    qoq_tag = '<span class="tag %s" style="font-size:10px">%s%s</span>' % (
        'tg' if qoq_val >= 0 else 'tr',
        '+' if qoq_val >= 0 else '',
        pct(qoq_val)
    )
    return (
        '<tr><td><div style="display:flex;align-items:center;gap:6px">%s<strong>%s</strong></div></td>%s'
        '<td class="nm"><strong>%s</strong></td><td>%s</td></tr>'
    ) % (dot(b['color']), ae(b['name_ar']), cells, sar(b['q1_revenue']), qoq_tag)

totals_by_month = {m: sum(b['monthly'].get(m, {}).get('revenue', 0) for b in B) for m in ALL_M}
total_mon_cells = ''.join('<td class="nm"><strong>%s</strong></td>' % sar(totals_by_month[m]) for m in ALL_M)
MON_REV_ROWS = (
    ''.join(mon_rev_row(b) for b in B_sorted_rev) +
    '<tr style="background:var(--surface2);font-weight:700"><td><strong>%s</strong></td>%s<td class="nm"><strong>%s</strong></td><td></td></tr>' % (
        ae('الإجمالي'), total_mon_cells, sar(T['rev']))
)

# ── Monthly P&L summary table ────────────────────────────────────────────────
def mon_pnl_row(m):
    mrev = totals_by_month.get(m, 0)
    mnet = round(mrev/1.15)
    mgp  = sum(b['monthly'].get(m, {}).get('gross_profit', 0) for b in B)
    mopex = ME.get(m, {}).get('total', 0)
    mnp  = mgp - mopex
    return (
        '<tr><td><strong>%s</strong></td>'
        '<td class="nm">%s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:#22c55e"><strong>%s</strong></td>'
        '<td class="nm"><span class="tag tn">%s</span></td>'
        '<td class="nm" style="color:#e92c30">%s</td>'
        '<td class="nm" style="color:%s"><strong>%s</strong></td>'
        '<td>%s</td></tr>'
    ) % (
        ae(MN_AR.get(m, m)), sar(mrev), sar(mnet),
        sar(mgp), pct(mgp/mnet*100 if mnet else 0),
        sar(mopex),
        npclr(mnp), sar(mnp),
        tag_np(mnp/mnet*100 if mnet else 0)
    )

MON_PNL_ROWS = ''.join(mon_pnl_row(m) for m in Q1M)

# ── Delivery table rows ──────────────────────────────────────────────────────
DEL_ROWS = ''
for app_name, v in sorted(DA.items(), key=lambda x: -x[1]['total']):
    fr, pr, dr = v['fee_rate'], v['payment_fee'], v['delivery_fee_sar']
    fee_str = '%s%%+%s%%' % (fr, pr)
    if dr:
        fee_str += '+%s/%s' % (dr, ae('ط'))
    DEL_ROWS += (
        '<tr><td><strong>%s</strong></td>'
        '<td class="nm">%s %s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="font-size:11px;color:#64748b">%s</td>'
        '<td class="nm" style="color:#e92c30">%s</td>'
        '<td><span class="tag tr" style="font-size:10px">%s</span></td>'
        '<td class="nm" style="color:#22c55e;font-weight:700">%s</td></tr>'
    ) % (ae(app_name), nfmt(v['count']), ae('طلب'), sar(v['total']),
         fee_str, sar(v['commission']), pct(v['effective_rate']), sar(v['net']))

DEL_ROWS += (
    '<tr style="background:var(--surface2);font-weight:700">'
    '<td><strong>%s</strong></td>'
    '<td class="nm"><strong>%s %s</strong></td>'
    '<td class="nm"><strong>%s</strong></td>'
    '<td></td>'
    '<td class="nm" style="color:#e92c30"><strong>%s</strong></td>'
    '<td></td>'
    '<td class="nm" style="color:#22c55e"><strong>%s</strong></td></tr>'
) % (ae('الإجمالي'), nfmt(T['del_orders']), ae('طلب'),
     sar(T['del_total']), sar(T['del_comm']), sar(T['del_net']))

# ── Expense table rows ───────────────────────────────────────────────────────
OPB = CP.get('opex_breakdown_q1', {})
OPEX_ODOO = 1622212
exp_items = [
    ('الرواتب (مبيعات + إدارة)',      OPB.get('salaries', 0),     '#8b5cf6'),
    ('إيجارات الفروع',                 OPB.get('rent', 0),         '#f59e0b'),
    ('خدمات ضيافة/لوبريف',            OPB.get('luopreev_food', 0),'#2ba9ed'),
    ('رسوم الامتياز (Munch Fees)',     OPB.get('royalty', 0),      '#06b6d4'),
    ('رسوم حكومية',                    OPB.get('govt_fees', 0),    '#ec4899'),
    ('تأمين',                          OPB.get('insurance', 0),    '#e92c30'),
    ('كهرباء واتصالات',                OPB.get('electricity', 0),  '#22c55e'),
    ('مصاريف بنكية',                   OPB.get('bank_fees', 0),    '#94a3b8'),
    ('مصاريف أخرى',                    OPB.get('other', 0),        '#64748b'),
]
EXP_ROWS = ''
for lbl, amt, clr in exp_items:
    if not amt:
        continue
    bar_w = int(amt / max(OPEX_ODOO, 1) * 100)
    EXP_ROWS += (
        '<tr><td>%s</td>'
        '<td class="nm" style="color:#e92c30">%s</td>'
        '<td class="nm">%s</td>'
        '<td><div style="height:6px;background:var(--border);border-radius:3px;overflow:hidden">'
        '<div style="height:100%%;width:%d%%;background:%s;border-radius:3px"></div></div></td></tr>'
    ) % (ae(lbl), sar(amt), pct(amt/OPEX_ODOO*100), bar_w, clr)

EXP_ROWS += (
    '<tr style="background:var(--surface2);font-weight:700">'
    '<td><strong>%s</strong></td>'
    '<td class="nm" style="color:#e92c30"><strong>%s</strong></td>'
    '<td class="nm"><strong>100%%</strong></td>'
    '<td></td></tr>'
) % (ae('الإجمالي (Odoo)'), sar(OPEX_ODOO))

# ── Product table rows ───────────────────────────────────────────────────────
max_rev = PR[0]['revenue'] if PR else 1
PROD_ROWS = ''
for i, p in enumerate(PR[:10]):
    bar_w = int(p['revenue'] / max(max_rev, 1) * 100)
    PROD_ROWS += (
        '<tr><td><strong>%d</strong></td>'
        '<td>%s</td>'
        '<td class="nm">%s</td>'
        '<td class="nm" style="color:#22c55e">%s</td>'
        '<td style="width:130px"><div style="height:6px;background:var(--border);border-radius:3px">'
        '<div style="height:100%%;width:%d%%;background:%s;border-radius:3px"></div></div></td></tr>'
    ) % (i+1, ae(p['name']), nfmt(p['qty']), sar(p['revenue']), bar_w, COLORS[i % len(COLORS)])

# ── Payment table rows ───────────────────────────────────────────────────────
PAY_TOTAL = sum(PT.values())
PAY_ROWS = ''
for k, v in sorted(PT.items(), key=lambda x: -x[1]):
    PAY_ROWS += (
        '<tr><td>%s</td>'
        '<td class="nm"><strong>%s</strong></td>'
        '<td><span class="tag tn" style="font-size:10px">%s</span></td></tr>'
    ) % (ae(k), sar(v), pct(v/PAY_TOTAL*100 if PAY_TOTAL else 0))

# ── Waterfall P&L rows ────────────────────────────────────────────────────────
def wf_row(label, amount, color, pct_of_net, bold=False, bg=''):
    sign = '+' if amount >= 0 else ''
    bar_w = min(100, int(abs(pct_of_net)))
    bold_s = 'font-weight:700;' if bold else ''
    bg_s = 'background:%s;' % bg if bg else ''
    return (
        '<div class="wf-row" style="%s">'
        '<div class="wf-label" style="%s">%s</div>'
        '<div class="wf-bar-wrap"><div class="wf-bar" style="width:%d%%;background:%s"></div></div>'
        '<div class="wf-val" style="color:%s;%s">%s%s</div>'
        '</div>'
    ) % (bg_s, bold_s, ae(label), bar_w, color, color, bold_s, sign, sar(amount))

net = T['net']
gp  = T['gp']
cogs = net - gp
np_v = T['np']
sal  = OPB.get('salaries', 0)
rent = OPB.get('rent', 0)
lub  = OPB.get('luopreev_food', 0)
other_opex = OPEX_ODOO - sal - rent - lub

WF_ROWS = (
    wf_row('الإيرادات الإجمالية (+VAT)', T['rev'], '#2ba9ed', 100, True, '#eff8ff') +
    wf_row('(−) ضريبة القيمة المضافة 15%', -(T['rev']-net), '#94a3b8', (T['rev']-net)/T['rev']*100 if T['rev'] else 0) +
    wf_row('= صافي الإيرادات (ex-VAT)', net, '#22c55e', 100, True, '#f0fdf4') +
    wf_row('(−) تكلفة البضاعة المباعة COGS', -cogs, '#f59e0b', cogs/net*100 if net else 0) +
    wf_row('= الربح الخام (%.1f%%)' % gm, gp, '#2ba9ed', gm, True, '#eff8ff') +
    wf_row('(−) الرواتب', -sal, '#8b5cf6', sal/net*100 if net else 0) +
    wf_row('(−) الإيجارات', -rent, '#f59e0b', rent/net*100 if net else 0) +
    wf_row('(−) خدمات الضيافة (لوبريف)', -lub, '#06b6d4', lub/net*100 if net else 0) +
    wf_row('(−) رسوم امتياز + حكومية + أخرى', -other_opex, '#e92c30', other_opex/net*100 if net else 0) +
    wf_row('= صافي الربح التشغيلي (%.1f%%)' % nm, np_v,
           '#22c55e' if np_v >= 0 else '#e92c30', abs(nm), True,
           '#f0fdf4' if np_v >= 0 else '#fff5f5')
)

# ── JS data injection ────────────────────────────────────────────────────────
B_js = json.dumps([{
    'name':          b['name'],
    'name_ar':       b.get('name_ar', ''),
    'color':         b.get('color', '#2ba9ed'),
    'q1_revenue':    b['q1_revenue'],
    'q1_net_revenue':b['q1_net_revenue'],
    'q1_gross_profit':b['q1_gross_profit'],
    'q1_gross_margin':b['q1_gross_margin'],
    'q1_opex':       b['q1_opex'],
    'q1_salaries':   b['q1_salaries'],
    'q1_rent':       b['q1_rent'],
    'q1_delivery_comm':b['q1_delivery_comm'],
    'q1_royalty':    b['q1_royalty'],
    'q1_marketing':  b['q1_marketing'],
    'q1_net_profit': b['q1_net_profit'],
    'q1_net_margin': b['q1_net_margin'],
    'q1_txn':        b['q1_txn'],
    'monthly':       {m: b['monthly'].get(m, {}) for m in ALL_M},
} for b in B], ensure_ascii=True)

DA_js = json.dumps(DA, ensure_ascii=True)
PT_js = json.dumps(dict(list(sorted(PT.items(), key=lambda x: -x[1]))[:8]), ensure_ascii=True)
ME_js = json.dumps(ME, ensure_ascii=True)
MONTHS_js = json.dumps({m: ae(MN_AR.get(m, m)) for m in ALL_M}, ensure_ascii=True)

# ── Executive summary text ────────────────────────────────────────────────────
EXC = (
    ae('حقق الربع الأول 2026 إيرادات إجمالية ') +
    '<strong>' + sar(T['rev']) + '</strong>' + ae(' (صافي: ') + '<strong>' + sar(T['net']) + '</strong>' + ae(') عبر 6 فروع.') +
    '<br>' +
    ae('الربح الخام: ') + '<strong style="color:#22c55e">' + sar(T['gp']) + '</strong>' +
    ae(' (') + pct(gm) + ae(') | مصاريف Odoo الفعلية: ') +
    '<strong style="color:#e92c30">' + sar(OPEX_ODOO) + '</strong>' +
    '<br>' +
    '<strong style="font-size:15px;color:' + npclr(T['np']) + '">' +
    ae('صافي الربح: ') + sar(T['np']) + ' (' + pct(nm) + ')' +
    '</strong><br><br>' +
    '<strong>' + ae('🏆 أفضل فرع: ') + '</strong>' +
    ae(best.get('name_ar', '')) + ' (' + sar(best.get('q1_net_profit', 0)) + ', ' + pct(best.get('q1_net_margin', 0)) + ')' +
    '<br>' +
    '<strong>' + ae('⚠️ الفرع الأكثر ضغطاً: ') + '</strong>' +
    ae(worst.get('name_ar', '')) + ' (' + sar(worst.get('q1_net_profit', 0)) + ', ' + pct(worst.get('q1_net_margin', 0)) + ')' +
    '<br><br>' +
    ae('التوصيل: ') + '<strong>' + sar(T['del_total']) + '</strong>' +
    ae(' إيرادات | ') + '<strong>' + sar(T['del_comm']) + '</strong>' + ae(' عمولات | صافي: ') +
    '<strong style="color:#22c55e">' + sar(T['del_net']) + '</strong>' +
    '<br>' +
    ae('المعاملات الكلية: ') + '<strong>' + nfmt(T['txn']) + ae(' طلب') + '</strong>' +
    ae(' | متوسط الفاتورة: ') + '<strong>' + sar(T['avg_ticket']) + '</strong>'
)

NOTES = (
    ae('• الإيرادات من Odoo POS — دقيقة 100%') + '<br>' +
    ae('• بيانات المصاريف: مبنية على نسب أبريل 2026 الفعلية (Excel) × 3 أشهر') + '<br>' +
    ae('• مصاريف Odoo (') + sar(OPEX_ODOO) + ae(') من القيود المحاسبية — بيانات Q1 2026 مكتملة') + '<br>' +
    ae('• لتوزيع دقيق بالفرع: يحتاج إدخال الحسابات التحليلية لكل فرع في Odoo') + '<br>' +
    ae('• آخر شهر بيانات مكتملة: مارس 2026 | أبريل ناقص 75% | مايو شبه فارغ')
)

print('HTML sections built OK')
print('Q1 Rev:', T['rev'], '| GP:', T['gp'], '| NP:', T['np'])


# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#f0f2f7;--surface:#fff;--surface2:#f8fafc;--nav:#0f172a;--nav2:#1e293b;--blue:#2ba9ed;--blue-lt:#eff8ff;--red:#e92c30;--green:#16a34a;--amber:#d97706;--purple:#7c3aed;--text:#0f172a;--text2:#475569;--text3:#94a3b8;--border:#e2e8f0;--border2:#f1f5f9;--sh:0 1px 3px rgba(0,0,0,.08);--sh-md:0 4px 6px -1px rgba(0,0,0,.08);--r:12px;--rs:8px}
html,body{overflow-x:hidden;width:100%}
body{font-family:'Tajawal',sans-serif;background:var(--bg);color:var(--text);direction:rtl;font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased}
/* NAV */
.bar{background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:0 24px;height:66px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200;box-shadow:0 4px 20px rgba(0,0,0,.3)}
.lw{display:flex;align-items:center;gap:14px}
.logo-b{background:#2ba9ed;border-radius:10px;padding:5px 10px;display:flex;align-items:center}
.logo-b img{height:36px;width:auto}
.t1{font-size:14px;font-weight:700;color:#fff;line-height:1.3}
.t2{font-size:11px;color:rgba(255,255,255,.5);margin-top:2px}
.badge{font-size:11px;background:rgba(43,169,237,.25);color:#7dd3fc;border:1px solid rgba(43,169,237,.35);padding:4px 14px;border-radius:20px;font-weight:600}
.upd{font-size:10px;color:rgba(255,255,255,.35)}
/* LAYOUT */
.wrap{padding:20px 24px;max-width:1560px;margin:0 auto}
.phdr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.phdr h2{font-size:19px;font-weight:800;letter-spacing:-.4px}
.phdr p{font-size:12px;color:var(--text2);margin-top:2px}
.per{font-size:11px;color:#2ba9ed;background:#eff8ff;border:1px solid #bae6fd;padding:5px 14px;border-radius:20px;font-weight:700}
/* GRIDS */
.kg5{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:12px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.g3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}
/* KPI CARD */
.kc{background:var(--surface);border-radius:var(--r);padding:18px 20px;box-shadow:var(--sh);border:1px solid var(--border2);position:relative;overflow:hidden;transition:transform .15s}
.kc::before{content:'';position:absolute;top:0;right:0;left:0;height:3px;background:var(--accent,#2ba9ed)}
.kc:hover{transform:translateY(-2px);box-shadow:var(--sh-md)}
.kl{font-size:9px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px}
.kv{font-size:22px;font-weight:800;line-height:1;font-family:'Cairo','Tajawal',monospace;letter-spacing:-.5px}
.ks{font-size:11px;color:var(--text2);margin-top:6px;font-weight:500}
/* TABS */
.tabs{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:5px;display:flex;gap:4px;margin-bottom:20px;overflow-x:auto;flex-wrap:wrap;box-shadow:var(--sh)}
.tab{padding:9px 16px;background:none;border:none;cursor:pointer;font-size:12px;color:var(--text2);border-radius:var(--rs);font-family:'Tajawal',sans-serif;white-space:nowrap;font-weight:600;transition:all .15s}
.tab:hover{background:var(--bg);color:var(--text)}
.tab.on{background:#2ba9ed;color:#fff;box-shadow:0 2px 8px rgba(43,169,237,.4)}
/* CARD */
.card{background:var(--surface);border:1px solid var(--border2);border-radius:var(--r);padding:18px 20px;margin-bottom:14px;box-shadow:var(--sh)}
.st{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.st::after{content:'';flex:1;height:1px;background:var(--border)}
.cw{position:relative;width:100%}
/* TABLE */
table.dt{width:100%;border-collapse:collapse;font-size:12.5px}
table.dt th{padding:9px 11px;font-size:9px;font-weight:700;color:var(--text3);border-bottom:2px solid var(--border);text-align:right;background:var(--surface2);text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}
table.dt td{padding:9px 11px;border-bottom:1px solid var(--border2);vertical-align:middle}
table.dt tbody tr:last-child td{border-bottom:none}
table.dt tbody tr:hover td{background:#f8faff}
/* TAGS */
.tag{display:inline-flex;align-items:center;font-size:10px;padding:3px 8px;border-radius:6px;font-weight:700;font-family:'Cairo','Tajawal',monospace;white-space:nowrap}
.tg{background:#dcfce7;color:#15803d}
.tr{background:#fee2e2;color:#b91c1c}
.tn{background:var(--border2);color:var(--text2)}
.nm{font-family:'Cairo','Tajawal',monospace;font-weight:600;white-space:nowrap}
/* WATERFALL */
.wf{display:flex;flex-direction:column;gap:5px;margin-top:8px}
.wf-row{display:flex;align-items:center;gap:12px;padding:9px 12px;border-radius:8px;background:var(--surface2)}
.wf-label{min-width:170px;font-size:12px;font-weight:600;color:var(--text2);flex-shrink:0}
.wf-bar-wrap{flex:1;height:8px;background:var(--border);border-radius:4px;overflow:hidden}
.wf-bar{height:100%;border-radius:4px;transition:width .5s}
.wf-val{min-width:95px;text-align:left;font-family:'Cairo',monospace;font-weight:700;font-size:12px;flex-shrink:0}
/* INFO BANNERS */
.info-banner{border-radius:8px;padding:10px 14px;font-size:11px;font-weight:600;margin-bottom:12px}
.info-green{background:#f0fdf4;border:1px solid #bbf7d0;color:#166534}
.info-amber{background:#fffbeb;border:1px solid #fde68a;color:#92400e}
/* RESPONSIVE */
@media(max-width:1024px){.kg5{grid-template-columns:repeat(3,1fr)}.g3{grid-template-columns:1fr 1fr}.card{overflow-x:auto}}
@media(max-width:768px){.kg5{grid-template-columns:1fr 1fr;gap:9px}.g2,.g3{grid-template-columns:1fr}.bar{height:56px;padding:0 12px}.logo-b img{height:28px}.t2,.upd{display:none}.wrap{padding:12px 10px}.kv{font-size:18px}.tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}.tab{padding:7px 4px;font-size:9px;text-align:center}.card{overflow-x:auto}}
@media(max-width:480px){.kg5{grid-template-columns:1fr 1fr}.kv{font-size:16px}}
"""

# ══════════════════════════════════════════════════════════════════════════════
# JavaScript
# ══════════════════════════════════════════════════════════════════════════════
JS_TEMPLATE = """
var B=__B__,DA=__DA__,PT=__PT__,ME=__ME__,MO=__MO__,CH={};
function fmt(v){var s=v<0?'-':'';v=Math.abs(v);if(v>=1e6)return s+'SAR '+(v/1e6).toFixed(1)+'M';if(v>=1e3)return s+'SAR '+(v/1e3).toFixed(1)+'K';return s+'SAR '+Math.round(v);}
Chart.defaults.font.family="'Cairo','Tajawal',sans-serif";
Chart.defaults.color="#94a3b8";
Chart.defaults.plugins.tooltip.backgroundColor="#0f172a";
Chart.defaults.plugins.tooltip.titleColor="#fff";
Chart.defaults.plugins.tooltip.bodyColor="#94a3b8";
Chart.defaults.plugins.tooltip.padding=10;
Chart.defaults.plugins.tooltip.cornerRadius=8;

function sw(n){
  for(var i=0;i<9;i++){
    var t=document.getElementById('t'+i),p=document.getElementById('p'+i);
    if(t)t.className='tab'+(i===n?' on':'');
    if(p)p.style.display=(i===n)?'block':'none';
  }
  if(n===0)setTimeout(dOv,60);
  else if(n===1)setTimeout(dPnl,60);
  else if(n===2)setTimeout(dBr,60);
  else if(n===4)setTimeout(dExp,60);
  else if(n===5)setTimeout(dDel,60);
  else if(n===7)setTimeout(dPay,60);
}
function mk(id,cfg){var el=document.getElementById(id);if(!el)return;if(CH[id])CH[id].destroy();try{CH[id]=new Chart(el,cfg);}catch(e){console.error(id,e);}}

/* OVERVIEW */
function dOv(){
  if(CH.ch_rev_ov)return;
  var Bsorted=B.slice().sort(function(a,b){return b.q1_revenue-a.q1_revenue;});
  var labels=Bsorted.map(function(b){return b.name_ar||b.name;});
  mk('ch_rev_ov',{type:'bar',data:{labels:labels,datasets:[{label:'Revenues',data:Bsorted.map(function(b){return b.q1_revenue;}),backgroundColor:Bsorted.map(function(b){return b.color;}),borderRadius:7,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+fmt(c.raw);}}}},scales:{x:{ticks:{color:'#64748b'},grid:{display:false}},y:{ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
  var npSorted=B.slice().sort(function(a,b){return b.q1_net_profit-a.q1_net_profit;});
  mk('ch_np_ov',{type:'bar',data:{labels:npSorted.map(function(b){return b.name_ar||b.name;}),datasets:[{label:'Net Profit',data:npSorted.map(function(b){return b.q1_net_profit;}),backgroundColor:npSorted.map(function(b){return b.q1_net_profit>=0?'rgba(22,163,74,.85)':'rgba(220,38,38,.85)';}),borderRadius:7,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return ' '+fmt(c.raw);}}}},scales:{x:{ticks:{color:'#64748b'},grid:{display:false}},y:{ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
}

/* P&L Monthly Trend */
function dPnl(){
  if(CH.ch_pnl)return;
  var months=['2026-01','2026-02','2026-03'];
  var labels=months.map(function(m){return MO[m]||m;});
  var revArr=months.map(function(m){return B.reduce(function(s,b){return s+(b.monthly&&b.monthly[m]?b.monthly[m].net_revenue||0:0);},0);});
  var gpArr =months.map(function(m){return B.reduce(function(s,b){return s+(b.monthly&&b.monthly[m]?b.monthly[m].gross_profit||0:0);},0);});
  var meArr =months.map(function(m){return ME[m]?ME[m].total:0;});
  var npArr =months.map(function(m,i){return gpArr[i]-meArr[i];});
  mk('ch_pnl',{type:'bar',data:{labels:labels,datasets:[
    {label:'صافي الإيرادات',data:revArr,backgroundColor:'rgba(43,169,237,.55)',borderRadius:6,borderSkipped:false},
    {label:'الربح الخام',data:gpArr,backgroundColor:'rgba(22,163,74,.6)',borderRadius:6,borderSkipped:false},
    {label:'المصاريف (Odoo)',data:meArr,backgroundColor:'rgba(220,38,38,.55)',borderRadius:6,borderSkipped:false},
    {label:'صافي الربح',data:npArr,type:'line',fill:false,borderColor:'#0f172a',borderWidth:2.5,pointRadius:6,pointBackgroundColor:npArr.map(function(v){return v>=0?'#16a34a':'#dc2626';}),pointBorderColor:'#fff',pointBorderWidth:2}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{color:'#475569',font:{size:10},padding:10}}},scales:{x:{ticks:{color:'#64748b'},grid:{display:false}},y:{ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
}

/* Branch P&L */
function dBr(){
  if(CH.ch_br)return;
  var Bsort=B.slice().sort(function(a,b){return b.q1_net_profit-a.q1_net_profit;});
  var labels=Bsort.map(function(b){return b.name_ar||b.name;});
  mk('ch_br',{type:'bar',data:{labels:labels,datasets:[
    {label:'الربح الخام',data:Bsort.map(function(b){return b.q1_gross_profit;}),backgroundColor:'rgba(43,169,237,.55)',borderRadius:5,borderSkipped:false},
    {label:'المصاريف التشغيلية',data:Bsort.map(function(b){return b.q1_opex;}),backgroundColor:'rgba(220,38,38,.5)',borderRadius:5,borderSkipped:false},
    {label:'صافي الربح',data:Bsort.map(function(b){return b.q1_net_profit;}),type:'line',fill:false,borderColor:'#0f172a',borderWidth:2,pointRadius:7,pointBackgroundColor:Bsort.map(function(b){return b.q1_net_profit>=0?'#16a34a':'#dc2626';}),pointBorderColor:'#fff',pointBorderWidth:2}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{color:'#475569',font:{size:10},padding:10}}},scales:{x:{ticks:{color:'#64748b'},grid:{display:false}},y:{ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
  mk('ch_br_share',{type:'doughnut',data:{labels:B.map(function(b){return b.name_ar||b.name;}),datasets:[{data:B.map(function(b){return b.q1_revenue;}),backgroundColor:B.map(function(b){return b.color;}),borderWidth:3,borderColor:'#fff',hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,cutout:'62%',plugins:{legend:{position:'bottom',labels:{color:'#475569',font:{size:10},boxWidth:10,padding:8}},tooltip:{callbacks:{label:function(c){var t=B.reduce(function(s,b){return s+b.q1_revenue;},0);return ' '+fmt(c.raw)+' ('+((c.raw/t)*100).toFixed(1)+'%)';}}}}}});
  /* Expense composition per branch — stacked bar */
  var Bexp=B.slice().sort(function(a,b){return b.q1_opex-a.q1_opex;});
  var expLabels=Bexp.map(function(b){return b.name_ar||b.name;});
  mk('ch_br_exp',{type:'bar',data:{labels:expLabels,datasets:[
    {label:'Salaries',data:Bexp.map(function(b){return b.q1_salaries;}),backgroundColor:'rgba(139,92,246,.8)',borderRadius:4,borderSkipped:false},
    {label:'Rent',data:Bexp.map(function(b){return b.q1_rent;}),backgroundColor:'rgba(245,158,11,.8)',borderRadius:4,borderSkipped:false},
    {label:'Delivery',data:Bexp.map(function(b){return b.q1_delivery_comm;}),backgroundColor:'rgba(220,38,38,.7)',borderRadius:4,borderSkipped:false},
    {label:'Royalty',data:Bexp.map(function(b){return b.q1_royalty;}),backgroundColor:'rgba(6,182,212,.8)',borderRadius:4,borderSkipped:false},
    {label:'Marketing',data:Bexp.map(function(b){return b.q1_marketing;}),backgroundColor:'rgba(236,72,153,.8)',borderRadius:4,borderSkipped:false}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{color:'#475569',font:{size:10},padding:10}}},scales:{x:{stacked:true,ticks:{color:'#64748b'},grid:{display:false}},y:{stacked:true,ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
}

/* Monthly Trend */
function dTrend(){
  if(CH.ch_trend)return;
  var months=['2025-10','2025-11','2025-12','2026-01','2026-02','2026-03'];
  var labels=months.map(function(m){return MO[m]||m;});
  mk('ch_trend',{type:'line',data:{labels:labels,datasets:B.map(function(b){return{label:b.name_ar||b.name,data:months.map(function(m){return b.monthly&&b.monthly[m]?b.monthly[m].revenue||0:0;}),borderColor:b.color,backgroundColor:b.color+'22',borderWidth:2.5,pointRadius:4,pointBackgroundColor:b.color,fill:false,tension:.3};})},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{color:'#475569',font:{size:10},padding:8,boxWidth:10}}},scales:{x:{ticks:{color:'#64748b'},grid:{display:false}},y:{ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
}

/* Expenses */
function dExp(){
  if(CH.ch_exp)return;
  var lbs=['رواتب','إيجار','&#1604;&#1608;&#1576;&#1585;&#1610;&#1601;','امتياز','حكومية','تأمين','كهرباء','بنكية','أخرى'];
  var vals=[230985,520182,233936,93873,56375,41461,14785,12612,418003];
  var clrs=['#8b5cf6','#f59e0b','#2ba9ed','#06b6d4','#ec4899','#e92c30','#22c55e','#94a3b8','#64748b'];
  mk('ch_exp',{type:'doughnut',data:{labels:lbs,datasets:[{data:vals,backgroundColor:clrs,borderWidth:3,borderColor:'#fff',hoverOffset:6}]},options:{responsive:true,maintainAspectRatio:false,cutout:'55%',plugins:{legend:{position:'right',labels:{color:'#475569',font:{size:10},boxWidth:10,padding:8}},tooltip:{callbacks:{label:function(c){return ' '+fmt(c.raw)+' ('+((c.raw/1622212)*100).toFixed(1)+'%)';}}}}}});
}

/* Delivery */
function dDel(){
  if(CH.ch_del)return;
  var keys=Object.keys(DA);var totals=keys.map(function(k){return DA[k].total;});
  var clrs=['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#10b981','#94a3b8','#0ea5e9','#f97316'];
  mk('ch_del',{type:'doughnut',data:{labels:keys,datasets:[{data:totals,backgroundColor:clrs,borderWidth:3,borderColor:'#fff',hoverOffset:6}]},options:{responsive:true,maintainAspectRatio:false,cutout:'55%',plugins:{legend:{position:'right',labels:{color:'#475569',font:{size:10},boxWidth:10,padding:8}},tooltip:{callbacks:{label:function(c){return ' '+fmt(c.raw);}}}}}});
  mk('ch_del_net',{type:'bar',data:{labels:keys,datasets:[
    {label:'الإيرادات',data:totals,backgroundColor:'rgba(43,169,237,.55)',borderRadius:5,borderSkipped:false},
    {label:'العمولة',data:keys.map(function(k){return DA[k].commission;}),backgroundColor:'rgba(220,38,38,.6)',borderRadius:5,borderSkipped:false},
    {label:'الصافي',data:keys.map(function(k){return DA[k].net;}),backgroundColor:'rgba(22,163,74,.7)',borderRadius:5,borderSkipped:false}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{color:'#475569',font:{size:10},padding:10}}},scales:{x:{ticks:{color:'#64748b',font:{size:10}},grid:{display:false}},y:{ticks:{color:'#94a3b8',callback:function(v){return fmt(v);}},grid:{color:'rgba(226,232,240,.5)'}}}}});
}

/* Payments */
function dPay(){
  if(CH.ch_pay)return;
  var keys=Object.keys(PT);var vals=keys.map(function(k){return PT[k];});
  var clrs=['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#94a3b8'];
  mk('ch_pay',{type:'doughnut',data:{labels:keys,datasets:[{data:vals,backgroundColor:clrs,borderWidth:3,borderColor:'#fff',hoverOffset:6}]},options:{responsive:true,maintainAspectRatio:false,cutout:'55%',plugins:{legend:{position:'right',labels:{color:'#475569',font:{size:10},boxWidth:10,padding:8}},tooltip:{callbacks:{label:function(c){var t=vals.reduce(function(a,b){return a+b;},0);return ' '+fmt(c.raw)+' ('+((c.raw/t)*100).toFixed(1)+'%)';}}}}}}); 
}
dOv();
"""

JS = (JS_TEMPLATE
    .replace('__B__',  B_js)
    .replace('__DA__', DA_js)
    .replace('__PT__', PT_js)
    .replace('__ME__', ME_js)
    .replace('__MO__', MONTHS_js))

print('JS built OK, len:', len(JS))

# ══════════════════════════════════════════════════════════════════════════════
# Assemble HTML — sections joined cleanly (no f-strings in templates)
# ══════════════════════════════════════════════════════════════════════════════
MN_LABEL = ae(D.get('report_month', ''))
DATA_SRC  = ae(D.get('data_source', '')[:50])
PERIOD    = ae(D.get('report_period', ''))
UPDATED   = ae(D.get('updated', ''))

LOGO_SRC = ('data:image/png;base64,' + LOGO) if LOGO else ''

# Tab 0 — Overview
T0 = """
<div class="g2">
  <div class="card">
    <div class="st">REVENUES_BY_BRANCH</div>
    <div class="cw"><canvas id="ch_rev_ov" style="height:270px"></canvas></div>
  </div>
  <div class="card">
    <div class="st">NET_PROFIT_BY_BRANCH</div>
    <div class="cw"><canvas id="ch_np_ov" style="height:270px"></canvas></div>
  </div>
</div>
<div class="card">
  <div class="st">BRANCH_SUMMARY</div>
  <table class="dt">
    <thead><tr>TH_OVERVIEW</tr></thead>
    <tbody>BRANCH_ROWS_OV</tbody>
  </table>
</div>
""".replace('REVENUES_BY_BRANCH', ae('الإيرادات Q1 بالفرع')
   ).replace('NET_PROFIT_BY_BRANCH', ae('صافي الربح/الخسارة Q1 بالفرع')
   ).replace('BRANCH_SUMMARY', ae('ملخص أداء الفروع — Q1 2026')
   ).replace('TH_OVERVIEW', th('الفرع','صافي الإيرادات','طلبات','ربح خام','هامش%','رواتب','إيجار','عمولة توصيل','رسوم امتياز','تسويق','إجمالي مصاريف','صافي الربح','هامش صافي')
   ).replace('BRANCH_ROWS_OV', BRANCH_ROWS)

# Tab 1 — P&L Waterfall
T1 = """
<div class="g2">
  <div class="card">
    <div class="st">PNL_STMT</div>
    <div class="wf">WATERFALL_ROWS</div>
  </div>
  <div class="card">
    <div class="st">MONTHLY_TREND</div>
    <div class="cw"><canvas id="ch_pnl" style="height:250px"></canvas></div>
    <div style="margin-top:14px">
      <table class="dt">
        <thead><tr>TH_MON_PNL</tr></thead>
        <tbody>MON_PNL_ROWS</tbody>
      </table>
    </div>
  </div>
</div>
""".replace('PNL_STMT', ae('قائمة الدخل — Q1 2026 (الشركة)')
   ).replace('WATERFALL_ROWS', WF_ROWS
   ).replace('MONTHLY_TREND', ae('الدخل والمصاريف الشهرية')
   ).replace('TH_MON_PNL', th('الشهر','الإيرادات+VAT','صافي','ربح خام','هامش%','مصاريف Odoo','صافي الربح','هامش صافي')
   ).replace('MON_PNL_ROWS', MON_PNL_ROWS)

# Tab 2 — Branch P&L
T2 = """
<div class="info-banner info-amber">NOTE_AMBER</div>
<div class="g2">
  <div class="card">
    <div class="st">GP_VS_EXP</div>
    <div class="cw"><canvas id="ch_br" style="height:280px"></canvas></div>
  </div>
  <div class="card">
    <div class="st">REV_SHARE</div>
    <div class="cw"><canvas id="ch_br_share" style="height:280px"></canvas></div>
  </div>
</div>
<div class="card">
  <div class="st">EXP_COMP</div>
  <div class="cw"><canvas id="ch_br_exp" style="height:220px"></canvas></div>
</div>
<div class="card">
  <div class="st">PNL_DETAIL</div>
  <table class="dt">
    <thead><tr>TH_BR_PNL</tr></thead>
    <tbody>BRANCH_ROWS_PNL</tbody>
  </table>
</div>
""".replace('NOTE_AMBER', ae('📋 الإيرادات من Odoo POS (دقيقة) | المصاريف مبنية على نسب أبريل 2026 الفعلية (Excel) × 3 أشهر — تقريبية')
   ).replace('GP_VS_EXP', ae('ربح خام ↔ مصاريف ↔ صافي ربح')
   ).replace('REV_SHARE', ae('حصة كل فرع من إيرادات Q1')
   ).replace('EXP_COMP', ae('تركيبة المصاريف لكل فرع')
   ).replace('PNL_DETAIL', ae('P&L تفصيلي بالفرع — Q1 2026')
   ).replace('TH_BR_PNL', th('الفرع','صافي الإيرادات','طلبات','ربح خام','هامش%','رواتب','إيجار','عمولة توصيل','رسوم امتياز','تسويق','إجمالي مصاريف','صافي الربح','هامش صافي')
   ).replace('BRANCH_ROWS_PNL', BRANCH_ROWS)

# Tab 3 — Monthly Revenue Trend
T3 = """
<div class="card">
  <div class="st">TREND_TITLE</div>
  <div class="cw"><canvas id="ch_trend" style="height:300px"></canvas></div>
</div>
<div class="card">
  <div class="st">REV_TABLE_TITLE</div>
  <table class="dt">
    <thead><tr>TH_MON_REV</tr></thead>
    <tbody>MON_REV_ROWS</tbody>
  </table>
</div>
""".replace('TREND_TITLE', ae('اتجاه الإيرادات الشهري (أكتوبر 2025 — مارس 2026)')
   ).replace('REV_TABLE_TITLE', ae('الإيرادات الشهرية لكل فرع (+VAT)')
   ).replace('TH_MON_REV', th('الفرع','أكتوبر','نوفمبر','ديسمبر','يناير 26','فبراير 26','مارس 26','إجمالي Q1','نمو Feb→Mar')
   ).replace('MON_REV_ROWS', MON_REV_ROWS)

# Tab 4 — Expenses
T4 = """
<div class="g2">
  <div class="card">
    <div class="st">EXP_CHART_TITLE</div>
    <div class="cw"><canvas id="ch_exp" style="height:300px"></canvas></div>
  </div>
  <div class="card">
    <div class="st">EXP_TABLE_TITLE</div>
    <table class="dt">
      <thead><tr>TH_EXP</tr></thead>
      <tbody>EXP_ROWS</tbody>
    </table>
  </div>
</div>
<div class="card">
  <div class="st">EXP_MONTHLY_TITLE</div>
  <table class="dt">
    <thead><tr>TH_MON_EXP</tr></thead>
    <tbody>MON_EXP_ROWS</tbody>
  </table>
</div>
""".replace('EXP_CHART_TITLE', ae('توزيع المصاريف التشغيلية Q1 (Odoo)')
   ).replace('EXP_TABLE_TITLE', ae('تفصيل المصاريف بالنسبة')
   ).replace('TH_EXP', th('البند','المبلغ Q1','% من الإجمالي','البار')
   ).replace('EXP_ROWS', EXP_ROWS
   ).replace('EXP_MONTHLY_TITLE', ae('المصاريف الشهرية (Odoo — بيانات مكتملة)')
   ).replace('TH_MON_EXP', th('الشهر','إجمالي المصاريف','الرواتب','الإيجارات','لوبريف (غذاء)','رسوم الامتياز')
   ).replace('MON_EXP_ROWS',
       ''.join(
           '<tr><td><strong>%s</strong></td><td class="nm" style="color:#e92c30"><strong>%s</strong></td>%s</tr>' % (
               ae(MN_AR.get(m, m)), sar(ME[m]['total']),
               ''.join('<td class="nm">%s</td>' % sar(ME[m].get(k, 0))
                       for k in ['salaries','rent','luopreev','royalty'])
           )
           for m in Q1M if m in ME
       ) +
       '<tr style="background:var(--surface2);font-weight:700"><td><strong>%s</strong></td><td class="nm" style="color:#e92c30"><strong>%s</strong></td>%s</tr>' % (
           ae('الإجمالي'), sar(sum(ME[m]['total'] for m in Q1M if m in ME)),
           ''.join('<td class="nm"><strong>%s</strong></td>' % sar(sum(ME[m].get(k,0) for m in Q1M if m in ME))
                   for k in ['salaries','rent','luopreev','royalty'])
       )
   )

# Tab 5 — Delivery
del_kpis = (
    kc('دخل التوصيل Q1',   sar(T['del_total']),  '%s %s' % (nfmt(T['del_orders']), ae('طلب')),  '#2ba9ed') +
    kc('العمولات المدفوعة', sar(T['del_comm']),   pct(T['del_comm']/T['del_total']*100 if T['del_total'] else 0) + ae(' من الدخل'), '#e92c30', '#e92c30') +
    kc('الصافي المستحق',    sar(T['del_net']),    pct(T['del_net']/T['del_total']*100 if T['del_total'] else 0) + ae(' من الدخل'), '#22c55e', '#22c55e')
)
T5 = """
<div class="g3">DEL_KPIS</div>
<div class="g2">
  <div class="card">
    <div class="st">DEL_SHARE</div>
    <div class="cw"><canvas id="ch_del" style="height:280px"></canvas></div>
  </div>
  <div class="card">
    <div class="st">DEL_NET_CHART</div>
    <div class="cw"><canvas id="ch_del_net" style="height:280px"></canvas></div>
  </div>
</div>
<div class="card">
  <div class="st">DEL_TABLE</div>
  <table class="dt">
    <thead><tr>TH_DEL</tr></thead>
    <tbody>DEL_ROWS</tbody>
  </table>
</div>
""".replace('DEL_KPIS', del_kpis
   ).replace('DEL_SHARE', ae('حصة التطبيقات من إيرادات التوصيل')
   ).replace('DEL_NET_CHART', ae('الإيرادات vs العمولة vs الصافي')
   ).replace('DEL_TABLE', ae('تفصيل رسوم تطبيقات التوصيل — Q1 2026')
   ).replace('TH_DEL', th('التطبيق','الطلبات','الإيرادات','هيكل الرسوم','الرسوم','نسبة فعلية','الصافي لك')
   ).replace('DEL_ROWS', DEL_ROWS)

# Tab 6 — Products
T6 = """
<div class="card">
  <div class="st">PROD_TITLE</div>
  <table class="dt">
    <thead><tr>TH_PROD</tr></thead>
    <tbody>PROD_ROWS</tbody>
  </table>
</div>
""".replace('PROD_TITLE', ae('أفضل 10 منتجات Q1 2026')
   ).replace('TH_PROD', th('#','المنتج','الكمية','الإيرادات (ex-VAT)','الحصة النسبية')
   ).replace('PROD_ROWS', PROD_ROWS)

# Tab 7 — Payments
T7 = """
<div class="g2">
  <div class="card">
    <div class="st">PAY_CHART_TITLE</div>
    <div class="cw"><canvas id="ch_pay" style="height:300px"></canvas></div>
  </div>
  <div class="card">
    <div class="st">PAY_TABLE_TITLE</div>
    <table class="dt">
      <thead><tr>TH_PAY</tr></thead>
      <tbody>PAY_ROWS</tbody>
      <tfoot>
        <tr>
          <td><strong>TOTAL_LABEL</strong></td>
          <td class="nm"><strong>TOTAL_VAL</strong></td>
          <td><span class="tag tn">100%</span></td>
        </tr>
      </tfoot>
    </table>
  </div>
</div>
""".replace('PAY_CHART_TITLE', ae('توزيع طرق الدفع Q1 2026')
   ).replace('PAY_TABLE_TITLE', ae('تفصيل طرق الدفع')
   ).replace('TH_PAY', th('طريقة الدفع','المبلغ Q1','النسبة')
   ).replace('PAY_ROWS', PAY_ROWS
   ).replace('TOTAL_LABEL', ae('الإجمالي')
   ).replace('TOTAL_VAL', sar(PAY_TOTAL))

# Tab 8 — Final Report
T8 = """
<div class="card">
  <div class="st">FINAL_TITLE</div>
  <div style="padding:8px 0;line-height:2.1;font-size:13px;color:#475569">EXEC_SUMMARY</div>
</div>
<div class="info-banner info-amber" style="margin-top:0">
  <strong>NOTES_TITLE</strong><br>
  <div style="margin-top:8px;line-height:1.9">NOTES_BODY</div>
</div>
""".replace('FINAL_TITLE', ae('الملخص التنفيذي — Q1 2026')
   ).replace('EXEC_SUMMARY', EXC
   ).replace('NOTES_TITLE', ae('📋 ملاحظات منهجية')
   ).replace('NOTES_BODY', NOTES)

# ── Assemble full HTML ────────────────────────────────────────────────────────
def pane(id_n, content, visible=False):
    display = 'block' if visible else 'none'
    return '<div id="p%d" style="display:%s">%s</div>' % (id_n, display, content)

def tab_btn(id_n, icon, label, active=False):
    cls = 'tab on' if active else 'tab'
    return '<button id="t%d" class="%s" onclick="sw(%d)">%s %s</button>' % (
        id_n, cls, id_n, icon, ae(label))

TABS = (
    tab_btn(0, '&#128202;', 'نظرة عامة', True) +
    tab_btn(1, '&#128181;', 'قائمة الدخل') +
    tab_btn(2, '&#127968;', 'P&L الفروع') +
    tab_btn(3, '&#128200;', 'الإيرادات الشهرية') +
    tab_btn(4, '&#128178;', 'المصاريف') +
    tab_btn(5, '&#128663;', 'التوصيل') +
    tab_btn(6, '&#127881;', 'المنتجات') +
    tab_btn(7, '&#128180;', 'طرق الدفع') +
    tab_btn(8, '&#127942;', 'التقرير النهائي')
)

HTML = ('<!DOCTYPE html>\n'
    '<html lang="ar" dir="rtl">\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    '<title>' + ae('لوحة التحليل المالي - شركة بوصلة التميز التجارية') + '</title>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">\n'
    '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n'
    '<style>' + CSS + '</style>\n'
    '</head>\n'
    '<body>\n'
    '<div class="bar">\n'
    '  <div class="lw">\n'
    '    <div class="logo-b"><img src="' + LOGO_SRC + '" alt="COE" onerror="this.style.display=\'none\'"></div>\n'
    '    <div>\n'
    '      <div class="t1">' + ae('لوحة التحليل المالي - شركة بوصلة التميز التجارية') + '</div>\n'
    '      <div class="t2">Odoo POS | 6 ' + ae('فروع') + ' | ' + DATA_SRC + '</div>\n'
    '    </div>\n'
    '  </div>\n'
    '  <div style="display:flex;align-items:center;gap:10px">\n'
    '    <span class="badge">&#128197; ' + MN_LABEL + '</span>\n'
    '    <span class="upd">' + UPDATED + '</span>\n'
    '  </div>\n'
    '</div>\n'
    '<div class="wrap">\n'
    '  <div class="phdr">\n'
    '    <div>\n'
    '      <h2>' + ae('التحليل المالي - ') + MN_LABEL + '</h2>\n'
    '      <p>' + PERIOD + ' | 6 ' + ae('فروع | بيانات مكتملة حتى مارس 2026') + '</p>\n'
    '    </div>\n'
    '    <span class="per">&#128197; ' + ae('Q1 2026') + '</span>\n'
    '  </div>\n'
    '  <div class="kg5">' + KPIS1 + '</div>\n'
    '  <div class="info-banner info-green" style="margin:-6px 0 12px">\n'
    '    &#9432; ' + ae('الإيرادات: Odoo POS (دقيقة 100%) | المصاريف: بيانات Odoo المحاسبية المكتملة Q1 2026') + '\n'
    '  </div>\n'
    '  <div class="kg5">' + KPIS2 + '</div>\n'
    '  <div class="tabs">' + TABS + '</div>\n'
    + pane(0, T0, True)
    + pane(1, T1)
    + pane(2, T2)
    + pane(3, T3)
    + pane(4, T4)
    + pane(5, T5)
    + pane(6, T6)
    + pane(7, T7)
    + pane(8, T8)
    + '\n</div>\n'
    '<script>\n' + JS + '\n</script>\n'
    '</body>\n</html>'
)

# ── Write output ──────────────────────────────────────────────────────────────
out_path = os.path.join(REPO, 'index.html')
# Convert any non-ASCII chars to HTML entities
import re
def to_ascii(s):
    out = []
    for c in s:
        if ord(c) > 127:
            out.append('&#%d;' % ord(c))
        else:
            out.append(c)
    return ''.join(out)

HTML_ASCII = to_ascii(HTML)
with open(out_path, 'w', encoding='ascii') as f:
    f.write(HTML_ASCII)

# Verify
import subprocess
js_blob = JS
with open('/tmp/check.js', 'w') as f:
    f.write(js_blob)
r = subprocess.run(['node', '--check', '/tmp/check.js'], capture_output=True, text=True)
js_ok = r.returncode == 0

print('HTML size   :', len(HTML), 'chars')
print('ASCII clean :', all(ord(c) < 128 for c in HTML_ASCII))
print('JS syntax   :', 'OK' if js_ok else 'ERROR: ' + r.stderr[:200])
