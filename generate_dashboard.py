import json

LOGO_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCAIbAjUDASIAAhEBAxEB/8QAHAABAAMBAQEBAQAAAAAAAAAAAAUGBwgEAgMB/8QARBAAAgEDAQUCBwwKAwEBAQAAAAECAwQFBhEhMUFRBxMSYYGUscHhFBciNkJVcXN0obLRCBUWNDVWYpHS4jNDUjKS8P/EABWBAQEBAAAAAAAAAAAAAAAAAAAAAA=="

def num(n):
    if abs(n) >= 1e6: return f"{n/1e6:.2f}M"
    if abs(n) >= 1e3: return f"{n/1e3:.1f}K"
    return f"{round(n):,}"

def sar(n): return f"ر.س {num(n)}"
def pct(n): return f"{float(n):.1f}%"
def arrow(v): return "&#9650;" if v >= 0 else "&#9660;"
def tag_cls(v): return "tg" if v >= 0 else "tr"
def dt_tag(v): return f'<span class="tag {tag_cls(v)}">{arrow(v)} {abs(float(v)):.1f}%</span>'

def build_html(data):
    B = data.get('branches', [])
    YB = data.get('ytd_branches', [])
    prods = data.get('products', [])
    hourly = data.get('hourly', [0]*24)
    daily = data.get('daily', [0]*7)
    pay_totals = data.get('payment_totals', {})
    delivery = data.get('delivery_apps', {})
    delivery_ytd = data.get('delivery_ytd', {})
    expenses = data.get('expenses', {})
    expenses_ytd = data.get('expenses_ytd', {})

    total_rev = sum(b['total'] for b in B)
    total_gp  = sum(b.get('gross_profit_real', b['total']*0.77) for b in B)
    total_txn = sum(b.get('total_txn', 0) for b in B)
    avg_ticket = round(total_rev/total_txn, 1) if total_txn else 0

    ytd_rev = sum(b['total'] for b in YB)
    ytd_gp  = sum(b.get('gross_profit_real', b['total']*0.77) for b in YB)
    ytd_txn = sum(b.get('total_txn', 0) for b in YB)

    best_branch = B[0]['name'] if B else '-'

    DAYS = ['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت']
    COLORS = ['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#10b981']

    # ── KPI Cards ──────────────────────────────────────────────
    def kpi_card(label, value, sub, accent):
        return f'''<div class="kc" style="border-top:3px solid {accent}">
<div class="kl">{label}</div>
<div class="kv">{value}</div>
<div class="ks">{sub}</div>
</div>'''

    kpis = ''.join([
        kpi_card('إجمالي الإيرادات', sar(total_rev), f'{len(B)} فروع', '#2ba9ed'),
        kpi_card('إجمالي الأرباح', sar(total_gp), f'{pct(total_gp/total_rev*100) if total_rev else "0%"} هامش', '#22c55e'),
        kpi_card('إجمالي المعاملات', num(total_txn), 'طلب', '#f59e0b'),
        kpi_card('متوسط الفاتورة', sar(avg_ticket), 'لكل طلب', '#8b5cf6'),
        kpi_card('أفضل فرع', best_branch, sar(B[0]['total']) if B else '-', '#e92c30'),
    ])

    # ── YTD KPI Cards ──────────────────────────────────────────
    ytd_kpis = ''.join([
        kpi_card('إيرادات YTD', sar(ytd_rev), f'{data.get("ytd_from","")} - {data.get("ytd_to","")}', '#2ba9ed'),
        kpi_card('أرباح YTD', sar(ytd_gp), f'{pct(ytd_gp/ytd_rev*100) if ytd_rev else "0%"} هامش', '#22c55e'),
        kpi_card('معاملات YTD', num(ytd_txn), 'طلب', '#f59e0b'),
        kpi_card('متوسط الفاتورة YTD', sar(round(ytd_rev/ytd_txn,1) if ytd_txn else 0), 'لكل طلب', '#8b5cf6'),
    ])

    # ── Branch Overview Table ──────────────────────────────────
    branch_rows = ''
    for i,b in enumerate(B):
        c = COLORS[i%len(COLORS)]
        qoq = b.get('qoq', 0)
        rm = b.get('gross_margin_real', 77)
        branch_rows += f'''<tr>
<td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{c};margin-left:8px"></span><strong>{b['name']}</strong></td>
<td class="num">{sar(b['total'])}</td>
<td class="num">{num(b.get('total_txn',0))}</td>
<td class="num">{sar(b.get('avg_ticket',0))}</td>
<td class="num" style="color:#22c55e"><strong>{sar(b.get('gross_profit_real',0))}</strong></td>
<td><strong>{pct(rm)}</strong></td>
<td class="num" style="color:#e92c30">{sar(b.get('cogs_real',0))}</td>
</tr>'''

    # ── YTD Branch Table ───────────────────────────────────────
    ytd_rows = ''
    ytd_map = {b['name']:b for b in YB}
    for i,b in enumerate(B):
        yb = ytd_map.get(b['name'],{})
        c = COLORS[i%len(COLORS)]
        ytd_rows += f'''<tr>
<td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{c};margin-left:8px"></span><strong>{b['name']}</strong></td>
<td class="num">{sar(yb.get('total',0))}</td>
<td class="num">{num(yb.get('total_txn',0))}</td>
<td class="num">{sar(yb.get('avg_ticket',0))}</td>
<td class="num" style="color:#22c55e">{sar(yb.get('gross_profit_real',0))}</td>
<td><strong>{pct(yb.get('gross_margin_real',0))}</strong></td>
</tr>'''

    # ── Growth Table ───────────────────────────────────────────
    growth_rows = ''
    for i,b in enumerate(B):
        c = COLORS[i%len(COLORS)]
        qoq = b.get('qoq', 0)
        yoy = b.get('yoy', 0)
        rm  = b.get('gross_margin_real', 77)
        growth_rows += f'''<tr>
<td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{c};margin-left:8px"></span><strong>{b['name']}</strong></td>
<td class="num">{sar(b['total'])}</td>
<td>{dt_tag(qoq)} <span class="num" style="color:#6b7280;font-size:11px">{sar(abs(b['total']*(qoq/100)))}</span></td>
<td>{dt_tag(yoy) if yoy else '<span class="tag tn">جديد</span>'}</td>
<td><strong>{pct(rm)}</strong></td>
<td class="num">{num(b.get('total_txn',0))}</td>
<td class="num">{sar(b.get('avg_ticket',0))}</td>
<td><span class="tag {'tg' if b.get('qoq',0)>0 else 'tr'}">{b.get('score',0) if 'score' in b else '-'}</span></td>
</tr>'''

    # ── Delivery Apps Section ─────────────────────────────────
    DELIVERY_RATES = {'Online Paid': 25, 'Taker Wallet': 20}
    del_rows = ''
    total_del = 0; total_commission = 0; total_net = 0
    for method, info in delivery.items():
        rate = DELIVERY_RATES.get(method, 25)
        rev  = info.get('total', 0)
        comm = round(rev * rate / 100)
        net  = rev - comm
        cnt  = info.get('count', 0)
        total_del += rev; total_commission += comm; total_net += net
        del_rows += f'''<tr>
<td><strong>{method}</strong></td>
<td class="num">{num(cnt)} طلب</td>
<td class="num">{sar(rev)}</td>
<td class="num" style="color:#6b7280">{rate}%</td>
<td class="num" style="color:#e92c30">{sar(comm)}</td>
<td class="num" style="color:#22c55e"><strong>{sar(net)}</strong></td>
</tr>'''
    if del_rows:
        del_rows += f'''<tr style="background:#f0f9ff;font-weight:700">
<td colspan="2"><strong>الإجمالي</strong></td>
<td class="num">{sar(total_del)}</td>
<td></td>
<td class="num" style="color:#e92c30">{sar(total_commission)}</td>
<td class="num" style="color:#22c55e">{sar(total_net)}</td>
</tr>'''

    # ── Expenses Table ────────────────────────────────────────
    branch_names = [b['name'] for b in B]
    # Map branch names to expense data
    exp_map = {}
    for bn, edata in expenses.items():
        for pb in branch_names:
            if pb.lower() in bn.lower() or bn.lower() in pb.lower():
                exp_map[pb] = edata
                break
        else:
            exp_map[bn] = edata

    exp_html = ''
    for bn, edata in sorted(exp_map.items()):
        total_exp = edata.get('total', 0)
        items = edata.get('items', [])
        if not items: continue
        items_html = ''.join([f'<tr><td style="padding-right:20px;color:#6b7280">{it["account"]}</td><td class="num">{sar(it["amount"])}</td></tr>' for it in items[:15]])
        exp_html += f'''<div class="card" style="margin-bottom:12px">
<div class="st">{bn} <span style="color:#e92c30;margin-right:8px">{sar(total_exp)}</span></div>
<table class="dt" style="font-size:12px"><tbody>{items_html}</tbody>
<tfoot><tr style="border-top:2px solid #e2e8f0;font-weight:700"><td>إجمالي المصاريف</td><td class="num" style="color:#e92c30">{sar(total_exp)}</td></tr></tfoot>
</table></div>'''

    # ── Menu Engineering ──────────────────────────────────────
    if prods:
        avg_r = sum(p['revenue'] for p in prods)/len(prods)
        avg_m = sum(p.get('margin_pct',0) for p in prods)/len(prods)
        stars  = sorted([p for p in prods if p['revenue']>=avg_r and p.get('margin_pct',0)>=avg_m], key=lambda x:-x['revenue'])[:10]
        quest  = sorted([p for p in prods if p['revenue']<avg_r  and p.get('margin_pct',0)>=avg_m], key=lambda x:-x.get('margin_pct',0))[:10]
        plow   = sorted([p for p in prods if p['revenue']>=avg_r and p.get('margin_pct',0)<avg_m],  key=lambda x:-x['revenue'])[:10]
        dogs   = sorted([p for p in prods if p['revenue']<avg_r  and p.get('margin_pct',0)<avg_m],  key=lambda x:x.get('margin_pct',0))[:8]

        def prod_tbl(items, tag_cls_name):
            rows = ''.join([f'<tr><td style="max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="{p["name"]}">{p["name"].split("/")[-1].strip() or p["name"]}</td><td class="num">{sar(p["revenue"])}</td><td class="num">{num(p.get("qty",0))}</td><td><span class="tag {tag_cls_name}">{pct(p.get("margin_pct",0))}</span></td></tr>' for p in items])
            return f'<table class="dt"><thead><tr><th>المنتج</th><th>إيرادات</th><th>كمية</th><th>هامش</th></tr></thead><tbody>{rows}</tbody></table>'

        menu_eng = f'''
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
  <div class="card" style="border-top:3px solid #22c55e">
    <div class="st" style="color:#22c55e">&#11088; نجوم — هامش عالٍ + مبيعات عالية</div>
    <div style="font-size:11px;color:#6b7280;margin-bottom:8px">حافظ عليها وعززها في القائمة</div>
    {prod_tbl(stars,"tg")}
  </div>
  <div class="card" style="border-top:3px solid #2ba9ed">
    <div class="st" style="color:#2ba9ed">&#10067; علامات استفهام — هامش عالٍ + مبيعات منخفضة</div>
    <div style="font-size:11px;color:#6b7280;margin-bottom:8px">سوّق أكثر واعرضها بشكل بارز</div>
    {prod_tbl(quest,"tbl")}
  </div>
  <div class="card" style="border-top:3px solid #f59e0b">
    <div class="st" style="color:#f59e0b">&#128004; أبقار حلوب — هامش منخفض + مبيعات عالية</div>
    <div style="font-size:11px;color:#6b7280;margin-bottom:8px">راجع التسعير وخفض التكلفة</div>
    {prod_tbl(plow,"tn")}
  </div>
  <div class="card" style="border-top:3px solid #e92c30">
    <div class="st" style="color:#e92c30">&#128021; خسائر — هامش منخفض + مبيعات منخفضة</div>
    <div style="font-size:11px;color:#6b7280;margin-bottom:8px">تحقق من إلغائها أو تطوير وصفتها</div>
    {prod_tbl(dogs,"tr")}
  </div>
</div>'''
    else:
        menu_eng = '<div class="card" style="text-align:center;padding:40px;color:#6b7280">لا توجد بيانات منتجات</div>'

    # ── Hourly heatmap ────────────────────────────────────────
    mH = max(hourly) if max(hourly)>0 else 1
    mD = max(daily) if max(daily)>0 else 1
    hcells = ''.join([f'<div class="hcell" style="background:rgba(43,169,237,{0.05+v/mH*0.85:.2f})" title="{h}:00 - {sar(v)}">{num(v) if v>mH*0.3 else ""}</div>' for h,v in enumerate(hourly)])
    hlbls  = ''.join([f'<div class="hlbl">{h:02d}</div>' for h in range(24)])
    dcells = ''.join([f'<div class="dcell" style="background:rgba(43,169,237,{0.05+v/mD*0.3:.2f})"><div class="dcell-lbl">{DAYS[d]}</div><div class="dcell-val">{num(v)}</div></div>' for d,v in enumerate(daily)])

    # ── Payment methods ───────────────────────────────────────
    pay_total_sum = sum(pay_totals.values()) or 1
    pay_rows = ''.join([f'<tr><td>{m}</td><td class="num">{sar(v)}</td><td class="num">{pct(v/pay_total_sum*100)}</td></tr>' for m,v in sorted(pay_totals.items(), key=lambda x:-x[1])])

    # ── Rankings ──────────────────────────────────────────────
    max_tot = B[0]['total'] if B else 1
    rank_rows = ''
    for i,b in enumerate(sorted(B, key=lambda x:-(x.get('gross_margin_real',0)*0.4+x['total']/max_tot*0.6*100))):
        c = COLORS[i%len(COLORS)]
        rank_rows += f'''<div class="rrow">
<div class="rn">{i+1}</div>
<div class="rnm">{b['name']}</div>
<div class="rbb"><div class="rbf" style="width:{int(b['total']/max_tot*100)}%;background:{c}"></div></div>
<div class="rv">{sar(b['total'])}</div>
{dt_tag(b.get('qoq',0))}
<span class="tag {'tg' if b.get('gross_margin_real',0)>=75 else 'tn'}">{pct(b.get('gross_margin_real',77))}</span>
</div>'''

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>لوحة التحليل المالي - شركة بوصلة التميز التجارية</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></""" + """script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#f5f7fa;--bg2:#ffffff;--bg3:#f0f3f8;--bg4:#e2e8f0;--text:#1e293b;--text2:#64748b;--text3:#94a3b8;--blue:#2ba9ed;--red:#e92c30;--green:#22c55e;--gold:#f59e0b;--purple:#8b5cf6;--border:#e2e8f0;--shadow:0 1px 3px rgba(0,0,0,.08)}}
body{{font-family:'IBM Plex Sans Arabic',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;direction:rtl;font-size:14px}}
.bar{{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:50;box-shadow:var(--shadow)}}
.logo-area{{display:flex;align-items:center;gap:12px}}
.logo-area img{{height:40px;width:auto}}
.title-area h1{{font-size:14px;font-weight:700;color:var(--text);line-height:1.2}}
.title-area p{{font-size:11px;color:var(--text2);margin-top:1px}}
.badge{{font-size:10px;background:#dcfce7;color:#166534;border:1px solid #bbf7d0;padding:3px 10px;border-radius:20px}}
.upd{{font-size:11px;color:var(--text2);font-family:'IBM Plex Mono',monospace}}
.main{{padding:20px 24px;max-width:1400px;margin:0 auto}}
.page-hdr{{margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}}
.page-hdr h2{{font-size:18px;font-weight:700;color:var(--text)}}
.page-hdr p{{font-size:12px;color:var(--text2);margin-top:2px}}
.per{{font-size:11px;color:var(--blue);background:#eff8ff;border:1px solid #bae6fd;padding:4px 12px;border-radius:20px;font-weight:600}}
.kgrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}}
.kgrid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}}
.kc{{background:var(--bg2);border-radius:12px;padding:18px 16px;box-shadow:var(--shadow);border:1px solid var(--border)}}
.kl{{font-size:10px;color:var(--text2);font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}}
.kv{{font-size:24px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text);line-height:1}}
.ks{{font-size:11px;color:var(--text2);margin-top:6px}}
.tabs{{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:4px;display:flex;gap:3px;margin-bottom:20px;overflow-x:auto;flex-wrap:wrap;box-shadow:var(--shadow)}}
.tab{{padding:8px 16px;background:none;border:none;cursor:pointer;font-size:12px;color:var(--text2);border-radius:8px;font-family:inherit;transition:all .2s;white-space:nowrap;font-weight:500}}
.tab.on{{background:#eff8ff;color:var(--blue);font-weight:600}}
.tab:hover:not(.on){{background:var(--bg3)}}
.pane{{display:none}}.pane.on{{display:block;animation:fi .2s ease}}
@keyframes fi{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}
.card{{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:18px;margin-bottom:14px;box-shadow:var(--shadow)}}
.st{{font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
.st::after{{content:'';flex:1;height:1px;background:var(--border)}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}}
.cw{{position:relative;width:100%}}
table.dt{{width:100%;border-collapse:collapse;font-size:12px}}
table.dt th{{padding:10px 12px;font-size:10px;font-weight:700;color:var(--text2);border-bottom:2px solid var(--border);text-align:right;white-space:nowrap;background:var(--bg3);text-transform:uppercase;letter-spacing:.3px}}
table.dt td{{padding:10px 12px;border-bottom:1px solid var(--border);color:var(--text);vertical-align:middle}}
table.dt tr:last-child td{{border-bottom:none}}
table.dt tr:hover td{{background:var(--bg3)}}
table.dt tfoot td{{background:var(--bg3);font-weight:700}}
.tag{{display:inline-flex;align-items:center;gap:2px;font-size:10px;padding:2px 7px;border-radius:4px;font-weight:600;font-family:'IBM Plex Mono',monospace}}
.tg{{background:#dcfce7;color:#166534}}.tr{{background:#fee2e2;color:#991b1b}}.tn{{background:var(--bg4);color:var(--text2)}}.tbl{{background:#dbeafe;color:#1e40af}}
.num{{font-family:'IBM Plex Mono',monospace}}
.hmap{{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-top:6px}}
.hcell{{height:36px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:9px;color:var(--text2);cursor:default;font-family:monospace;transition:opacity .2s}}
.hcell:hover{{opacity:.8}}
.hlabel{{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-bottom:4px}}
.hlbl{{font-size:9px;color:var(--text3);text-align:center}}
.dmap{{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:8px}}
.dcell{{border-radius:8px;padding:12px 6px;text-align:center;font-size:11px;border:1px solid var(--border)}}
.dcell-lbl{{font-size:10px;color:var(--text2);margin-bottom:4px;font-weight:600}}
.dcell-val{{font-size:13px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text)}}
.rrow{{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)}}
.rrow:last-child{{border-bottom:none}}
.rn{{font-size:16px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text3);width:28px;text-align:center;flex-shrink:0}}
.rnm{{min-width:140px;font-size:13px;font-weight:600}}
.rbb{{flex:1;height:8px;background:var(--bg4);border-radius:4px;overflow:hidden}}
.rbf{{height:100%;border-radius:4px;transition:width .5s}}
.rv{{font-size:12px;font-family:'IBM Plex Mono',monospace;min-width:80px;text-align:left;color:var(--text2)}}
.rec{{padding:14px;background:var(--bg2);border-radius:10px;border:1px solid var(--border);border-right:4px solid var(--gold);margin-bottom:8px;box-shadow:var(--shadow)}}
.rec.gn{{border-right-color:var(--green)}}.rec.rd{{border-right-color:var(--red)}}.rec.bl{{border-right-color:var(--blue)}}
.rec-t{{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px}}
.rec-b{{font-size:12px;color:var(--text2);line-height:1.7}}
.exec{{background:#eff8ff;border:1px solid #bae6fd;border-radius:10px;padding:16px;font-size:12px;color:var(--text2);line-height:1.9;margin-top:16px}}
.exec strong{{color:var(--text)}}
.spin{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:16px}}
.sp{{width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--blue);border-radius:50%;animation:sp .7s linear infinite}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
.del-summary{{display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap}}
.del-card{{flex:1;min-width:180px;background:var(--bg2);border-radius:10px;padding:16px;border:1px solid var(--border);text-align:center;box-shadow:var(--shadow)}}
.del-card .label{{font-size:10px;color:var(--text2);font-weight:600;text-transform:uppercase;margin-bottom:6px}}
.del-card .value{{font-size:20px;font-weight:700;font-family:'IBM Plex Mono',monospace}}
.section-divider{{height:1px;background:var(--border);margin:20px 0}}
@media(max-width:900px){{.kgrid{{grid-template-columns:1fr 1fr}}.kgrid4{{grid-template-columns:1fr 1fr}}.g2,.g3{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="bar">
  <div class="logo-area">
    <img src="data:image/jpeg;base64,{LOGO_B64}" alt="Compass of Excellence" onerror="this.style.display='none'">
    <div class="title-area">
      <h1>لوحة التحليل المالي الشهري</h1>
      <p>شركة بوصلة التميز التجارية</p>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:14px">
    <div class="badge">&#128197; {data.get('report_month','')}</div>
    <div class="upd">آخر تحديث: {data.get('updated','')}</div>
  </div>
</div>

<div class="main">
<div class="page-hdr">
  <div><h2>لوحة التحليل المالي - شركة بوصلة التميز التجارية (شهري)</h2>
  <p>تقرير شهر {data.get('report_month','')} | {len(B)} فروع | بيانات من Odoo POS</p></div>
  <span class="per">&#128197; {data.get('date_from','')} - {data.get('date_to','')}</span>
</div>

<div class="kgrid">{kpis}</div>

<div class="tabs">
  <button class="tab on" onclick="sw(0)">&#128202; النظرة العامة</button>
  <button class="tab" onclick="sw(1)">&#128200; الاداء والنمو</button>
  <button class="tab" onclick="sw(2)">&#128176; الربحية والمصاريف</button>
  <button class="tab" onclick="sw(3)">&#128661; تطبيقات التوصيل</button>
  <button class="tab" onclick="sw(4)">&#129409; هندسة القائمة</button>
  <button class="tab" onclick="sw(5)">&#8987; التوقيت والسلوك</button>
  <button class="tab" onclick="sw(6)">&#128179; طرق الدفع</button>
  <button class="tab" onclick="sw(7)">&#128197; YTD</button>
  <button class="tab" onclick="sw(8)">&#127942; التقرير النهائي</button>
</div>

<div id="panes">

<!-- TAB 0: Overview -->
<div class="pane on" id="p0">
  <div class="st">ملخص أداء الفروع - {data.get('report_month','')}</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt">
      <thead><tr><th>الفرع</th><th>الإيرادات</th><th>المعاملات</th><th>م. الفاتورة</th><th>إجمالي الربح</th><th>هامش%</th><th>تكلفة البضاعة</th></tr></thead>
      <tbody>{branch_rows}</tbody>
      <tfoot><tr>
        <td><strong>الإجمالي</strong></td>
        <td class="num"><strong>{sar(total_rev)}</strong></td>
        <td class="num"><strong>{num(total_txn)}</strong></td>
        <td class="num"><strong>{sar(avg_ticket)}</strong></td>
        <td class="num" style="color:#22c55e"><strong>{sar(total_gp)}</strong></td>
        <td><strong>{pct(total_gp/total_rev*100) if total_rev else '0%'}</strong></td>
        <td></td>
      </tr></tfoot>
    </table>
  </div>
  <div class="g2">
    <div class="card"><div class="st">الإيرادات - مقارنة الفروع</div><div class="cw"><canvas id="ch_rev" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">توزيع الإيرادات</div><div class="cw"><canvas id="ch_pie" style="height:260px"></canvas></div></div>
  </div>
</div>

<!-- TAB 1: Growth -->
<div class="pane" id="p1">
  <div class="st">مؤشرات النمو والأداء - {data.get('report_month','')}</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt">
      <thead><tr><th>الفرع</th><th>الإيرادات</th><th>نمو QoQ</th><th>نمو YoY</th><th>هامش%</th><th>المعاملات</th><th>م. الفاتورة</th><th>نقاط</th></tr></thead>
      <tbody>{growth_rows}</tbody>
    </table>
  </div>
  <div class="g2">
    <div class="card"><div class="st">مقارنة QoQ للفروع</div><div class="cw"><canvas id="ch_qoq" style="height:250px"></canvas></div></div>
    <div class="card"><div class="st">الهامش الحقيقي لكل فرع</div><div class="cw"><canvas id="ch_margin" style="height:250px"></canvas></div></div>
  </div>
</div>

<!-- TAB 2: Profitability & Expenses -->
<div class="pane" id="p2">
  <div class="g3">
    <div class="kc" style="border-top:3px solid #22c55e"><div class="kl">إجمالي الإيرادات</div><div class="kv">{sar(total_rev)}</div></div>
    <div class="kc" style="border-top:3px solid #e92c30"><div class="kl">إجمالي المصاريف</div><div class="kv" style="color:#e92c30">{sar(sum(e.get('total',0) for e in expenses.values()))}</div></div>
    <div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">صافي الربح (بعد المصاريف)</div><div class="kv" style="color:#22c55e">{sar(total_gp - sum(e.get('total',0) for e in expenses.values()))}</div></div>
  </div>
  <div class="st">جدول الربحية الحقيقية</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt">
      <thead><tr><th>الفرع</th><th>الإيرادات</th><th>تكلفة البضاعة</th><th>إجمالي الربح</th><th>هامش إجمالي%</th><th>المصاريف</th><th>صافي الربح</th></tr></thead>
      <tbody>{"".join([f'<tr><td><strong>{b["name"]}</strong></td><td class="num">{sar(b["total"])}</td><td class="num" style="color:#e92c30">{sar(b.get("cogs_real",0))}</td><td class="num" style="color:#22c55e">{sar(b.get("gross_profit_real",0))}</td><td><strong>{pct(b.get("gross_margin_real",0))}</strong></td><td class="num" style="color:#e92c30">{sar(next((e.get("total",0) for k,e in expenses.items() if b["name"].lower() in k.lower() or k.lower() in b["name"].lower()),0))}</td><td class="num" style="color:{"#22c55e" if b.get("gross_profit_real",0)-next((e.get("total",0) for k,e in expenses.items() if b["name"].lower() in k.lower()),0)>0 else "#e92c30"}"><strong>{sar(b.get("gross_profit_real",0)-next((e.get("total",0) for k,e in expenses.items() if b["name"].lower() in k.lower() or k.lower() in b["name"].lower()),0))}</strong></td></tr>' for b in B])}</tbody>
    </table>
  </div>
  <div class="st">تفاصيل المصاريف حسب الفرع</div>
  {exp_html if exp_html else '<div class="card" style="text-align:center;color:#6b7280;padding:30px">لا توجد بيانات مصاريف للفترة</div>'}
</div>

<!-- TAB 3: Delivery Apps -->
<div class="pane" id="p3">
  <div class="del-summary">
    <div class="del-card"><div class="label">إجمالي الدخل من التوصيل</div><div class="value" style="color:#2ba9ed">{sar(sum(v.get('total',0) for v in delivery.values()))}</div></div>
    <div class="del-card"><div class="label">العمولات المستقطعة</div><div class="value" style="color:#e92c30">{sar(sum(round(v.get('total',0)*DELIVERY_RATES.get(k,25)/100) for k,v in delivery.items()))}</div></div>
    <div class="del-card"><div class="label">المبالغ المستحقة لك</div><div class="value" style="color:#22c55e">{sar(sum(v.get('total',0)-round(v.get('total',0)*DELIVERY_RATES.get(k,25)/100) for k,v in delivery.items()))}</div></div>
    <div class="del-card"><div class="label">إجمالي الطلبات</div><div class="value">{num(sum(v.get('count',0) for v in delivery.values()))}</div></div>
  </div>
  <div class="st">تحليل تطبيقات التوصيل - {data.get('report_month','')}</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt">
      <thead><tr><th>التطبيق</th><th>عدد الطلبات</th><th>إجمالي الدخل</th><th>نسبة العمولة</th><th>مبلغ العمولة المستقطع</th><th>المبلغ المستحق لك</th></tr></thead>
      <tbody>{del_rows if del_rows else '<tr><td colspan="6" style="text-align:center;color:#6b7280">لا توجد بيانات تطبيقات التوصيل للفترة</td></tr>'}</tbody>
    </table>
  </div>
  <div class="card" style="background:#fffbeb;border-color:#fde68a">
    <div class="rec-t">&#128276; ملاحظة حول نسب العمولة</div>
    <div class="rec-b" style="margin-top:4px">نسبة "Online Paid" محسوبة بـ 25% (متوسط تطبيقات التوصيل). "Taker Wallet" بنسبة 20%. يمكن تعديل هذه النسب عند توفر العقود الفعلية.</div>
  </div>
</div>

<!-- TAB 4: Menu Engineering -->
<div class="pane" id="p4">
  <div class="st">مصفوفة هندسة القائمة - تحليل المنتجات</div>
  {menu_eng}
</div>

<!-- TAB 5: Timing -->
<div class="pane" id="p5">
  <div class="card"><div class="st">خريطة حرارة الإيرادات - توزيع ساعي</div>
    <div class="hlabel">{hlbls}</div>
    <div class="hmap">{hcells}</div>
    <div style="margin-top:8px;font-size:11px;color:#64748b">أعلى ساعة: <strong style="color:#2ba9ed">{hourly.index(max(hourly)):02d}:00</strong> | {sar(max(hourly))}</div>
  </div>
  <div class="g2">
    <div class="card"><div class="st">أداء أيام الأسبوع</div><div class="dmap">{dcells}</div></div>
    <div class="card"><div class="st">التوزيع الساعي</div><div class="cw"><canvas id="ch_hourly" style="height:220px"></canvas></div></div>
  </div>
</div>

<!-- TAB 6: Payments -->
<div class="pane" id="p6">
  <div class="g2">
    <div class="card"><div class="st">توزيع طرق الدفع</div><div class="cw"><canvas id="ch_pay" style="height:280px"></canvas></div></div>
    <div class="card"><div class="st">مبالغ طرق الدفع</div>
      <table class="dt"><thead><tr><th>طريقة الدفع</th><th>المبلغ</th><th>النسبة</th></tr></thead>
      <tbody>{pay_rows}</tbody>
      <tfoot><tr><td><strong>الإجمالي</strong></td><td class="num"><strong>{sar(sum(pay_totals.values()))}</strong></td><td class="num"><strong>100%</strong></td></tr></tfoot>
      </table>
    </div>
  </div>
</div>

<!-- TAB 7: YTD -->
<div class="pane" id="p7">
  <div class="st">مؤشرات YTD - من {data.get('ytd_from','')} إلى {data.get('ytd_to','')}</div>
  <div class="kgrid4">{ytd_kpis}</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt">
      <thead><tr><th>الفرع</th><th>الإيرادات YTD</th><th>المعاملات</th><th>م. الفاتورة</th><th>إجمالي الربح</th><th>هامش%</th></tr></thead>
      <tbody>{ytd_rows}</tbody>
      <tfoot><tr>
        <td><strong>الإجمالي</strong></td>
        <td class="num"><strong>{sar(ytd_rev)}</strong></td>
        <td class="num"><strong>{num(ytd_txn)}</strong></td>
        <td class="num"><strong>{sar(round(ytd_rev/ytd_txn,1) if ytd_txn else 0)}</strong></td>
        <td class="num" style="color:#22c55e"><strong>{sar(ytd_gp)}</strong></td>
        <td><strong>{pct(ytd_gp/ytd_rev*100) if ytd_rev else '0%'}</strong></td>
      </tr></tfoot>
    </table>
  </div>
  <div class="g2">
    <div class="card"><div class="st">تطور الإيرادات YTD</div><div class="cw"><canvas id="ch_ytd" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">مقارنة YTD vs شهري</div>
      <table class="dt"><thead><tr><th>الفرع</th><th>هذا الشهر</th><th>YTD</th><th>نسبة الشهر</th></tr></thead>
      <tbody>{"".join([f'<tr><td><strong>{b["name"]}</strong></td><td class="num">{sar(b["total"])}</td><td class="num">{sar(next((yb["total"] for yb in YB if yb["name"]==b["name"]),0))}</td><td class="num" style="color:#2ba9ed">{pct(b["total"]/next((yb["total"] for yb in YB if yb["name"]==b["name"]),b["total"])*100) if YB else "0%"}</td></tr>' for b in B])}</tbody>
      </table>
    </div>
  </div>
</div>

<!-- TAB 8: Final Report -->
<div class="pane" id="p8">
  <div class="st">&#127942; التصنيف المركّب للفروع</div>
  <div class="card">{rank_rows}</div>
  <div class="g2">
    <div>
      <div class="st">&#129351; أعلى 3 فروع</div>
      {"".join([f'<div class="card" style="margin-bottom:8px;border-right:4px solid {COLORS[i%len(COLORS)]}"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:700">{"🥇🥈🥉"[i]} {b["name"]}</span><span class="tag tg">{sar(b["total"])}</span></div><div style="margin-top:6px;font-size:11px;color:#64748b">هامش: {pct(b.get("gross_margin_real",0))} | الطلبات: {num(b.get("total_txn",0))} | م. الفاتورة: {sar(b.get("avg_ticket",0))}</div></div>' for i,b in enumerate(B[:3])])}
    </div>
    <div>
      <div class="st">&#128161; التوصيات</div>
      <div class="rec gn"><div class="rec-t">&#127919; هندسة القائمة</div><div class="rec-b">تعزيز منتجات "علامات الاستفهام" في القائمة يرفع الإيراد بدون زيادة تكلفة.</div></div>
      <div class="rec bl"><div class="rec-t">&#8987; التوظيف الذكي</div><div class="rec-b">جدولة الموظفين حسب ساعات الذروة يقلل التكلفة التشغيلية.</div></div>
      <div class="rec rd"><div class="rec-t">&#128661; تطبيقات التوصيل</div><div class="rec-b">مراجعة عقود التوصيل ومقارنة النسب للحصول على شروط أفضل.</div></div>
    </div>
  </div>
  <div class="exec">
    <strong>&#128203; الملخص التنفيذي - {data.get("report_month","")}</strong><br><br>
    حقق النظام إيرادات <strong>{sar(total_rev)}</strong> عبر {len(B)} فروع بإجمالي ربح <strong>{sar(total_gp)}</strong> وهامش <strong>{pct(total_gp/total_rev*100) if total_rev else "0%"}</strong>.
    نُفّذت <strong>{num(total_txn)}</strong> معاملة بمتوسط فاتورة <strong>{sar(avg_ticket)}</strong>.
    يتصدر <strong>{B[0]["name"] if B else "-"}</strong> القائمة.
    إيرادات YTD: <strong>{sar(ytd_rev)}</strong> | دخل التوصيل: <strong>{sar(sum(v.get("total",0) for v in delivery.values()))}</strong>.
  </div>
</div>

</div><!-- /panes -->
</div><!-- /main -->

<script>
var C = {json.dumps(COLORS)};
var DAYS = ['الاحد','الاثنين','الثلاثاء','الاربعاء','الخميس','الجمعة','السبت'];
var B = {json.dumps(B)};
var YB = {json.dumps(YB)};
var HOURLY = {json.dumps(hourly)};
var DAILY = {json.dumps(daily)};
var PAYMENTS = {json.dumps(pay_totals)};
var BASE = {{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}}}};
var CH = {{}};

function mk(id,cfg){{var c=document.getElementById(id);if(!c)return;if(CH[id])CH[id].destroy();CH[id]=new Chart(c,cfg);}}
function fmt(n){{return Math.abs(n)>=1e6?(n/1e6).toFixed(2)+'M':Math.abs(n)>=1e3?(n/1e3).toFixed(1)+'K':Math.round(n).toLocaleString();}}

function sw(i){{
  document.querySelectorAll('.tab').forEach(function(b,j){{b.classList.toggle('on',i===j);}});
  document.querySelectorAll('.pane').forEach(function(p,j){{p.classList.toggle('on',i===j);}});
  if(i===0)drawOverview();
  else if(i===1)drawGrowth();
  else if(i===5)drawTiming();
  else if(i===6)drawPayments();
  else if(i===7)drawYTD();
}}

function drawOverview(){{
  if(CH['ch_rev'])return;
  mk('ch_rev',{{type:'bar',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.total;}}),backgroundColor:C,borderRadius:6,borderSkipped:false}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return fmt(v);}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,0.8)'}}}}}}}}}});
  mk('ch_pie',{{type:'doughnut',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.total;}}),backgroundColor:C,borderWidth:2,borderColor:'#ffffff'}}]}},options:{{...BASE,cutout:'60%',plugins:{{legend:{{display:true,position:'bottom',labels:{{color:'#64748b',font:{{size:10}},boxWidth:10}}}},tooltip:{{callbacks:{{label:function(ctx){{return ctx.label+': '+fmt(ctx.raw);}}}}}}}}}}}});
}}

