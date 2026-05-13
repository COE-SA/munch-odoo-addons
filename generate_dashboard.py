import json

LOGO_SVG = """<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 200 60\" height=\"44\">
  <!-- Diamond/Compass icon -->
  <g transform=\"translate(5,5)\">
    <!-- Top-left blue triangle -->
    <polygon points=\"25,25 5,45 25,5\" fill=\"#2ba9ed\"/>
    <!-- Top-right red triangle -->
    <polygon points=\"25,25 45,5 45,25\" fill=\"#e92c30\"/>
    <!-- Bottom-left dark triangle -->
    <polygon points=\"25,25 5,45 25,45\" fill=\"#2d2d2d\"/>
    <!-- Bottom-right gray triangle -->
    <polygon points=\"25,25 45,25 45,45\" fill=\"#888888\"/>
  </g>
  <!-- Text -->
  <text x=\"60\" y=\"22\" font-family=\"Arial Black, sans-serif\" font-size=\"13\" font-weight=\"900\" fill=\"#1e293b\" letter-spacing=\"0.5\">COMPASS OF</text>
  <text x=\"60\" y=\"42\" font-family=\"Arial, sans-serif\" font-size=\"10\" font-weight=\"400\" fill=\"#64748b\" letter-spacing=\"2\">— EXCELLENCE —</text>
</svg>"""

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
    expenses = data.get('expenses', {})

    total_rev = sum(b['total'] for b in B)
    total_gp  = sum(b.get('gross_profit_real', b['total']*0.77) for b in B)
    total_txn = sum(b.get('total_txn', 0) for b in B)
    avg_ticket = round(total_rev/total_txn, 1) if total_txn else 0

    ytd_rev = sum(b['total'] for b in YB)
    ytd_gp  = sum(b.get('gross_profit_real', b['total']*0.77) for b in YB)
    ytd_txn = sum(b.get('total_txn', 0) for b in YB)
    ytd_margin = round(ytd_gp/ytd_rev*100,1) if ytd_rev else 0

    COLORS = ['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#10b981']
    DAYS = ['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت']
    DELIVERY_RATES = {'Online Paid': 25, 'Taker Wallet': 20}

    # ── KPI Cards ──────────────────────────────────────────
    kpis = ''.join([
        f'<div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">إجمالي الإيرادات</div><div class="kv">{sar(total_rev)}</div><div class="ks">{len(B)} فروع</div></div>',
        f'<div class="kc" style="border-top:3px solid #22c55e"><div class="kl">إجمالي الأرباح</div><div class="kv">{sar(total_gp)}</div><div class="ks">{pct(total_gp/total_rev*100) if total_rev else "0%"} هامش</div></div>',
        f'<div class="kc" style="border-top:3px solid #f59e0b"><div class="kl">إجمالي المعاملات</div><div class="kv">{num(total_txn)}</div><div class="ks">طلب</div></div>',
        f'<div class="kc" style="border-top:3px solid #8b5cf6"><div class="kl">متوسط الفاتورة</div><div class="kv">{sar(avg_ticket)}</div><div class="ks">لكل طلب</div></div>',
        f'<div class="kc" style="border-top:3px solid #e92c30"><div class="kl">أفضل فرع</div><div class="kv" style="font-size:15px;line-height:1.5">{B[0]["name"] if B else "-"}</div><div class="ks">{sar(B[0]["total"]) if B else "-"}</div></div>',
    ])

    # ── YTD KPIs ───────────────────────────────────────────
    ytd_kpis = ''.join([
        f'<div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">إيرادات YTD</div><div class="kv">{sar(ytd_rev)}</div><div class="ks">{data.get("ytd_from","")} - {data.get("ytd_to","")}</div></div>',
        f'<div class="kc" style="border-top:3px solid #22c55e"><div class="kl">أرباح YTD</div><div class="kv">{sar(ytd_gp)}</div><div class="ks">{pct(ytd_margin)} هامش</div></div>',
        f'<div class="kc" style="border-top:3px solid #f59e0b"><div class="kl">معاملات YTD</div><div class="kv">{num(ytd_txn)}</div><div class="ks">طلب</div></div>',
        f'<div class="kc" style="border-top:3px solid #8b5cf6"><div class="kl">متوسط الفاتورة YTD</div><div class="kv">{sar(round(ytd_rev/ytd_txn,1) if ytd_txn else 0)}</div><div class="ks">لكل طلب</div></div>',
    ])

    # ── Overview Table ──────────────────────────────────────
    branch_rows = ''.join([
        f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{COLORS[i%8]};margin-left:8px"></span><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td>'
        f'<td class="num">{num(b.get("total_txn",0))}</td>'
        f'<td class="num">{sar(b.get("avg_ticket",0))}</td>'
        f'<td class="num" style="color:#22c55e"><strong>{sar(b.get("gross_profit_real",0))}</strong></td>'
        f'<td><strong>{pct(b.get("gross_margin_real",0))}</strong></td>'
        f'<td class="num" style="color:#e92c30">{sar(b.get("cogs_real",0))}</td></tr>'
        for i,b in enumerate(B)
    ])

    # ── Growth Table ───────────────────────────────────────
    growth_rows = ''.join([
        f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{COLORS[i%8]};margin-left:8px"></span><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td>'
        f'<td>{dt_tag(b.get("qoq",0))}</td>'
        f'<td>{"<span class=\"tag tn\">جديد</span>" if b.get("yoy",0)==0 else dt_tag(b.get("yoy",0))}</td>'
        f'<td><strong>{pct(b.get("gross_margin_real",0))}</strong></td>'
        f'<td class="num">{num(b.get("total_txn",0))}</td>'
        f'<td class="num">{sar(b.get("avg_ticket",0))}</td></tr>'
        for i,b in enumerate(B)
    ])

    # ── YTD Table ──────────────────────────────────────────
    ytd_map = {b['name']:b for b in YB}
    ytd_rows = ''.join([
        f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{COLORS[i%8]};margin-left:8px"></span><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(ytd_map.get(b["name"],{}).get("total",0))}</td>'
        f'<td class="num">{num(ytd_map.get(b["name"],{}).get("total_txn",0))}</td>'
        f'<td class="num">{sar(ytd_map.get(b["name"],{}).get("avg_ticket",0))}</td>'
        f'<td class="num" style="color:#22c55e">{sar(ytd_map.get(b["name"],{}).get("gross_profit_real",0))}</td>'
        f'<td><strong>{pct(ytd_map.get(b["name"],{}).get("gross_margin_real",0))}</strong></td></tr>'
        for i,b in enumerate(B)
    ])

    # ── Delivery Apps ─────────────────────────────────────
    total_del = sum(v.get('total',0) for v in delivery.values())
    total_comm = sum(round(v.get('total',0)*DELIVERY_RATES.get(k,25)/100) for k,v in delivery.items())
    total_net = total_del - total_comm
    del_rows = ''.join([
        f'<tr><td><strong>{method}</strong></td>'
        f'<td class="num">{num(info.get("count",0))} طلب</td>'
        f'<td class="num">{sar(info.get("total",0))}</td>'
        f'<td class="num" style="color:#6b7280">{DELIVERY_RATES.get(method,25)}%</td>'
        f'<td class="num" style="color:#e92c30">{sar(round(info.get("total",0)*DELIVERY_RATES.get(method,25)/100))}</td>'
        f'<td class="num" style="color:#22c55e"><strong>{sar(info.get("total",0)-round(info.get("total",0)*DELIVERY_RATES.get(method,25)/100))}</strong></td></tr>'
        for method, info in delivery.items()
    ])
    if del_rows:
        del_rows += f'<tr style="background:#f0f9ff;font-weight:700"><td colspan="2"><strong>الإجمالي</strong></td><td class="num">{sar(total_del)}</td><td></td><td class="num" style="color:#e92c30">{sar(total_comm)}</td><td class="num" style="color:#22c55e">{sar(total_net)}</td></tr>'

    # ── Expenses Table ────────────────────────────────────
    exp_html = ''
    for bn, edata in sorted(expenses.items()):
        total_exp = edata.get('total', 0)
        items = edata.get('items', [])[:15]
        if not items: continue
        items_html = ''.join([f'<tr><td style="color:#64748b;padding-right:16px">{it["account"]}</td><td class="num">{sar(it["amount"])}</td></tr>' for it in items])
        exp_html += f'<div class="card" style="margin-bottom:12px"><div class="st" style="color:#e92c30">{bn} — إجمالي: {sar(total_exp)}</div><table class="dt" style="font-size:12px"><thead><tr><th>بند المصروف</th><th>المبلغ</th></tr></thead><tbody>{items_html}</tbody><tfoot><tr style="border-top:2px solid #e2e8f0;background:#fef2f2"><td><strong>إجمالي المصاريف</strong></td><td class="num" style="color:#e92c30"><strong>{sar(total_exp)}</strong></td></tr></tfoot></table></div>'

    # ── Menu Engineering ──────────────────────────────────
    if prods:
        avg_r = sum(p['revenue'] for p in prods)/len(prods)
        avg_m = sum(p.get('margin_pct',0) for p in prods)/len(prods)
        def nm(p): return p['name'].split('/')[-1].strip() or p['name']
        stars  = sorted([p for p in prods if p['revenue']>=avg_r and p.get('margin_pct',0)>=avg_m], key=lambda x:-x['revenue'])[:10]
        quest  = sorted([p for p in prods if p['revenue']<avg_r  and p.get('margin_pct',0)>=avg_m], key=lambda x:-x.get('margin_pct',0))[:10]
        plow   = sorted([p for p in prods if p['revenue']>=avg_r and p.get('margin_pct',0)<avg_m],  key=lambda x:-x['revenue'])[:10]
        dogs   = sorted([p for p in prods if p['revenue']<avg_r  and p.get('margin_pct',0)<avg_m],  key=lambda x:x.get('margin_pct',0))[:8]

        def prod_tbl(items, tc):
            rows = ''.join([f'<tr><td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:12px" title="{p["name"]}">{nm(p)}</td><td class="num">{sar(p["revenue"])}</td><td class="num">{num(p.get("qty",0))}</td><td><span class="tag {tc}">{pct(p.get("margin_pct",0))}</span></td></tr>' for p in items])
            return f'<div style="overflow-x:auto"><table class="dt"><thead><tr><th>المنتج</th><th>الإيرادات</th><th>الكمية</th><th>الهامش</th></tr></thead><tbody>{rows}</tbody></table></div>'

        menu_eng = f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px">
