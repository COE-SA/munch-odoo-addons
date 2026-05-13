import json

LOGO_SVG = '<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCABBASgDASIAAhEBAxEB/8QAHAABAAICAwEAAAAAAAAAAAAAAAYHBAUBAwgC/8QAOhAAAQMCAwUGAgcJAQAAAAAAAAECAwQFBhEhBxIxQVETIjJhkcGBsRQjQlJicaEWNENyc4KisuHw/8QAGgEBAAMBAQEAAAAAAAAAAAAAAAECBgcFBP/EAC0RAQABAwIEAwcFAAAAAAAAAAABAgMEBRESITGxBiKhEzJBUWFx4VKBkaLx/9oADAMBAAIRAxEAPwDxkAdtHTVFZVRUtLC+aeVyMjjYmbnOXgiITEbztCJmIjeXNHTVFZVxUlJC+eeZyMjjYmbnOXgiIXHX7OafCeyO83G4tZPepoY953FtO1ZWdxvn1X4JpxmWyHZzT4UpG3K5NZNepm953FtO1fsN8+q/BNOOw23Oa3Zded5yJmyNEzXivasNViaPFjFrvXo83DO0fLl37MVm69OTm28fHnycVO8/PnHp3U7hjCVLiTZ7G5m7DcIppOxmy46+F3l8vVFr640VVb62WjrIXQzxO3Xsdy/55lz7G3IuC2IioqpUSIuvDVDMx7hKmxJRb7N2G4RN+pmy0X8LvL5eqLz2jNm1fqor6b/w7/k+F6dQ0qxk40bXYojeP1cu/wDkqEBkXCjqbfWy0dZC6GeJ269juKf+6mOetExMbw5xVTVRVNNUbTAACVQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB20lPPV1UVLSwvmnlcjI42Nzc5y8ERD0rsh2cwYUpW3K5NZNepW6rxbTtX7LfPq74JpxiGyCTZ9hWlbc7niCimvUrdV3Xq2mav2W93j1X4JpxsR+03ArGOd+0NOuSZ5Ix6qv5d01mj4mNYiL16uni+Ebxy/PZiNezsvJmcfHt1cHxnaefp07/AGSS83Ohs9snuVyqGU9LA3ee93yTqq8ETmeXtqGPK7GVzyTfp7XA5fo1Nn/m/q5f04JzVedqOPK7GVzybv09rgcv0anz4/jf1cv6cE5qsMPi1jV5yZ9la9zv+HoaDoUYcRevRvcn0/LeYOxJW4buSVFOqyQPySeBV0kT2VOSl8WO60V5tsdfQSpJE/inNq82qnJUPNZvMHYlrcN3FKiBVkp35JPAq6PT2VOSmRzMOL0cVPvd3VvDHiavTK/YX53tT/X6x9PnH7xz629j3CNNiSj7SPdhuETfqZctHJ913l8vXOjLhR1NBWS0dZC6GeJ269jk1RS9oMdYWlhZIt1jjVzUVWPY5HN8l04kax7U4MxJR9pHeaaG4RN+ql3XZOT7rtOHyPlwr121PBXTO326ND4o03TtQpnKxb1EXPjHFHm9evfpKpwcqmSqmmnQ4PZcvAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG8tNFbK6H+I2Vqd9u/+qeRnLYaHLTtU/uIzTzSQTNlicrXtXRUJbabhHXQ8mytTvs908iY2VndGLjRS0U6xyJm1fC7k5DFJxW00VXAsMzc0XgvNF6oRG40UtFOsciZtXwuTg5BMJiWKbXC9huGI7tHbrdFvPdq96+GNvNzl6HGF7DcMRXaO3W6Lee7V718MbebnLyQ9H4Nwzb8L2ltFRN3pHZLPO5O9K7qvROicvURBMoxTbIcLsp42zy18sqNRHvSVGo5ea5ZafkaLHGDsB4VtS1VUtfJUPzSnp0qE3pHemiJzX3LAxxiq34VtS1VUqSTvzSnp0XvSO9kTmvvkeccRXq4X+6y3K5TLJM/RETwsbya1OSITKIa9yorlVEyTPh0OACqwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHZTzSQTNlicrXtXRTrAExtNwjroc9Gyt8bPdPI+cQMa61TK5qKrclavRc0IpTzSU8zZYnK17eCm/qbhHXWOdUybK1qb7PimqeRbdXZbewangjwR9IZExs01Q/tHonedloma+RIsb4pt+FbUtXVr2k780p6dF70rvZE5r75IQTAGKbfhbZXHV1a9pM+olSnp0XvSuzT0ROa8vRCrMSXu4YgustyuM3aSv0a1PCxvJrU5Ig3NuZiO9XC/wB1luVxm7SV+iInhY3k1qckQ1oBVYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7IeEn8i/NAAMit/cKD+m/8A3cYYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf//Z" alt="Compass of Excellence" style="height:44px;width:auto;filter:brightness(0)" onerror="this.style.display=\'none\'">'

def num(n):
    if abs(n)>=1e6: return f"{n/1e6:.2f}M"
    if abs(n)>=1e3: return f"{n/1e3:.1f}K"
    return f"{round(n):,}"
def sar(n): return "Ø±.Ø³ " + num(n)
def pct(n): return f"{float(n):.1f}%"
def dt_tag(v):
    arr = "&#9650;" if v>=0 else "&#9660;"
    cls = "tg" if v>=0 else "tr"
    return f'<span class="tag {cls}">{arr} {abs(float(v)):.1f}%</span>'

# âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# HTML template uses __PLACEHOLDER__ â no f-string escaping issues
# âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
HTML_TMPL = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ÙÙØ­Ø© Ø§ÙØªØ­ÙÙÙ Ø§ÙÙØ§ÙÙ - Ø´Ø±ÙØ© Ø¨ÙØµÙØ© Ø§ÙØªÙÙØ² Ø§ÙØªØ¬Ø§Ø±ÙØ©</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#f5f7fa;--bg2:#ffffff;--bg3:#f0f4f9;--bg4:#e2e8f0;--text:#1e293b;--text2:#64748b;--text3:#94a3b8;--blue:#2ba9ed;--red:#e92c30;--green:#22c55e;--gold:#f59e0b;--purple:#8b5cf6;--border:#e2e8f0}
body{font-family:'IBM Plex Sans Arabic',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;direction:rtl;font-size:14px}
.bar{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;height:62px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:50;box-shadow:0 1px 4px rgba(0,0,0,.07)}
.logo-wrap{display:flex;align-items:center;gap:14px}
.logo-wrap svg{height:44px;width:auto}
.title-area h1{font-size:14px;font-weight:700;color:var(--text);line-height:1.3}
.title-area p{font-size:11px;color:var(--text2)}
.badge{font-size:11px;background:#dcfce7;color:#166534;border:1px solid #bbf7d0;padding:4px 12px;border-radius:20px;font-weight:600}
.upd{font-size:11px;color:var(--text2);font-family:'IBM Plex Mono',monospace}
.main{padding:20px 24px;max-width:1440px;margin:0 auto}
.page-hdr{margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
.page-hdr h2{font-size:18px;font-weight:700}.page-hdr p{font-size:12px;color:var(--text2);margin-top:2px}
.per{font-size:11px;color:var(--blue);background:#eff8ff;border:1px solid #bae6fd;padding:4px 14px;border-radius:20px;font-weight:600}
.kgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}
.kgrid4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:14px}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.kc{background:var(--bg2);border-radius:12px;padding:18px 16px;box-shadow:0 1px 3px rgba(0,0,0,.06);border:1px solid var(--border)}
.kl{font-size:10px;color:var(--text2);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}
.kv{font-size:22px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text);line-height:1}
.ks{font-size:11px;color:var(--text2);margin-top:6px}
.tabs{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:4px;display:flex;gap:3px;margin-bottom:20px;overflow-x:auto;flex-wrap:wrap;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.tab{padding:8px 16px;background:none;border:none;cursor:pointer;font-size:12px;color:var(--text2);border-radius:8px;font-family:inherit;transition:all .2s;white-space:nowrap;font-weight:500}
.tab.on{background:#eff8ff;color:var(--blue);font-weight:700}
.tab:hover:not(.on){background:var(--bg3)}
.pane{display:none!important}.pane.on{display:block!important}
@keyframes fi{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:18px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.st{font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.st::after{content:'';flex:1;height:1px;background:var(--border)}
.cw{position:relative;width:100%}
table.dt{width:100%;border-collapse:collapse;font-size:12px}
table.dt th{padding:10px 12px;font-size:10px;font-weight:700;color:var(--text2);border-bottom:2px solid var(--border);text-align:right;white-space:nowrap;background:var(--bg3);text-transform:uppercase}
table.dt td{padding:10px 12px;border-bottom:1px solid var(--border);color:var(--text);vertical-align:middle}
table.dt tr:last-child td{border-bottom:none}
table.dt tr:hover td{background:var(--bg3)}
table.dt tfoot td{background:var(--bg3);font-weight:700;border-top:2px solid var(--border)}
.tag{display:inline-flex;align-items:center;gap:2px;font-size:10px;padding:2px 7px;border-radius:4px;font-weight:600;font-family:'IBM Plex Mono',monospace}
.tg{background:#dcfce7;color:#166534}.tr{background:#fee2e2;color:#991b1b}.tn{background:var(--bg4);color:var(--text2)}.tbl{background:#dbeafe;color:#1e40af}
.num{font-family:'IBM Plex Mono',monospace}
.hmap{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-top:6px}
.hcell{height:38px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:9px;color:var(--text2);cursor:default;font-family:monospace;font-weight:600}
.hlabel{display:grid;grid-template-columns:repeat(24,1fr);gap:3px;margin-bottom:4px}
.hlbl{font-size:9px;color:var(--text3);text-align:center}
.dmap{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:8px}
.dcell{border-radius:8px;padding:14px 6px;text-align:center;border:1px solid var(--border);background:var(--bg2)}
.dcell-lbl{font-size:10px;color:var(--text2);margin-bottom:6px;font-weight:600}
.dcell-val{font-size:14px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text)}
.rrow{display:flex;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)}
.rrow:last-child{border-bottom:none}
.rn{font-size:16px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text3);width:28px;text-align:center;flex-shrink:0}
.rnm{min-width:140px;font-size:13px;font-weight:600}
.rbb{flex:1;height:10px;background:var(--bg4);border-radius:5px;overflow:hidden}
.rbf{height:100%;border-radius:5px}
.rv{font-size:12px;font-family:'IBM Plex Mono',monospace;min-width:90px;text-align:left;color:var(--text2)}
.del-box{display:flex;gap:14px;margin-bottom:18px;flex-wrap:wrap}
.del-card{flex:1;min-width:180px;background:var(--bg2);border-radius:10px;padding:16px;border:1px solid var(--border);text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.del-card .dlbl{font-size:10px;color:var(--text2);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px}
.del-card .dval{font-size:20px;font-weight:700;font-family:'IBM Plex Mono',monospace}
.rec{padding:14px;background:var(--bg2);border-radius:10px;border:1px solid var(--border);border-right:4px solid var(--gold);margin-bottom:8px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.rec.gn{border-right-color:var(--green)}.rec.rd{border-right-color:var(--red)}.rec.bl{border-right-color:var(--blue)}
.rec-t{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px}
.rec-b{font-size:12px;color:var(--text2);line-height:1.7}
.exec{background:#eff8ff;border:1px solid #bae6fd;border-radius:10px;padding:16px;font-size:12px;color:var(--text2);line-height:1.9;margin-top:16px}
.exec strong{color:var(--text)}
.spin{display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:16px}
.sp{width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--blue);border-radius:50%;animation:sp .7s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
@media(max-width:900px){.kgrid,.kgrid4{grid-template-columns:1fr 1fr}.g2,.g3{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="bar">
  <div class="logo-wrap">__LOGO_SVG__
    <div class="title-area">
      <h1>ÙÙØ­Ø© Ø§ÙØªØ­ÙÙÙ Ø§ÙÙØ§ÙÙ - Ø´Ø±ÙØ© Ø¨ÙØµÙØ© Ø§ÙØªÙÙØ² Ø§ÙØªØ¬Ø§Ø±ÙØ© (Ø´ÙØ±Ù)</h1>
      <p>ØªÙØ±ÙØ± Ø´ÙØ± __REPORT_MONTH__ | __BRANCH_COUNT__ ÙØ±ÙØ¹ | Odoo POS</p>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:14px">
    <div class="badge">&#128197; __REPORT_MONTH__</div>
    <div class="upd">ØªØ­Ø¯ÙØ«: __UPDATED__</div>
  </div>
</div>
<div class="main">
<div class="page-hdr">
  <div><h2>Ø§ÙØªØ­ÙÙÙ Ø§ÙÙØ§ÙÙ Ø§ÙØ´ÙØ±Ù â __REPORT_MONTH__</h2>
  <p>__BRANCH_COUNT__ ÙØ±ÙØ¹ | __DATE_FROM__ Ø¥ÙÙ __DATE_TO__</p></div>
  <span class="per">&#128197; __DATE_FROM__ Ø¥ÙÙ __DATE_TO__</span>
</div>
<div class="kgrid">__KPIS__</div>
<div class="tabs">
  <button class="tab on" onclick="sw(0)">&#128202; Ø§ÙÙØ¸Ø±Ø© Ø§ÙØ¹Ø§ÙØ©</button>
  <button class="tab" onclick="sw(1)">&#128200; Ø§ÙØ£Ø¯Ø§Ø¡ ÙØ§ÙÙÙÙ</button>
  <button class="tab" onclick="sw(2)">&#128176; Ø§ÙØ±Ø¨Ø­ÙØ© ÙØ§ÙÙØµØ§Ø±ÙÙ</button>
  <button class="tab" onclick="sw(3)">&#128661; ØªØ·Ø¨ÙÙØ§Øª Ø§ÙØªÙØµÙÙ</button>
  <button class="tab" onclick="sw(4)">&#129409; ÙÙØ¯Ø³Ø© Ø§ÙÙØ§Ø¦ÙØ©</button>
  <button class="tab" onclick="sw(5)">&#8987; Ø§ÙØªÙÙÙØª ÙØ§ÙØ³ÙÙÙ</button>
  <button class="tab" onclick="sw(6)">&#128179; Ø·Ø±Ù Ø§ÙØ¯ÙØ¹</button>
  <button class="tab" onclick="sw(7)">&#128197; ØªØ­ÙÙÙ YTD</button>
  <button class="tab" onclick="sw(8)">&#127942; Ø§ÙØªÙØ±ÙØ± Ø§ÙÙÙØ§Ø¦Ù</button>
</div>
<div id="panes">
<div class="pane on" id="p0">
  <div class="st">ÙÙØ®Øµ Ø£Ø¯Ø§Ø¡ Ø§ÙÙØ±ÙØ¹ â __REPORT_MONTH__</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt"><thead><tr><th>Ø§ÙÙØ±Ø¹</th><th>Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</th><th>Ø§ÙÙØ¹Ø§ÙÙØ§Øª</th><th>Ù. Ø§ÙÙØ§ØªÙØ±Ø©</th><th>Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ±Ø¨Ø­</th><th>ÙØ§ÙØ´%</th><th>ØªÙÙÙØ© Ø§ÙØ¨Ø¶Ø§Ø¹Ø©</th></tr></thead>
    <tbody>__BRANCH_ROWS__</tbody>
    <tfoot><tr><td><strong>Ø§ÙØ¥Ø¬ÙØ§ÙÙ</strong></td><td class="num"><strong>__TOT_REV__</strong></td><td class="num"><strong>__TOT_TXN__</strong></td><td class="num"><strong>__AVG_TICKET__</strong></td><td class="num" style="color:var(--green)"><strong>__TOT_GP__</strong></td><td><strong>__TOT_MARGIN__</strong></td><td></td></tr></tfoot>
    </table>
  </div>
  <div class="g2">
    <div class="card"><div class="st">ÙÙØ§Ø±ÙØ© Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</div><div class="cw"><canvas id="ch_rev" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">ØªÙØ²ÙØ¹ Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</div><div class="cw"><canvas id="ch_pie" style="height:260px"></canvas></div></div>
  </div>
</div>
<div class="pane" id="p1">
  <div class="st">Ø§ÙØ£Ø¯Ø§Ø¡ ÙØ§ÙÙÙÙ â __REPORT_MONTH__</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt"><thead><tr><th>Ø§ÙÙØ±Ø¹</th><th>Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</th><th>ÙÙÙ QoQ</th><th>ÙÙÙ YoY</th><th>ÙØ§ÙØ´%</th><th>Ø§ÙÙØ¹Ø§ÙÙØ§Øª</th><th>Ù. Ø§ÙÙØ§ØªÙØ±Ø©</th></tr></thead>
    <tbody>__GROWTH_ROWS__</tbody>
    </table>
  </div>
  <div class="g2">
    <div class="card"><div class="st">ÙÙØ§Ø±ÙØ© ÙÙÙ QoQ</div><div class="cw"><canvas id="ch_qoq" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">Ø§ÙÙØ§ÙØ´ Ø§ÙØ­ÙÙÙÙ</div><div class="cw"><canvas id="ch_margin" style="height:260px"></canvas></div></div>
  </div>
</div>
<div class="pane" id="p2">
  <div class="g3">
    <div class="kc" style="border-top:3px solid #22c55e"><div class="kl">Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</div><div class="kv">__TOT_REV__</div></div>
    <div class="kc" style="border-top:3px solid #e92c30"><div class="kl">Ø¥Ø¬ÙØ§ÙÙ Ø§ÙÙØµØ§Ø±ÙÙ</div><div class="kv" style="color:var(--red)">__TOT_EXP__</div></div>
    <div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">ØµØ§ÙÙ Ø§ÙØ±Ø¨Ø­ Ø¨Ø¹Ø¯ Ø§ÙÙØµØ§Ø±ÙÙ</div><div class="kv" style="color:var(--green)">__NET_PROFIT__</div></div>
  </div>
  <div class="st">Ø§ÙØ±Ø¨Ø­ÙØ© Ø§ÙØ­ÙÙÙÙØ© ÙØ¹ Ø§ÙÙØµØ§Ø±ÙÙ</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt"><thead><tr><th>Ø§ÙÙØ±Ø¹</th><th>Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</th><th>ØªÙÙÙØ© Ø§ÙØ¨Ø¶Ø§Ø¹Ø©</th><th>Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ±Ø¨Ø­</th><th>ÙØ§ÙØ´%</th><th>Ø§ÙÙØµØ§Ø±ÙÙ</th><th>ØµØ§ÙÙ Ø§ÙØ±Ø¨Ø­</th></tr></thead>
    <tbody>__PROFIT_ROWS__</tbody>
    <tfoot><tr><td><strong>Ø§ÙØ¥Ø¬ÙØ§ÙÙ</strong></td><td class="num"><strong>__TOT_REV__</strong></td><td></td><td class="num" style="color:var(--green)"><strong>__TOT_GP__</strong></td><td><strong>__TOT_MARGIN__</strong></td><td class="num" style="color:var(--red)"><strong>__TOT_EXP__</strong></td><td class="num" style="color:var(--green)"><strong>__NET_PROFIT__</strong></td></tr></tfoot>
    </table>
  </div>
  <div class="st">ØªÙØ§ØµÙÙ Ø§ÙÙØµØ§Ø±ÙÙ Ø­Ø³Ø¨ Ø§ÙÙØ±Ø¹</div>
  __EXP_HTML__
</div>
<div class="pane" id="p3">
  <div class="del-box">
    <div class="del-card"><div class="dlbl">Ø¥Ø¬ÙØ§ÙÙ Ø¯Ø®Ù Ø§ÙØªÙØµÙÙ</div><div class="dval" style="color:var(--blue)">__DEL_TOTAL__</div></div>
    <div class="del-card"><div class="dlbl">Ø§ÙØ¹ÙÙÙØ§Øª Ø§ÙÙØ³ØªÙØ·Ø¹Ø©</div><div class="dval" style="color:var(--red)">__DEL_COMM__</div></div>
    <div class="del-card"><div class="dlbl">Ø§ÙÙØ¨Ø§ÙØº Ø§ÙÙØ³ØªØ­ÙØ© ÙÙ</div><div class="dval" style="color:var(--green)">__DEL_NET__</div></div>
    <div class="del-card"><div class="dlbl">Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ·ÙØ¨Ø§Øª</div><div class="dval">__DEL_CNT__</div></div>
  </div>
  <div class="st">ØªØ­ÙÙÙ ØªØ·Ø¨ÙÙØ§Øª Ø§ÙØªÙØµÙÙ â __REPORT_MONTH__</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt"><thead><tr><th>Ø§ÙØªØ·Ø¨ÙÙ</th><th>Ø¹Ø¯Ø¯ Ø§ÙØ·ÙØ¨Ø§Øª</th><th>Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ¯Ø®Ù</th><th>ÙØ³Ø¨Ø© Ø§ÙØ¹ÙÙÙØ©</th><th>Ø§ÙÙØ¨ÙØº Ø§ÙÙØ³ØªÙØ·Ø¹</th><th>Ø§ÙÙØ³ØªØ­Ù ÙÙ</th></tr></thead>
    <tbody>__DEL_ROWS__</tbody>
    </table>
  </div>
  <div class="rec" style="background:#fffbeb;border-color:#fde68a;border-right-color:var(--gold)">
    <div class="rec-t">&#128276; ÙÙØ§Ø­Ø¸Ø© Ø­ÙÙ ÙØ³Ø¨ Ø§ÙØ¹ÙÙÙØ©</div>
    <div class="rec-b">ÙØ³Ø¨Ø© "Online Paid" ÙØ­Ø³ÙØ¨Ø© Ø¨Ù 25% (ÙØªÙØ³Ø· ØªØ·Ø¨ÙÙØ§Øª Ø§ÙØªÙØµÙÙ â Ø¬Ø§ÙØ²Ø ÙÙÙØ±Ø³ØªÙØ´ÙØ Ø¥ÙØ®). "Taker Wallet" Ø¨ÙØ³Ø¨Ø© 20%. ÙÙÙØµØ­ Ø¨ÙØ±Ø§Ø¬Ø¹Ø© Ø§ÙØ¹ÙÙØ¯ Ø§ÙÙØ¹ÙÙØ© ÙØªØ­Ø¯ÙØ« ÙØ°Ù Ø§ÙÙØ³Ø¨.</div>
  </div>
</div>
<div class="pane" id="p4">
  <div class="st">ÙØµÙÙÙØ© ÙÙØ¯Ø³Ø© Ø§ÙÙØ§Ø¦ÙØ©</div>
  __MENU_ENG__
</div>
<div class="pane" id="p5">
  <div class="card"><div class="st">Ø®Ø±ÙØ·Ø© Ø­Ø±Ø§Ø±Ø© Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª â Ø§ÙØªÙØ²ÙØ¹ Ø§ÙØ³Ø§Ø¹Ù</div>
    <div class="hlabel">__HLBLS__</div>
    <div class="hmap">__HCELLS__</div>
    <div style="margin-top:10px;font-size:11px;color:var(--text2)">&#128313; Ø£Ø¹ÙÙ Ø³Ø§Ø¹Ø©: <strong style="color:var(--blue)">__PEAK_HOUR__</strong> | __PEAK_VAL__</div>
  </div>
  <div class="g2">
    <div class="card"><div class="st">Ø£Ø¯Ø§Ø¡ Ø£ÙØ§Ù Ø§ÙØ£Ø³Ø¨ÙØ¹</div><div class="dmap">__DCELLS__</div></div>
    <div class="card"><div class="st">Ø§ÙØªÙØ²ÙØ¹ Ø§ÙØ³Ø§Ø¹Ù</div><div class="cw"><canvas id="ch_hourly" style="height:230px"></canvas></div></div>
  </div>
</div>
<div class="pane" id="p6">
  <div class="g2">
    <div class="card"><div class="st">ØªÙØ²ÙØ¹ Ø·Ø±Ù Ø§ÙØ¯ÙØ¹</div><div class="cw"><canvas id="ch_pay" style="height:280px"></canvas></div></div>
    <div class="card"><div class="st">ÙØ¨Ø§ÙØº Ø·Ø±Ù Ø§ÙØ¯ÙØ¹</div>
      <table class="dt"><thead><tr><th>Ø·Ø±ÙÙØ© Ø§ÙØ¯ÙØ¹</th><th>Ø§ÙÙØ¨ÙØº</th><th>Ø§ÙÙØ³Ø¨Ø©</th></tr></thead>
      <tbody>__PAY_ROWS__</tbody>
      <tfoot><tr><td><strong>Ø§ÙØ¥Ø¬ÙØ§ÙÙ</strong></td><td class="num"><strong>__PAY_TOTAL__</strong></td><td class="num"><strong>100%</strong></td></tr></tfoot>
      </table>
    </div>
  </div>
</div>
<div class="pane" id="p7">
  <div class="st">ÙØ¤Ø´Ø±Ø§Øª YTD â ÙÙ __YTD_FROM__ Ø¥ÙÙ __YTD_TO__</div>
  <div class="kgrid4">__YTD_KPIS__</div>
  <div class="card" style="overflow-x:auto">
    <table class="dt"><thead><tr><th>Ø§ÙÙØ±Ø¹</th><th>Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª YTD</th><th>Ø§ÙÙØ¹Ø§ÙÙØ§Øª</th><th>Ù. Ø§ÙÙØ§ØªÙØ±Ø©</th><th>Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ±Ø¨Ø­</th><th>ÙØ§ÙØ´%</th></tr></thead>
    <tbody>__YTD_ROWS__</tbody>
    <tfoot><tr><td><strong>Ø§ÙØ¥Ø¬ÙØ§ÙÙ</strong></td><td class="num"><strong>__YTD_REV__</strong></td><td class="num"><strong>__YTD_TXN__</strong></td><td class="num"><strong>__YTD_AVG__</strong></td><td class="num" style="color:var(--green)"><strong>__YTD_GP__</strong></td><td><strong>__YTD_MARGIN__</strong></td></tr></tfoot>
    </table>
  </div>
  <div class="g2">
    <div class="card"><div class="st">ØªØ·ÙØ± Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª YTD</div><div class="cw"><canvas id="ch_ytd" style="height:260px"></canvas></div></div>
    <div class="card"><div class="st">ÙÙØ§Ø±ÙØ© Ø§ÙØ´ÙØ±Ù vs YTD</div>
      <table class="dt"><thead><tr><th>Ø§ÙÙØ±Ø¹</th><th>ÙØ°Ø§ Ø§ÙØ´ÙØ±</th><th>YTD</th><th>ÙØ³Ø¨Ø©</th></tr></thead>
      <tbody>__VS_ROWS__</tbody>
      </table>
    </div>
  </div>
</div>
<div class="pane" id="p8">
  <div class="g2">
    <div><div class="st">&#127942; Ø§ÙØªØµÙÙÙ Ø§ÙÙØ±ÙÙØ¨</div><div class="card">__RANK_ROWS__</div></div>
    <div>
      <div class="st">&#129351; Ø£Ø¹ÙÙ Ø§ÙÙØ±ÙØ¹</div>__TOP3__
      <div class="st" style="margin-top:12px">&#128161; Ø§ÙØªÙØµÙØ§Øª</div>
      <div class="rec gn"><div class="rec-t">&#127919; ÙÙØ¯Ø³Ø© Ø§ÙÙØ§Ø¦ÙØ© â ÙØ±ØµØ© ÙÙØ±ÙØ©</div><div class="rec-b">ØªØ¹Ø²ÙØ² ÙÙØªØ¬Ø§Øª "Ø¹ÙØ§ÙØ§Øª Ø§ÙØ§Ø³ØªÙÙØ§Ù" ÙØ±ÙØ¹ Ø§ÙØ¥ÙØ±Ø§Ø¯ Ø¨Ø¯ÙÙ Ø²ÙØ§Ø¯Ø© Ø§ÙØªÙÙÙØ©.</div></div>
      <div class="rec bl"><div class="rec-t">&#8987; Ø§ÙØªÙØ¸ÙÙ Ø§ÙØ°ÙÙ Ø­Ø³Ø¨ Ø§ÙØ°Ø±ÙØ©</div><div class="rec-b">Ø®Ø±ÙØ·Ø© Ø§ÙØ­Ø±Ø§Ø±Ø© ØªÙØ´Ù Ø³Ø§Ø¹Ø§Øª Ø§ÙØ°Ø±ÙØ© â Ø¬Ø¯ÙÙØ© Ø§ÙÙÙØ¸ÙÙÙ ÙÙÙØ§Ù ÙÙØ§.</div></div>
      <div class="rec rd"><div class="rec-t">&#128661; ÙØ±Ø§Ø¬Ø¹Ø© Ø¹ÙÙØ¯ Ø§ÙØªÙØµÙÙ</div><div class="rec-b">ÙÙØ§Ø±ÙØ© ÙØ³Ø¨ Ø§ÙØ¹ÙÙÙØ© ÙØ§ÙØªÙØ§ÙØ¶ ÙÙØ­ØµÙÙ Ø¹ÙÙ Ø´Ø±ÙØ· Ø£ÙØ¶Ù.</div></div>
    </div>
  </div>
  <div class="exec">
    <strong>&#128203; Ø§ÙÙÙØ®Øµ Ø§ÙØªÙÙÙØ°Ù â __REPORT_MONTH__</strong><br><br>
    Ø­ÙÙØª Ø§ÙØ´Ø±ÙØ© Ø¥ÙØ±Ø§Ø¯Ø§Øª <strong>__TOT_REV__</strong> Ø¹Ø¨Ø± __BRANCH_COUNT__ ÙØ±ÙØ¹
    Ø¨Ø¥Ø¬ÙØ§ÙÙ Ø±Ø¨Ø­ <strong>__TOT_GP__</strong> ÙÙØ§ÙØ´ <strong>__TOT_MARGIN__</strong>.
    ÙÙÙÙØ°Øª <strong>__TOT_TXN__</strong> ÙØ¹Ø§ÙÙØ© Ø¨ÙØªÙØ³Ø· ÙØ§ØªÙØ±Ø© <strong>__AVG_TICKET__</strong>.<br>
    Ø¥ÙØ±Ø§Ø¯Ø§Øª YTD: <strong>__YTD_REV__</strong> | Ø¯Ø®Ù Ø§ÙØªÙØµÙÙ: <strong>__DEL_TOTAL__</strong> (ÙØ³ØªØ­Ù: <strong>__DEL_NET__</strong>) | Ø¥Ø¬ÙØ§ÙÙ Ø§ÙÙØµØ§Ø±ÙÙ: <strong>__TOT_EXP__</strong>.
  </div>
</div>
</div>
</div>
<script>
var C = __COLORS_JSON__;
var B = __B_JSON__;
var YB = __YB_JSON__;
var HOURLY = __H_JSON__;
var DAILY = __D_JSON__;
var PAYMENTS = __P_JSON__;
var BASE = {responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}};
var CH = {};
function mk(id,cfg){var c=document.getElementById(id);if(!c)return;if(CH[id])CH[id].destroy();CH[id]=new Chart(c,cfg);}
function fmt(n){return Math.abs(n)>=1e6?(n/1e6).toFixed(2)+'M':Math.abs(n)>=1e3?(n/1e3).toFixed(1)+'K':Math.round(n).toLocaleString();}
function sw(i){
  try {
    document.querySelectorAll('.tab').forEach(function(b,j){b.className='tab'+(j===i?' on':'');});
    for(var j=0;j<=8;j++){var p=document.getElementById('p'+j);if(p)p.style.display=(j===i)?'block':'none';}
    if(i===0){setTimeout(drawOv,30);}
    else if(i===1){setTimeout(drawGr,30);}
    else if(i===5){setTimeout(drawTm,30);}
    else if(i===6){setTimeout(drawPay,30);}
    else if(i===7){setTimeout(drawYTD,30);}
  } catch(err){console.error('sw:',err);}
}
function drawOv(){
  try { var p0=document.getElementById("p0"); if(p0)p0.style.display="block"; } catch(e){}
  
  if(CH['ch_rev'])return;
  mk('ch_rev',{type:'bar',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.total;}),backgroundColor:C,borderRadius:6,borderSkipped:false}]},options:options_tmpscales:{x:{ticks:{color:'#64748b',font:{size:10}},grid:{display:false}},y:{ticks:{color:'#64748b',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(226,232,240,.8)'}}}}});
  mk('ch_pie',{type:'doughnut',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.total;}),backgroundColor:C,borderWidth:2,borderColor:'#fff'}]},options:options_tmpcutout:'62%',plugins:{legend:{display:true,position:'bottom',labels:{color:'#64748b',font:{size:10},boxWidth:10,padding:6}},tooltip:{callbacks:{label:function(ctx){return ctx.label+': '+fmt(ctx.raw);}}}}}});
}
function drawGr(){
  if(CH['ch_qoq'])return;
  mk('ch_qoq',{type:'bar',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.qoq||0;}),backgroundColor:B.map(function(b){return (b.qoq||0)>=0?'rgba(34,197,94,.8)':'rgba(233,44,48,.8)';}),borderRadius:5}]},options:options_tmpscales:{x:{ticks:{color:'#64748b',font:{size:10}},grid:{display:false}},y:{ticks:{color:'#64748b',callback:function(v){return v+'%';},font:{size:10}},grid:{color:'rgba(226,232,240,.8)'},afterDataLimits:function(s){s.min=Math.min(s.min,-10);s.max=Math.max(s.max,15);}}}}});
  mk('ch_margin',{type:'bar',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.gross_margin_real||0;}),backgroundColor:B.map(function(b){var rm=b.gross_margin_real||0;return rm>=75?'rgba(34,197,94,.8)':rm>=65?'rgba(245,158,11,.8)':'rgba(233,44,48,.8)';}),borderRadius:5,indexAxis:'y'}]},options:options_tmpindexAxis:'y',scales:{x:{ticks:{color:'#64748b',callback:function(v){return v+'%';},font:{size:10}},grid:{color:'rgba(226,232,240,.8)'},min:50},y:{ticks:{color:'#64748b',font:{size:10}},grid:{display:false}}}}});
}
function drawTm(){
  if(CH['ch_hourly'])return;
  mk('ch_hourly',{type:'line',data:{labels:Array.from({length:24},function(_,h){return (h<10?'0'+h:h)+':00';}),datasets:[{data:HOURLY,borderColor:'#2ba9ed',backgroundColor:'rgba(43,169,237,.1)',borderWidth:2,fill:true,tension:.4,pointRadius:2}]},options:options_tmpscales:{x:{ticks:{color:'#64748b',font:{size:9}},grid:{color:'rgba(226,232,240,.8)'}},y:{ticks:{color:'#64748b',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(226,232,240,.8)'}}}}}});
}
function drawPay(){
  if(CH['ch_pay'])return;
  var keys=Object.keys(PAYMENTS),vals=keys.map(function(k){return PAYMENTS[k];});
  mk('ch_pay',{type:'doughnut',data:{labels:keys,datasets:[{data:vals,backgroundColor:C.slice(0,keys.length),borderWidth:2,borderColor:'#fff'}]},options:options_tmpcutout:'55%',plugins:{legend:{display:true,position:'right',labels:{color:'#64748b',font:{size:11},boxWidth:12}},tooltip:{callbacks:{label:function(ctx){var tot=vals.reduce(function(a,b){return a+b;},0);return ctx.label+': '+fmt(ctx.raw)+' ('+((ctx.raw/tot*100).toFixed(1))+'%)';}}}}}}}); 
}
function drawYTD(){
  if(CH['ch_ytd'])return;
  var months={};
  YB.forEach(function(b){if(b.monthly){Object.entries(b.monthly).forEach(function(e){months[e[0]]=(months[e[0]]||0)+e[1];});}});
  var keys=Object.keys(months).sort();
  mk('ch_ytd',{type:'bar',data:{labels:keys,datasets:[{data:keys.map(function(k){return Math.round(months[k]);}),backgroundColor:'rgba(43,169,237,.7)',borderRadius:5}]},options:options_tmpscales:{x:{ticks:{color:'#64748b',font:{size:10}},grid:{display:false}},y:{ticks:{color:'#64748b',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(226,232,240,.8)'}}}}}}); 
}
// Init: show first pane
(function(){for(var j=0;j<=8;j++){var p=document.getElementById('p'+j);if(p)p.style.display=(j===0)?'block':'none';}})();
drawOv();
</script>
</body>
</html>"""

def build_html(data):
    B = data.get('branches', [])
    YB = data.get('ytd_branches', [])
    prods = data.get('products', [])
    hourly = data.get('hourly', [0]*24)
    daily = data.get('daily', [0]*7)
    pay_totals = data.get('payment_totals', {})
    delivery = data.get('delivery_apps', {})
    expenses = data.get('expenses', {})

    COLORS = ['#2ba9ed','#e92c30','#22c55e','#f59e0b','#8b5cf6','#06b6d4','#ec4899','#10b981']
    DAYS = ['Ø§ÙØ£Ø­Ø¯','Ø§ÙØ§Ø«ÙÙÙ','Ø§ÙØ«ÙØ§Ø«Ø§Ø¡','Ø§ÙØ£Ø±Ø¨Ø¹Ø§Ø¡','Ø§ÙØ®ÙÙØ³','Ø§ÙØ¬ÙØ¹Ø©','Ø§ÙØ³Ø¨Øª']
    DELIVERY_RATES = {'Online Paid': 25, 'Taker Wallet': 20}

    total_rev = sum(b['total'] for b in B)
    total_gp  = sum(b.get('gross_profit_real', b['total']*0.77) for b in B)
    total_txn = sum(b.get('total_txn', 0) for b in B)
    avg_tick  = round(total_rev/total_txn, 1) if total_txn else 0
    total_exp = sum(e.get('total',0) for e in expenses.values())
    net_prof  = total_gp - total_exp
    tot_margin = pct(total_gp/total_rev*100) if total_rev else '0%'

    ytd_rev = sum(b['total'] for b in YB)
    ytd_gp  = sum(b.get('gross_profit_real', b['total']*0.77) for b in YB)
    ytd_txn = sum(b.get('total_txn', 0) for b in YB)
    ytd_avg = round(ytd_rev/ytd_txn, 1) if ytd_txn else 0

    total_del  = sum(v.get('total',0) for v in delivery.values())
    total_comm = sum(round(v.get('total',0)*DELIVERY_RATES.get(k,25)/100) for k,v in delivery.items())
    total_net  = total_del - total_comm
    del_cnt    = sum(v.get('count',0) for v in delivery.values())

    # ââ KPI Cards âââââââââââââââââââââââââââââââââââââââââ
    kpis = ''.join([
        f'<div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</div><div class="kv">{sar(total_rev)}</div><div class="ks">{len(B)} ÙØ±ÙØ¹</div></div>',
        f'<div class="kc" style="border-top:3px solid #22c55e"><div class="kl">Ø¥Ø¬ÙØ§ÙÙ Ø§ÙØ£Ø±Ø¨Ø§Ø­</div><div class="kv">{sar(total_gp)}</div><div class="ks">{pct(total_gp/total_rev*100) if total_rev else "0%"} ÙØ§ÙØ´</div></div>',
        f'<div class="kc" style="border-top:3px solid #f59e0b"><div class="kl">Ø¥Ø¬ÙØ§ÙÙ Ø§ÙÙØ¹Ø§ÙÙØ§Øª</div><div class="kv">{num(total_txn)}</div><div class="ks">Ø·ÙØ¨</div></div>',
        f'<div class="kc" style="border-top:3px solid #8b5cf6"><div class="kl">ÙØªÙØ³Ø· Ø§ÙÙØ§ØªÙØ±Ø©</div><div class="kv">{sar(avg_tick)}</div><div class="ks">ÙÙÙ Ø·ÙØ¨</div></div>',
        f'<div class="kc" style="border-top:3px solid #e92c30"><div class="kl">Ø£ÙØ¶Ù ÙØ±Ø¹</div><div class="kv" style="font-size:15px;line-height:1.5">{B[0]["name"] if B else "-"}</div><div class="ks">{sar(B[0]["total"]) if B else "-"}</div></div>',
    ])

    # ââ Branch rows âââââââââââââââââââââââââââââââââââââââ
    branch_rows = ''.join([
        f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{COLORS[i%8]};margin-left:8px"></span><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td><td class="num">{num(b.get("total_txn",0))}</td>'
        f'<td class="num">{sar(b.get("avg_ticket",0))}</td>'
        f'<td class="num" style="color:#22c55e"><strong>{sar(b.get("gross_profit_real",0))}</strong></td>'
        f'<td><strong>{pct(b.get("gross_margin_real",0))}</strong></td>'
        f'<td class="num" style="color:#e92c30">{sar(b.get("cogs_real",0))}</td></tr>'
        for i,b in enumerate(B)
    ])

    # ââ Growth rows âââââââââââââââââââââââââââââââââââââââ
    growth_rows = ''.join([
        f'<tr><td><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:{COLORS[i%8]};margin-left:8px"></span><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td>'
        f'<td>{dt_tag(b.get("qoq",0))}</td>'
        f'<td>{"<span class=\"tag tn\">Ø¬Ø¯ÙØ¯</span>" if b.get("yoy",0)==0 else dt_tag(b.get("yoy",0))}</td>'
        f'<td><strong>{pct(b.get("gross_margin_real",0))}</strong></td>'
        f'<td class="num">{num(b.get("total_txn",0))}</td><td class="num">{sar(b.get("avg_ticket",0))}</td></tr>'
        for i,b in enumerate(B)
    ])

    # ââ Profit rows with expenses âââââââââââââââââââââââââ
    def get_branch_exp(bn):
        for k,e in expenses.items():
            if bn.lower() in k.lower() or k.lower() in bn.lower():
                return e.get('total',0)
        return 0

    profit_rows = ''.join([
        f'<tr><td><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td>'
        f'<td class="num" style="color:#e92c30">{sar(b.get("cogs_real",0))}</td>'
        f'<td class="num" style="color:#22c55e">{sar(b.get("gross_profit_real",0))}</td>'
        f'<td><strong>{pct(b.get("gross_margin_real",0))}</strong></td>'
        f'<td class="num" style="color:#e92c30">{sar(get_branch_exp(b["name"]))}</td>'
        f'<td class="num" style="color:#22c55e"><strong>{sar(b.get("gross_profit_real",0)-get_branch_exp(b["name"]))}</strong></td></tr>'
        for b in B
    ])

    # ââ Expenses detail âââââââââââââââââââââââââââââââââââ
    exp_html = ''
    for bn, edata in sorted(expenses.items()):
        total_e = edata.get('total', 0)
        items = edata.get('items', [])[:15]
        if not items: continue
        rows = ''.join([f'<tr><td style="color:#64748b">{it["account"]}</td><td class="num">{sar(it["amount"])}</td></tr>' for it in items])
        exp_html += f'<div class="card" style="margin-bottom:12px"><div class="st" style="color:#e92c30">{bn} â Ø¥Ø¬ÙØ§ÙÙ: {sar(total_e)}</div><table class="dt"><thead><tr><th>Ø¨ÙØ¯ Ø§ÙÙØµØ±ÙÙ</th><th>Ø§ÙÙØ¨ÙØº</th></tr></thead><tbody>{rows}</tbody><tfoot><tr style="background:#fef2f2"><td><strong>Ø¥Ø¬ÙØ§ÙÙ Ø§ÙÙØµØ§Ø±ÙÙ</strong></td><td class="num" style="color:#e92c30"><strong>{sar(total_e)}</strong></td></tr></tfoot></table></div>'
    if not exp_html:
        exp_html = '<div class="card" style="text-align:center;color:#64748b;padding:30px">ÙØ§ ØªÙØ¬Ø¯ Ø¨ÙØ§ÙØ§Øª ÙØµØ§Ø±ÙÙ ÙÙÙØªØ±Ø© Ø§ÙÙØ­Ø¯Ø¯Ø©</div>'

    # ââ Delivery rows âââââââââââââââââââââââââââââââââââââ
    del_rows = ''.join([
        f'<tr><td><strong>{m}</strong></td><td class="num">{num(v.get("count",0))} Ø·ÙØ¨</td>'
        f'<td class="num">{sar(v.get("total",0))}</td>'
        f'<td class="num" style="color:#64748b">{DELIVERY_RATES.get(m,25)}%</td>'
        f'<td class="num" style="color:#e92c30">{sar(round(v.get("total",0)*DELIVERY_RATES.get(m,25)/100))}</td>'
        f'<td class="num" style="color:#22c55e"><strong>{sar(v.get("total",0)-round(v.get("total",0)*DELIVERY_RATES.get(m,25)/100))}</strong></td></tr>'
        for m,v in delivery.items()
    ])
    if del_rows:
        del_rows += f'<tr style="background:#f0f9ff;font-weight:700"><td colspan="2"><strong>Ø§ÙØ¥Ø¬ÙØ§ÙÙ</strong></td><td class="num">{sar(total_del)}</td><td></td><td class="num" style="color:#e92c30">{sar(total_comm)}</td><td class="num" style="color:#22c55e">{sar(total_net)}</td></tr>'
    if not del_rows:
        del_rows = '<tr><td colspan="6" style="text-align:center;color:#64748b;padding:20px">ÙØ§ ØªÙØ¬Ø¯ Ø¨ÙØ§ÙØ§Øª ØªØ·Ø¨ÙÙØ§Øª Ø§ÙØªÙØµÙÙ ÙÙÙØªØ±Ø©</td></tr>'

    # ââ Menu Engineering ââââââââââââââââââââââââââââââââââ
    if prods:
        avg_r = sum(p['revenue'] for p in prods) / len(prods)
        avg_m = sum(p.get('margin_pct',0) for p in prods) / len(prods)
        nm = lambda p: p['name'].split('/')[-1].strip() or p['name']
        stars  = sorted([p for p in prods if p['revenue']>=avg_r and p.get('margin_pct',0)>=avg_m], key=lambda x:-x['revenue'])[:10]
        quest  = sorted([p for p in prods if p['revenue']<avg_r  and p.get('margin_pct',0)>=avg_m], key=lambda x:-x.get('margin_pct',0))[:10]
        plow   = sorted([p for p in prods if p['revenue']>=avg_r and p.get('margin_pct',0)<avg_m],  key=lambda x:-x['revenue'])[:10]
        dogs   = sorted([p for p in prods if p['revenue']<avg_r  and p.get('margin_pct',0)<avg_m],  key=lambda x:x.get('margin_pct',0))[:8]
        def ptbl(items, tc):
            rows = ''.join([f'<tr><td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:12px" title="{p["name"]}">{nm(p)}</td><td class="num">{sar(p["revenue"])}</td><td class="num">{num(p.get("qty",0))}</td><td><span class="tag {tc}">{pct(p.get("margin_pct",0))}</span></td></tr>' for p in items])
            return f'<div style="overflow-x:auto"><table class="dt" style="font-size:12px"><thead><tr><th>Ø§ÙÙÙØªØ¬</th><th>Ø§ÙØ¥ÙØ±Ø§Ø¯Ø§Øª</th><th>Ø§ÙÙÙÙØ©</th><th>Ø§ÙÙØ§ÙØ´</th></tr></thead><tbody>{rows}</tbody></table></div>'
        menu_eng = f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
<div class="card" style="border-top:4px solid #22c55e">
  <div style="background:#f0fdf4;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#166534">&#11088; ÙØ¬ÙÙ â ÙØ§ÙØ´ Ø¹Ø§ÙÙ + ÙØ¨ÙØ¹Ø§Øª Ø¹Ø§ÙÙØ©</div>
    <div style="font-size:11px;color:#166534;margin-top:2px">Ø­Ø§ÙØ¸ Ø¹ÙÙÙØ§ ÙØ¹Ø²Ø²ÙØ§ ÙÙ Ø§ÙÙØ§Ø¦ÙØ©</div>
  </div>{ptbl(stars,"tg")}</div>
<div class="card" style="border-top:4px solid #2ba9ed">
  <div style="background:#eff8ff;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#1e40af">&#10067; Ø¹ÙØ§ÙØ§Øª Ø§Ø³ØªÙÙØ§Ù â ÙØ§ÙØ´ Ø¹Ø§ÙÙ + ÙØ¨ÙØ¹Ø§Øª ÙÙØ®ÙØ¶Ø©</div>
    <div style="font-size:11px;color:#1e40af;margin-top:2px">Ø³ÙÙÙ Ø£ÙØ«Ø± ÙØ§Ø¹Ø±Ø¶ÙØ§ Ø¨Ø´ÙÙ Ø¨Ø§Ø±Ø²</div>
  </div>{ptbl(quest,"tbl")}</div>
<div class="card" style="border-top:4px solid #f59e0b">
  <div style="background:#fffbeb;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#92400e">&#128004; Ø£Ø¨ÙØ§Ø± Ø­ÙÙØ¨ â ÙØ§ÙØ´ ÙÙØ®ÙØ¶ + ÙØ¨ÙØ¹Ø§Øª Ø¹Ø§ÙÙØ©</div>
    <div style="font-size:11px;color:#92400e;margin-top:2px">Ø±Ø§Ø¬Ø¹ Ø§ÙØªØ³Ø¹ÙØ± ÙØ®ÙØ¶ ØªÙÙÙØ© Ø§ÙØ¥ÙØªØ§Ø¬</div>
  </div>{ptbl(plow,"tn")}</div>
<div class="card" style="border-top:4px solid #e92c30">
  <div style="background:#fef2f2;border-radius:8px;padding:10px;margin-bottom:12px">
    <div style="font-size:13px;font-weight:700;color:#991b1b">&#128021; Ø®Ø³Ø§Ø¦Ø± â ÙØ§ÙØ´ ÙÙØ®ÙØ¶ + ÙØ¨ÙØ¹Ø§Øª ÙÙØ®ÙØ¶Ø©</div>
    <div style="font-size:11px;color:#991b1b;margin-top:2px">ØªØ­ÙÙ ÙÙ Ø¥ÙØºØ§Ø¦ÙØ§ Ø£Ù ØªØ·ÙÙØ± ÙØµÙØªÙØ§</div>
  </div>{ptbl(dogs,"tr")}</div></div>"""
    else:
        menu_eng = '<div class="card" style="text-align:center;padding:40px;color:#64748b">ÙØ§ ØªÙØ¬Ø¯ Ø¨ÙØ§ÙØ§Øª ÙÙØªØ¬Ø§Øª</div>'

    # ââ Timing ââââââââââââââââââââââââââââââââââââââââââââ
    mH = max(hourly) if max(hourly)>0 else 1
    mD = max(daily)  if max(daily)>0  else 1
    hcells = ''.join([f'<div class="hcell" style="background:rgba(43,169,237,{0.05+v/mH*0.85:.2f})" title="{h:02d}:00 - {sar(v)}">{num(v) if v>mH*0.3 else ""}</div>' for h,v in enumerate(hourly)])
    hlbls  = ''.join([f'<div class="hlbl">{h:02d}</div>' for h in range(24)])
    dcells = ''.join([f'<div class="dcell" style="background:rgba(43,169,237,{0.08+v/mD*0.25:.2f})"><div class="dcell-lbl">{DAYS[d]}</div><div class="dcell-val">{num(v)}</div></div>' for d,v in enumerate(daily)])
    peak_h = hourly.index(max(hourly))
    peak_v = max(hourly)

    # ââ Payments ââââââââââââââââââââââââââââââââââââââââââ
    pay_sum = sum(pay_totals.values()) or 1
    pay_rows = ''.join([f'<tr><td>{m}</td><td class="num">{sar(v)}</td><td class="num">{pct(v/pay_sum*100)}</td></tr>' for m,v in sorted(pay_totals.items(), key=lambda x:-x[1])])

    # ââ YTD âââââââââââââââââââââââââââââââââââââââââââââââ
    ytd_kpis = ''.join([
        f'<div class="kc" style="border-top:3px solid #2ba9ed"><div class="kl">Ø¥ÙØ±Ø§Ø¯Ø§Øª YTD</div><div class="kv">{sar(ytd_rev)}</div><div class="ks">{data.get("ytd_from","")} - {data.get("ytd_to","")}</div></div>',
        f'<div class="kc" style="border-top:3px solid #22c55e"><div class="kl">Ø£Ø±Ø¨Ø§Ø­ YTD</div><div class="kv">{sar(ytd_gp)}</div><div class="ks">{pct(ytd_gp/ytd_rev*100) if ytd_rev else "0%"} ÙØ§ÙØ´</div></div>',
        f'<div class="kc" style="border-top:3px solid #f59e0b"><div class="kl">ÙØ¹Ø§ÙÙØ§Øª YTD</div><div class="kv">{num(ytd_txn)}</div><div class="ks">Ø·ÙØ¨</div></div>',
        f'<div class="kc" style="border-top:3px solid #8b5cf6"><div class="kl">ÙØªÙØ³Ø· Ø§ÙÙØ§ØªÙØ±Ø© YTD</div><div class="kv">{sar(ytd_avg)}</div><div class="ks">ÙÙÙ Ø·ÙØ¨</div></div>',
    ])

    ytd_map = {b['name']:b for b in YB}
    ytd_rows = ''.join([
        f'<tr><td><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(ytd_map.get(b["name"],{}).get("total",0))}</td>'
        f'<td class="num">{num(ytd_map.get(b["name"],{}).get("total_txn",0))}</td>'
        f'<td class="num">{sar(ytd_map.get(b["name"],{}).get("avg_ticket",0))}</td>'
        f'<td class="num" style="color:#22c55e">{sar(ytd_map.get(b["name"],{}).get("gross_profit_real",0))}</td>'
        f'<td><strong>{pct(ytd_map.get(b["name"],{}).get("gross_margin_real",0))}</strong></td></tr>'
        for b in B
    ])
    vs_rows = ''.join([
        f'<tr><td><strong>{b["name"]}</strong></td>'
        f'<td class="num">{sar(b["total"])}</td>'
        f'<td class="num">{sar(ytd_map.get(b["name"],{}).get("total",0))}</td>'
        f'<td class="num" style="color:#2ba9ed">{pct(b["total"]/max(ytd_map.get(b["name"],{}).get("total",b["total"]),1)*100)}</td></tr>'
        for b in B
    ])

    # ââ Rankings ââââââââââââââââââââââââââââââââââââââââââ
    max_t = B[0]['total'] if B else 1
    rank_rows = ''.join([
        f'<div class="rrow"><div class="rn">{i+1}</div><div class="rnm">{b["name"]}</div>'
        f'<div class="rbb"><div class="rbf" style="width:{int(b["total"]/max_t*100)}%;background:{COLORS[i%8]}"></div></div>'
        f'<div class="rv">{sar(b["total"])}</div>'
        f'{dt_tag(b.get("qoq",0))}'
        f'<span class="tag {"tg" if b.get("gross_margin_real",0)>=75 else "tn"}">{pct(b.get("gross_margin_real",0))}</span></div>'
        for i,b in enumerate(sorted(B, key=lambda x:-x['total']))
    ])
    MEDALS = ['&#127941;','&#129352;','&#127942;','4.']
    top3 = ''.join([
        f'<div class="card" style="margin-bottom:8px;border-right:4px solid {COLORS[i%8]}"><div style="display:flex;justify-content:space-between"><span style="font-weight:700">{MEDALS[i] if i<4 else ""} {b["name"]}</span><span class="tag tg">{sar(b["total"])}</span></div><div style="font-size:11px;color:#64748b;margin-top:6px">ÙØ§ÙØ´: {pct(b.get("gross_margin_real",0))} | Ø§ÙØ·ÙØ¨Ø§Øª: {num(b.get("total_txn",0))} | Ù.Ø§ÙÙØ§ØªÙØ±Ø©: {sar(b.get("avg_ticket",0))}</div></div>'
        for i,b in enumerate(sorted(B, key=lambda x:-x['total'])[:4])
    ])

    # ââ Replace all placeholders ââââââââââââââââââââââââââ
    html = HTML_TMPL
    replacements = {
        '__LOGO_SVG__':     LOGO_SVG,
        '__REPORT_MONTH__': data.get('report_month','â'),
        '__BRANCH_COUNT__': str(len(B)),
        '__UPDATED__':      data.get('updated',''),
        '__DATE_FROM__':    data.get('date_from',''),
        '__DATE_TO__':      data.get('date_to',''),
        '__YTD_FROM__':     data.get('ytd_from',''),
        '__YTD_TO__':       data.get('ytd_to',''),
        '__KPIS__':         kpis,
        '__BRANCH_ROWS__':  branch_rows,
        '__GROWTH_ROWS__':  growth_rows,
        '__PROFIT_ROWS__':  profit_rows,
        '__EXP_HTML__':     exp_html,
        '__TOT_REV__':      sar(total_rev),
        '__TOT_TXN__':      num(total_txn),
        '__AVG_TICKET__':   sar(avg_tick),
        '__TOT_GP__':       sar(total_gp),
        '__TOT_MARGIN__':   tot_margin,
        '__TOT_EXP__':      sar(total_exp),
        '__NET_PROFIT__':   sar(net_prof),
        '__DEL_TOTAL__':    sar(total_del),
        '__DEL_COMM__':     sar(total_comm),
        '__DEL_NET__':      sar(total_net),
        '__DEL_CNT__':      num(del_cnt),
        '__DEL_ROWS__':     del_rows,
        '__MENU_ENG__':     menu_eng,
        '__HLBLS__':        hlbls,
        '__HCELLS__':       hcells,
        '__PEAK_HOUR__':    f'{peak_h:02d}:00',
        '__PEAK_VAL__':     sar(peak_v),
        '__DCELLS__':       dcells,
        '__PAY_ROWS__':     pay_rows,
        '__PAY_TOTAL__':    sar(sum(pay_totals.values())),
        '__YTD_KPIS__':     ytd_kpis,
        '__YTD_ROWS__':     ytd_rows,
        '__VS_ROWS__':      vs_rows,
        '__YTD_REV__':      sar(ytd_rev),
        '__YTD_TXN__':      num(ytd_txn),
        '__YTD_AVG__':      sar(ytd_avg),
        '__YTD_GP__':       sar(ytd_gp),
        '__YTD_MARGIN__':   pct(ytd_gp/ytd_rev*100) if ytd_rev else '0%',
        '__RANK_ROWS__':    rank_rows,
        '__TOP3__':         top3,
        '__COLORS_JSON__':  json.dumps(COLORS),
        '__B_JSON__':       json.dumps(B, default=str),
        '__YB_JSON__':      json.dumps(YB, default=str),
        '__H_JSON__':       json.dumps(hourly),
        '__D_JSON__':       json.dumps(daily),
        '__P_JSON__':       json.dumps(pay_totals),
    }
    for k, v in replacements.items():
        html = html.replace(k, v)
    return html

# ââ Main ââââââââââââââââââââââââââââââââââââââââââââââââââ
try:
    with open('data.json','r',encoding='utf-8') as f:
        data = json.load(f)
    print(f'data.json loaded: {len(data.get("branches",[]))} branches')
except Exception as e:
    print(f'Warning: {e}')
    data = {'branches':[],'ytd_branches':[],'products':[],'hourly':[0]*24,'daily':[0]*7,
            'payment_totals':{},'delivery_apps':{},'expenses':{},'report_month':'â',
            'updated':'','date_from':'','date_to':'','ytd_from':'','ytd_to':''}

html = build_html(data)
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print(f'index.html generated: {len(html):,} chars')