function drawGrowth(){{
  if(CH['ch_qoq'])return;
  mk('ch_qoq',{{type:'bar',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{label:'QoQ%',data:B.map(function(b){{return b.qoq||0;}}),backgroundColor:B.map(function(b){{return (b.qoq||0)>=0?'rgba(34,197,94,.8)':'rgba(233,44,48,.8)';}})  ,borderRadius:4}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return v+'%';}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,0.8)'}},afterDataLimits:function(s){{s.min=Math.min(s.min,-10);s.max=Math.max(s.max,15);}}}}}}}}}});
  mk('ch_margin',{{type:'bar',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.gross_margin_real||77;}}),backgroundColor:B.map(function(b){{var rm=b.gross_margin_real||77;return rm>=75?'rgba(34,197,94,.8)':rm>=65?'rgba(245,158,11,.8)':'rgba(233,44,48,.8)';}})  ,borderRadius:4,indexAxis:'y'}}]}},options:{{...BASE,indexAxis:'y',scales:{{x:{{ticks:{{color:'#64748b',callback:function(v){{return v+'%';}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}},min:50}},y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}}}}}}}});
}}

function drawTiming(){{
  if(CH['ch_hourly'])return;
  var mH=Math.max.apply(null,HOURLY.concat([1])),mD=Math.max.apply(null,DAILY.concat([1]));
  mk('ch_hourly',{{type:'line',data:{{labels:Array.from({{length:24}},function(_,h){{return (h<10?'0'+h:h)+':00';}}),datasets:[{{data:HOURLY,borderColor:'#2ba9ed',backgroundColor:'rgba(43,169,237,.1)',borderWidth:2,fill:true,tension:.4,pointRadius:2}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:9}}}},grid:{{color:'rgba(226,232,240,.8)'}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return fmt(v);}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}}}}}}}}}}});
}}