<div class="card" style="border-top:4px solid #22c55e">
  <div style="background:#f0fdf4;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#166534">&#11088; نجوم — حافظ عليها وعززها</div>
    <div style="font-size:11px;color:#166534;margin-top:2px">هامش عالٍ + مبيعات عالية — الأفضل أداءً</div>
  </div>
  {prod_tbl(stars,"tg")}
</div>
<div class="card" style="border-top:4px solid #2ba9ed">
  <div style="background:#eff8ff;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#1e40af">&#10067; علامات استفهام — سوّق أكثر</div>
    <div style="font-size:11px;color:#1e40af;margin-top:2px">هامش عالٍ + مبيعات منخفضة — فرصة ذهبية</div>
  </div>
  {prod_tbl(quest,"tbl")}
</div>
<div class="card" style="border-top:4px solid #f59e0b">
  <div style="background:#fffbeb;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#92400e">&#128004; أبقار حلوب — راجع التسعير</div>
    <div style="font-size:11px;color:#92400e;margin-top:2px">هامش منخفض + مبيعات عالية — يمكن تحسينها</div>
  </div>
  {prod_tbl(plow,"tn")}
</div>
<div class="card" style="border-top:4px solid #e92c30">
  <div style="background:#fef2f2;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#991b1b">&#128021; خسائر — تحقق من إلغائها</div>
    <div style="font-size:11px;color:#991b1b;margin-top:2px">هامش منخفض + مبيعات منخفضة — راجع أو أوقف</div>
  </div>
  {prod_tbl(dogs,"tr")}
</div></div>'''
    else:
        menu_eng = '<div class="card" style="text-align:center;padding:40px;color:#64748b">لا توجد بيانات منتجات</div>'

    # ── Timing ────────────────────────────────────────────
    mH = max(hourly) if max(hourly)>0 else 1
    mD = max(daily) if max(daily)>0 else 1
    hcells = ''.join([f'<div class="hcell" style="background:rgba(43,169,237,{0.05+v/mH*0.85:.2f})" title="{h:02d}:00 - {sar(v)}">{num(v) if v>mH*0.3 else ""}</div>' for h,v in enumerate(hourly)])
    hlbls  = ''.join([f'<div class="hlbl">{h:02d}</div>' for h in range(24)])
    dcells = ''.join([f'<div class="dcell" style="background:rgba(43,169,237,{0.08+v/mD*0.25:.2f})"><div class="dcell-lbl">{DAYS[d]}</div><div class="dcell-val">{num(v)}</div></div>' for d,v in enumerate(daily)])

    # ── Payments ─────────────────────────────────────────
    pay_sum = sum(pay_totals.values()) or 1
    pay_rows = ''.join([f'<tr><td>{m}</td><td class="num">{sar(v)}</td><td class="num">{pct(v/pay_sum*100)}</td></tr>' for m,v in sorted(pay_totals.items(), key=lambda x:-x[1])])

    # ── Rankings ─────────────────────────────────────────
    max_t = B[0]['total'] if B else 1
    MEDALS = ['&#127941;','&#129352;','&#127942;']
    rank_rows = ''.join([
        f'<div class="rrow"><div class="rn">{i+1}</div><div class="rnm">{b["name"]}</div>'
        f'<div class="rbb"><div class="rbf" style="width:{int(b["total"]/max_t*100)}%;background:{COLORS[i%8]}"></div></div>'
        f'<div class="rv">{sar(b["total"])}</div>'
        f'{dt_tag(b.get("qoq",0))}'
        f'<span class="tag {"tg" if b.get("gross_margin_real",0)>=75 else "tn"}">{pct(b.get("gross_margin_real",77))}</span></div>'
        for i,b in enumerate(sorted(B, key=lambda x:-x['total']))
    ])

    # ── Profitability with expenses ───────────────────────
    total_expenses_sum = sum(e.get('total',0) for e in expenses.values())
    profit_rows = ''.join([
        f'<tr><td><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td>'
        f'<td class="num" style="color:#e92c30">{sar(b.get("cogs_real",0))}</td>'
        f'<td class="num" style="color:#22c55e">{sar(b.get("gross_profit_real",0))}</td>'
        f'<td><strong>{pct(b.get("gross_margin_real",0))}</strong></td>'
        f'<td class="num" style="color:#e92c30">{sar(next((e.get("total",0) for k,e in expenses.items() if b["name"].lower() in k.lower() or k.lower() in b["name"].lower()),0))}</td>'
        f'<td class="num" style="color:{"#22c55e" if b.get("gross_profit_real",0)>0 else "#e92c30"}"><strong>{sar(b.get("gross_profit_real",0)-next((e.get("total",0) for k,e in expenses.items() if b["name"].lower() in k.lower() or k.lower() in b["name"].lower()),0))}</strong></td>'
        f'</tr>'
        for b in B
    ])

    COLS = json.dumps(COLORS)
    B_JSON = json.dumps(B, default=str)
    YB_JSON = json.dumps(YB, default=str)
    H_JSON = json.dumps(hourly)
    D_JSON = json.dumps(daily)
    P_JSON = json.dumps(pay_totals)

    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>لوحة التحليل المالي - شركة بوصلة التميز التجارية</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></""" + """script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#f5f7fa;--bg2:#ffffff;--bg3:#f0f4f9;--bg4:#e2e8f0;--text:#1e293b;--text2:#64748b;--text3:#94a3b8;--blue:#2ba9ed;--red:#e92c30;--green:#22c55e;--gold:#f59e0b;--purple:#8b5cf6;--border:#e2e8f0}}
body{{font-family:'IBM Plex Sans Arabic',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;direction:rtl;font-size:14px}}
.bar{{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;height:62px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:50;box-shadow:0 1px 4px rgba(0,0,0,.07)}}
.logo-wrap{{display:flex;align-items:center;gap:14px}}
.logo-wrap svg{{height:44px;width:auto}}
.title-area h1{{font-size:14px;font-weight:700;color:var(--text);line-height:1.3}}
.title-area p{{font-size:11px;color:var(--text2)}}
.badge{{font-size:11px;background:#dcfce7;color:#166534;border:1px solid #bbf7d0;padding:4px 12px;border-radius:20px;font-weight:600}}
.upd{{font-size:11px;color:var(--text2);font-family:'IBM Plex Mono',monospace}}
.main{{padding:20px 24px;max-width:1440px;margin:0 auto}}
.page-hdr{{margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}}
.page-hdr h2{{font-size:18px;font-weight:700}}.page-hdr p{{font-size:12px;color:var(--text2);margin-top:2px}}
.per{{font-size:11px;color:var(--blue);background:#eff8ff;border:1px solid #bae6fd;padding:4px 14px;border-radius:20px;font-weight:600}}
.kgrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}}
.kgrid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}}
.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px}}
.kc{{background:var(--bg2);border-radius:12px;padding:18px 16px;box-shadow:0 1px 3px rgba(0,0,0,.06);border:1px solid var(--border)}}
.kl{{font-size:10px;color:var(--text2);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}}
.kv{{font-size:22px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text);line-height:1}}
.ks{{font-size:11px;color:var(--text2);margin-top:6px}}
.tabs{{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:4px;display:flex;gap:3px;margin-bottom:20px;overflow-x:auto;flex-wrap:wrap;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.tab{{padding:8px 16px;background:none;border:none;cursor:pointer;font-size:12px;color:var(--text2);border-radius:8px;font-family:inherit;transition:all .2s;white-space:nowrap;font-weight:500}}
.tab.on{{background:#eff8ff;color:var(--blue);font-weight:700}}
.tab:hover:not(.on){{background:var(--bg3)}}
.pane{{display:none}}.pane.on{{display:block;animation:fi .2s ease}}
@keyframes fi{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}
.card{{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:18px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}}
.st{{font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:14px;display:flex;align-items:center;gap:8px}}
.st::after{{content:'';flex:1;height:1px;background:var(--border)}}
.cw{{position:relative;width:100%}}
table.dt{{width:100%;border-collapse:collapse;font-size:12px}}
table.dt th{{padding:10px 12px;font-size:10px;font-weight:700;color:var(--text2);border-bottom:2px solid var(--border);text-align:right;white-space:nowrap;background:var(--bg3);text-transform:uppercase}}
table.dt td{{padding:10px 12px;border-bottom:1px solid var(--border);color:var(--text);vertical-align:middle}}
table.dt tr:last-child td{{border-bottom:none}}
table.dt tr:hover td{{background:var(--bg3)}}
table.dt tfoot td{{background:var(--bg3);font-weight:700;border-top:2px solid var(--border)}}
.tag{{display:inline-flex;align-items:center;gap:2px;font-size:10px;padding:2px 7px;border-radius:4px;font-weight:600;font-family:'IBM Plex Mono',monospace}}
.tg{{background:#dcfce7;color:#166534}}.tr{{background:#fee2e2;color:#991b1b}}.tn{{background:var(--bg4);color:var(--text2)}}.tbl{{background:#dbeafe;color:#1e40af}}
.num{{font-family:'IBM Plex Mono',monospace}}
.hmap{{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-top:6px}}
.hcell{{height:38px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:9px;color:var(--text2);cursor:default;font-family:monospace;font-weight:600}}
.hlabel{{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-bottom:4px}}
.hlbl{{font-size:9px;color:var(--text3);text-align:center}}
.dmap{{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:8px}}
.dcell{{border-radius:8px;padding:14px 6px;text-align:center;border:1px solid var(--border);background:var(--bg2)}}
.dcell-lbl{{font-size:10px;color:var(--text2);margin-bottom:6px;font-weight:600}}
.dcell-val{{font-size:14px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text)}}
.rrow{{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)}}
.rrow:last-child{{border-bottom:none}}
.rn{{font-size:16px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text3);width:28px;text-align:center;flex-shrink:0}}
.rnm{{min-width:140px;font-size:13px;font-weight:600}}
.rbb{{flex:1;height:10px;background:var(--bg4);border-radius:5px;overflow:hidden}}
.rbf{{height:100%;border-radius:5px}}
.rv{{font-size:12px;font-family:'IBM Plex Mono',monospace;min-width:90px;text-align:left;color:var(--text2)}}
.del-card{{flex:1;min-width:180px;background:var(--bg2);border-radius:10px;padding:16px;border:1px solid var(--border);text-align:center}}
.del-card .label{{font-size:10px;color:var(--text2);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}}
.del-card .value{{font-size:20px;font-weight:700;font-family:'IBM Plex Mono',monospace}}
.rec{{padding:14px;background:var(--bg2);border-radius:10px;border:1px solid var(--border);border-right:4px solid var(--gold);margin-bottom:8px}}
.rec.gn{{border-right-color:var(--green)}}.rec.rd{{border-right-color:var(--red)}}.rec.bl{{border-right-color:var(--blue)}}
.rec-t{{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px}}
.rec-b{{font-size:12px;color:var(--text2);line-height:1.7}}
.exec{{background:#eff8ff;border:1px solid #bae6fd;border-radius:10px;padding:16px;font-size:12px;color:var(--text2);line-height:1.9;margin-top:16px}}
.exec strong{{color:var(--text)}}
.spin{{display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:16px}}
.sp{{width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--blue);border-radius:50%;animation:sp .7s linear infinite}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
@media(max-width:900px){{.kgrid{{grid-template-columns:1fr 1fr}}.kgrid4{{grid-template-columns:1fr 1fr}}.g2,.g3{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="bar">
  <div class="logo-wrap">
    {LOGO_SVG}
    <div class="title-area">
      <h1>لوحة التحليل المالي - شركة بوصلة التميز التجارية (شهري)</h1>
      <p>تقرير شهر {data.get('report_month','—')} | {len(B)} فروع | بيانات Odoo POS</p>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:14px">
    <div class="badge">&#128197; {data.get('report_month','')}</div>
    <div class="upd">تحديث: {data.get('updated','')}</div>
  </div>
</div>

<div class="main">
<div class="page-hdr">
  <div><h2>التحليل المالي الشهري — {data.get('report_month','')}</h2>
  <p>{len(B)} فروع | بيانات من Odoo POS</p></div>
  <span class="per">&#128197; {data.get('date_from','')} إلى {data.get('date_to','')}</span>
</div>

<div class="kgrid">{kpis}</div>

<div class="tabs">
  <button class="tab on" onclick="sw(0)">&#128202; النظرة العامة</button>
  <button class="tab" onclick="sw(1)">&#128200; الأداء والنمو</button>
  <button class="tab" onclick="sw(2)">&#128176; الربحية والمصاريف</button>
  <button class="tab" onclick="sw(3)">&#128661; تطبيقات التوصيل</button>
  <button class="tab" onclick="sw(4)">&#129409; هندسة القائمة</button>
  <button class="tab" onclick="sw(5)">&#8987; التوقيت والسلوك</button>
  <button class="tab" onclick="sw(6)">&#128179; طرق الدفع</button>
  <button class="tab" onclick="sw(7)">&#128197; تحليل YTD</button>
  <button class="tab" onclick="sw(8)">&#127942; التقرير النهائي</button>
</div>

<div id="panes">
<div class="pane on" id="p0">
  <div class="st">ملخص أداء الفروع — {data.get('report_month','')}</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
    <thead><tr><th>الفرع</th><th>الإيرادات</th><th>المعاملات</th><th>م. الفاتورة</th><th>إجمالي الربح</th><th>هامش%</th><th>تكلفة البضاعة</th></tr></thead>
    <tbody>{branch_rows}</tbody>
    <tfoot><tr><td><strong>الإجمالي</strong></td><td class="num"><strong>{sar(total_rev)}</strong></td><td class="num"><strong>{num(total_txn)}</strong></td><td class="num"><strong>{sar(avg_ticket)}</strong></td><td class="num" style="color:#22c55e"><strong>{sar(total_gp)}</strong></td><td><strong>{pct(total_gp/total_rev*100) if total_rev else "0%"}</strong></td><td></td></tr></tfoot>
  </table></div>
  <div class="g2">
    <div class="card"><div class="st">مقارنة الإيرادات</div><div class="cw"><canvas id="ch_rev" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">توزيع الإيرادات</div><div class="cw"><canvas id="ch_pie" style="height:260px"></canvas></div></div>
  </div>
</div>

<div class="pane" id="p1">
  <div class="st">مؤشرات الأداء والنمو — {data.get('report_month','')}</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
    <thead><tr><th>الفرع</th><th>الإيرادات</th><th>نمو QoQ</th><th>نمو YoY</th><th>هامش%</th><th>المعاملات</th><th>م. الفاتورة</th></tr></thead>
    <tbody>{growth_rows}</tbody>
  </table></div>
  <div class="g2">
    <div class="card"><div class="st">مقارنة نمو QoQ للفروع</div><div class="cw"><canvas id="ch_qoq" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">الهامش الحقيقي لكل فرع</div><div class="cw"><canvas id="ch_margin" style="height:260px"></canvas></div></div>
  </div>
</div>

<div class="pane" id="p2">
  <div class="g3">
    <div class="kc" style="border-top:3px solid #22c55e"><div class="kl">إجمالي الإيرادات</div><div class="kv">{sar(total_rev)}</div></div>
    <div class="kc" style="border-top:3px solid #e92c30"><div class="kl">إجمالي المصاريف</div><div class="kv" style="color:#e92c30">{sar(total_expenses_sum)}</div></div>
    <div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">صافي الربح (بعد المصاريف)</div><div class="kv" style="color:#22c55e">{sar(total_gp - total_expenses_sum)}</div></div>
  </div>
  <div class="st">الربحية الحقيقية مع المصاريف</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
    <thead><tr><th>الفرع</th><th>الإيرادات</th><th>تكلفة البضاعة</th><th>إجمالي الربح</th><th>هامش%</th><th>المصاريف</th><th>صافي الربح</th></tr></thead>
    <tbody>{profit_rows}</tbody>
    <tfoot><tr><td><strong>الإجمالي</strong></td><td class="num"><strong>{sar(total_rev)}</strong></td><td></td><td class="num" style="color:#22c55e"><strong>{sar(total_gp)}</strong></td><td><strong>{pct(total_gp/total_rev*100) if total_rev else "0%"}</strong></td><td class="num" style="color:#e92c30"><strong>{sar(total_expenses_sum)}</strong></td><td class="num" style="color:#22c55e"><strong>{sar(total_gp-total_expenses_sum)}</strong></td></tr></tfoot>
  </table></div>
  <div class="st">تفاصيل المصاريف حسب الفرع</div>
  {exp_html if exp_html else '<div class="card" style="text-align:center;color:#64748b;padding:30px">لا توجد بيانات مصاريف للفترة المحددة</div>'}
</div>

<div class="pane" id="p3">
  <div style="display:flex;gap:14px;margin-bottom:18px;flex-wrap:wrap">
    <div class="del-card"><div class="label">إجمالي دخل التوصيل</div><div class="value" style="color:#2ba9ed">{sar(total_del)}</div></div>
    <div class="del-card"><div class="label">العمولات المستقطعة</div><div class="value" style="color:#e92c30">{sar(total_comm)}</div></div>
    <div class="del-card"><div class="label">المبالغ المستحقة لك &#128197;</div><div class="value" style="color:#22c55e">{sar(total_net)}</div></div>
    <div class="del-card"><div class="label">إجمالي الطلبات</div><div class="value">{num(sum(v.get("count",0) for v in delivery.values()))}</div></div>
  </div>
  <div class="st">تحليل تطبيقات التوصيل — {data.get('report_month','')}</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
    <thead><tr><th>التطبيق</th><th>عدد الطلبات</th><th>إجمالي الدخل</th><th>نسبة العمولة</th><th>المبلغ المستقطع</th><th>المبلغ المستحق لك</th></tr></thead>
    <tbody>{del_rows if del_rows else "<tr><td colspan='6' style='text-align:center;color:#64748b'>لا توجد بيانات تطبيقات التوصيل للفترة</td></tr>"}</tbody>
  </table></div>
  <div class="rec" style="background:#fffbeb;border-color:#fde68a;border-right-color:#f59e0b">
    <div class="rec-t">&#128276; ملاحظة</div>
    <div class="rec-b">نسبة "Online Paid" محسوبة بـ 25% (متوسط تطبيقات التوصيل في السوق السعودي مثل جاهز وهنقرستيشن). "Taker Wallet" بنسبة 20%. يُنصح بمراجعة العقود الفعلية لتحديث هذه النسب.</div>
  </div>
</div>

<div class="pane" id="p4">
  <div class="st">مصفوفة هندسة القائمة — تحليل المنتجات</div>
  {menu_eng}
</div>

<div class="pane" id="p5">
  <div class="card"><div class="st">خريطة حرارة الإيرادات — التوزيع الساعي</div>
    <div class="hlabel">{hlbls}</div>
    <div class="hmap">{hcells}</div>
    <div style="margin-top:10px;font-size:11px;color:#64748b">&#128313; أعلى ساعة: <strong style="color:#2ba9ed">{hourly.index(max(hourly)):02d}:00</strong> | {sar(max(hourly))}</div>
  </div>
  <div class="g2">
    <div class="card"><div class="st">أداء أيام الأسبوع</div><div class="dmap">{dcells}</div></div>
    <div class="card"><div class="st">التوزيع الساعي</div><div class="cw"><canvas id="ch_hourly" style="height:230px"></canvas></div></div>
  </div>
</div>

<div class="pane" id="p6">
  <div class="g2">
    <div class="card"><div class="st">توزيع طرق الدفع</div><div class="cw"><canvas id="ch_pay" style="height:280px"></canvas></div></div>
    <div class="card"><div class="st">مبالغ طرق الدفع</div><table class="dt"><thead><tr><th>طريقة الدفع</th><th>المبلغ</th><th>النسبة</th></tr></thead><tbody>{pay_rows}</tbody><tfoot><tr><td><strong>الإجمالي</strong></td><td class="num"><strong>{sar(sum(pay_totals.values()))}</strong></td><td class="num"><strong>100%</strong></td></tr></tfoot></table></div>
  </div>
</div>

<div class="pane" id="p7">
  <div class="st">مؤشرات YTD — من {data.get('ytd_from','')} إلى {data.get('ytd_to','')}</div>
  <div class="kgrid4">{ytd_kpis}</div>
  <div class="card" style="overflow-x:auto"><table class="dt">
    <thead><tr><th>الفرع</th><th>الإيرادات YTD</th><th>المعاملات</th><th>م. الفاتورة</th><th>إجمالي الربح</th><th>هامش%</th></tr></thead>
    <tbody>{ytd_rows}</tbody>
    <tfoot><tr><td><strong>الإجمالي</strong></td><td class="num"><strong>{sar(ytd_rev)}</strong></td><td class="num"><strong>{num(ytd_txn)}</strong></td><td class="num"><strong>{sar(round(ytd_rev/ytd_txn,1) if ytd_txn else 0)}</strong></td><td class="num" style="color:#22c55e"><strong>{sar(ytd_gp)}</strong></td><td><strong>{pct(ytd_margin)}</strong></td></tr></tfoot>
  </table></div>
  <div class="g2">
    <div class="card"><div class="st">تطور الإيرادات YTD</div><div class="cw"><canvas id="ch_ytd" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">مقارنة الشهري vs YTD</div><table class="dt"><thead><tr><th>الفرع</th><th>هذا الشهر</th><th>YTD</th><th>نسبة الشهر</th></tr></thead><tbody>{"".join([f'<tr><td><strong>{b["name"]}</strong></td><td class="num">{sar(b["total"])}</td><td class="num">{sar(ytd_map.get(b["name"],{{}}).get("total",0))}</td><td class="num" style="color:#2ba9ed">{pct(b["total"]/max(ytd_map.get(b["name"],{{}}).get("total",b["total"]),1)*100)}</td></tr>' for b in B])}</tbody></table></div>
  </div>
</div>

<div class="pane" id="p8">
  <div class="g2">
    <div>
      <div class="st">&#127942; التصنيف المركّب</div>
      <div class="card">{rank_rows}</div>
    </div>
    <div>
      <div class="st">&#129351; أعلى الفروع أداءً</div>
      {"".join([f'<div class="card" style="margin-bottom:8px;border-right:4px solid {COLORS[i%8]}"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:700">{MEDALS[i] if i<3 else str(i+1)+"."} {b["name"]}</span><span class="tag tg">{sar(b["total"])}</span></div><div style="margin-top:6px;font-size:11px;color:#64748b">هامش: {pct(b.get("gross_margin_real",0))} | الطلبات: {num(b.get("total_txn",0))} | م.الفاتورة: {sar(b.get("avg_ticket",0))}</div></div>' for i,b in enumerate(sorted(B,key=lambda x:-x["total"])[:4])])}
    </div>
  </div>
  <div class="st">&#128161; التوصيات المبنية على البيانات</div>
  <div class="rec gn"><div class="rec-t">&#127919; هندسة القائمة — فرصة فورية</div><div class="rec-b">منتجات علامات الاستفهام (هامش عالٍ + مبيعات منخفضة) تمثل فرصة ذهبية. تعزيز عرضها في القائمة وإضافتها للكومبو يرفع الإيراد بدون زيادة التكلفة.</div></div>
  <div class="rec bl"><div class="rec-t">&#8987; تحسين التوظيف حسب الذروة</div><div class="rec-b">خريطة الحرارة الساعية تكشف ساعات الذروة بدقة. تعديل جداول الموظفين يقلل التكلفة في الساعات المنخفضة ويحسّن الخدمة في الذروة.</div></div>
  <div class="rec rd"><div class="rec-t">&#128661; مراجعة عقود التوصيل</div><div class="rec-b">مقارنة نسب عمولة تطبيقات التوصيل والتفاوض للحصول على شروط أفضل يزيد صافي الإيراد من كل طلب توصيل.</div></div>
  <div class="exec">
    <strong>&#128203; الملخص التنفيذي — {data.get("report_month","")}</strong><br><br>
    حققت الشركة إيرادات <strong>{sar(total_rev)}</strong> عبر {len(B)} فروع بإجمالي ربح <strong>{sar(total_gp)}</strong> وهامش <strong>{pct(total_gp/total_rev*100) if total_rev else "0%"}</strong>.
    نُفّذت <strong>{num(total_txn)}</strong> معاملة بمتوسط فاتورة <strong>{sar(avg_ticket)}</strong>.
    إيرادات YTD: <strong>{sar(ytd_rev)}</strong> بهامش <strong>{pct(ytd_margin)}</strong>.
    دخل التوصيل: <strong>{sar(total_del)}</strong> | مستحق منها: <strong>{sar(total_net)}</strong>.
    إجمالي المصاريف: <strong>{sar(total_expenses_sum)}</strong>.
  </div>
</div>
</div><!-- /panes -->
</div><!-- /main -->

<script>
var C={COLS};
var DAYS=['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت'];
var B={B_JSON};
var YB={YB_JSON};
var HOURLY={H_JSON};
var DAILY={D_JSON};
var PAYMENTS={P_JSON};
var BASE={{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}}}};
var CH={{}};
function mk(id,cfg){{var c=document.getElementById(id);if(!c)return;if(CH[id])CH[id].destroy();CH[id]=new Chart(c,cfg);}}
function fmt(n){{return Math.abs(n)>=1e6?(n/1e6).toFixed(2)+'M':Math.abs(n)>=1e3?(n/1e3).toFixed(1)+'K':Math.round(n).toLocaleString();}}

function sw(i){{
  document.querySelectorAll('.tab').forEach(function(b,j){{b.classList.toggle('on',i===j);}});
  document.querySelectorAll('.pane').forEach(function(p,j){{p.classList.toggle('on',i===j);}});
  if(i===0)drawOv(); else if(i===1)drawGr(); else if(i===5)drawTm(); else if(i===6)drawPay(); else if(i===7)drawYTD();
}}

function drawOv(){{
  if(CH['ch_rev'])return;
  mk('ch_rev',{{type:'bar',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.total;}}),backgroundColor:C,borderRadius:6,borderSkipped:false}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return fmt(v);}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}}}}}}}}}});
  mk('ch_pie',{{type:'doughnut',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.total;}}),backgroundColor:C,borderWidth:2,borderColor:'#fff'}}]}},options:{{...BASE,cutout:'62%',plugins:{{legend:{{display:true,position:'bottom',labels:{{color:'#64748b',font:{{size:10}},boxWidth:10,padding:6}}}},tooltip:{{callbacks:{{label:function(ctx){{return ctx.label+': '+fmt(ctx.raw);}}}}}}}}}}}});
}}
function drawGr(){{
  if(CH['ch_qoq'])return;
  mk('ch_qoq',{{type:'bar',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.qoq||0;}}),backgroundColor:B.map(function(b){{return (b.qoq||0)>=0?'rgba(34,197,94,.8)':'rgba(233,44,48,.8)';}}),borderRadius:5}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return v+'%';}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}},afterDataLimits:function(s){{s.min=Math.min(s.min,-10);s.max=Math.max(s.max,15);}}}}}}}}}});
  mk('ch_margin',{{type:'bar',data:{{labels:B.map(function(b){{return b.name;}}),datasets:[{{data:B.map(function(b){{return b.gross_margin_real||0;}}),backgroundColor:B.map(function(b){{var rm=b.gross_margin_real||0;return rm>=75?'rgba(34,197,94,.8)':rm>=65?'rgba(245,158,11,.8)':'rgba(233,44,48,.8)';}}),borderRadius:5,indexAxis:'y'}}]}},options:{{...BASE,indexAxis:'y',scales:{{x:{{ticks:{{color:'#64748b',callback:function(v){{return v+'%';}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}},min:50}},y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}}}}}}}});
}}
function drawTm(){{
  if(CH['ch_hourly'])return;
  mk('ch_hourly',{{type:'line',data:{{labels:Array.from({{length:24}},function(_,h){{return (h<10?'0'+h:h)+':00';}}),datasets:[{{data:HOURLY,borderColor:'#2ba9ed',backgroundColor:'rgba(43,169,237,.1)',borderWidth:2,fill:true,tension:.4,pointRadius:2}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:9}}}},grid:{{color:'rgba(226,232,240,.8)'}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return fmt(v);}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}}}}}}}}}}});
}}
function drawPay(){{
  if(CH['ch_pay'])return;
  var keys=Object.keys(PAYMENTS),vals=keys.map(function(k){{return PAYMENTS[k];}});
  mk('ch_pay',{{type:'doughnut',data:{{labels:keys,datasets:[{{data:vals,backgroundColor:C.slice(0,keys.length),borderWidth:2,borderColor:'#fff'}}]}},options:{{...BASE,cutout:'55%',plugins:{{legend:{{display:true,position:'right',labels:{{color:'#64748b',font:{{size:11}},boxWidth:12}}}},tooltip:{{callbacks:{{label:function(ctx){{var tot=vals.reduce(function(a,b){{return a+b;}},0);return ctx.label+': '+fmt(ctx.raw)+' ('+((ctx.raw/tot*100).toFixed(1))+'%)';}}}}}}}}}}}}});
}}
function drawYTD(){{
  if(CH['ch_ytd'])return;
  var months={{}};
  YB.forEach(function(b){{if(b.monthly){{Object.entries(b.monthly).forEach(function(e){{months[e[0]]=(months[e[0]]||0)+e[1];}});}}}});
  var keys=Object.keys(months).sort();
  mk('ch_ytd',{{type:'bar',data:{{labels:keys,datasets:[{{data:keys.map(function(k){{return Math.round(months[k]);}}) ,backgroundColor:'rgba(43,169,237,.7)',borderRadius:5}}]}},options:{{...BASE,scales:{{x:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{display:false}}}},y:{{ticks:{{color:'#64748b',callback:function(v){{return fmt(v);}},font:{{size:10}}}},grid:{{color:'rgba(226,232,240,.8)'}}}}}}}}}}});
}}
drawOv();
</""" + """script>
</body>
</html>"""
    return html

try:
    with open('data.json','r',encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f'Warning: could not load data.json: {{e}}')
    data = {{'branches':[],'ytd_branches':[],'products':[],'hourly':[0]*24,'daily':[0]*7,
             'payment_totals':{{}},'delivery_apps':{{}},'expenses':{{}},'report_month':'—',
             'updated':'','date_from':'','date_to':'','ytd_from':'','ytd_to':''}}

html = build_html(data)
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print(f'index.html generated: {{len(html):,}} chars')