function drawPayments(){{
  if(CH['ch_pay'])return;
  var keys=Object.keys(PAYMENTS),vals=keys.map(function(k){{return PAYMENTS[k];}});
  mk('ch_pay',{{type:'doughnut',data:{{labels:keys,datasets:[{{data:vals,backgroundColor:C.slice(0,keys.length),borderWidth:2,borderColor:'#ffffff'}}]}},options:{{...BASE,cutout:'55%',plugins:{{legend:{{display:true,position:'right',labels:{{color:'#64748b',font:{{size:11}},boxWidth:12}}}},tooltip:{{callbacks:{{label:function(ctx){{var tot=vals.reduce(function(a,b){{return a+b;}},0);return ctx.label+': '+fmt(ctx.raw)+' ('+((ctx.raw/tot*100).toFixed(1))+'%)';}}}}}}}}}}}});
}}

function drawYTD(){{
  if(CH['ch_ytd'])return;
  var months={{}};
  YB.forEach(function(b){{
    if(b.monthly){{Object.entries(b.monthly).forEach(function(e){{months[e[0]]=(months[e[0]]||0)+e[1];}});}}
  }});
  var keys=Object.keys(months).sort();
  mk('ch_ytd',{{type:'bar',data:{{labels:keys,datasets:[{{data:keys.map(function(k){{return Math.round(months[k]);}}) ,backgroundColor:'rgba(43,169,237,.7)',borderRadius:4,borderSkipped:false}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return fmt(v);}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}}}}}}}}}}});
}}

drawOverview();
</""" + """script>
</body>
</html>"""

    return html

try:
    with open('data.json','r',encoding='utf-8') as f:
        data = json.load(f)
except:
    data = {{'branches':[],'ytd_branches':[],'products':[],'hourly':[0]*24,'daily':[0]*7,
             'payment_totals':{{}},'delivery_apps':{{}},'delivery_ytd':{{}},'expenses':{{}},'expenses_ytd':{{}},
             'report_month':'غير محدد','updated':'','date_from':'','date_to':'','ytd_from':'','ytd_to':''}}

html = build_html(data)
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print(f'index.html generated: {{len(html):,}} chars')
