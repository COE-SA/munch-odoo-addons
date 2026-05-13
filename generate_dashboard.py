import json

def build_html():
    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Munch Bakery - لوحة التحليل المالي</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></""" + """script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0d1117;--bg2:#161b22;--bg3:#21262d;--bg4:#30363d;--text:#e6edf3;--text2:#8b949e;--gold:#f0b429;--green:#3fb950;--red:#f85149;--blue:#58a6ff;--purple:#a371f7;--border:#30363d}
body{font-family:'IBM Plex Sans Arabic',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;direction:rtl;font-size:14px}
.bar{background:var(--bg2);border-bottom:1px solid var(--border);padding:0 24px;height:54px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:50}
.live-b{font-size:11px;background:rgba(63,185,80,.12);color:var(--green);border:1px solid rgba(63,185,80,.25);padding:3px 10px;border-radius:20px;display:flex;align-items:center;gap:5px}
.dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.upd{font-size:11px;color:var(--text2);font-family:'IBM Plex Mono',monospace}
.main{padding:20px 24px;max-width:1400px;margin:0 auto}
.hdr{margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}
.hdr h2{font-size:20px;font-weight:700}.hdr p{font-size:12px;color:var(--text2);margin-top:3px}
.per{font-size:12px;color:var(--gold);background:rgba(240,180,41,.1);border:1px solid rgba(240,180,41,.2);padding:4px 12px;border-radius:20px}
.kgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px}
.kc{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:14px 16px;position:relative;overflow:hidden}
.kc::before{content:'';position:absolute;top:0;right:0;width:3px;height:100%}
.kc.g::before{background:var(--gold)}.kc.gn::before{background:var(--green)}.kc.bl::before{background:var(--blue)}.kc.rd::before{background:var(--red)}.kc.pu::before{background:var(--purple)}
.kl{font-size:10px;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.kv{font-size:22px;font-weight:700;font-family:'IBM Plex Mono',monospace;line-height:1}
.ks{font-size:11px;margin-top:5px}.ks.up{color:var(--green)}.ks.n{color:var(--text2)}
.tabs{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:4px;display:flex;gap:3px;margin-bottom:18px;overflow-x:auto;flex-wrap:wrap}
.tab{padding:7px 14px;background:none;border:none;cursor:pointer;font-size:12px;color:var(--text2);border-radius:8px;font-family:inherit;transition:all .2s;white-space:nowrap}
.tab.on{background:var(--bg3);color:var(--text);font-weight:500}
.pane{display:none}.pane.on{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:14px}
.st{font-size:11px;font-weight:600;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.st::after{content:'';flex:1;height:1px;background:var(--border)}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.cw{position:relative;width:100%}
.leg{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:10px}
.li{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2)}
.ld{width:9px;height:9px;border-radius:2px;flex-shrink:0}
table.dt{width:100%;border-collapse:collapse;font-size:12px}
table.dt th{padding:8px 10px;font-size:10px;font-weight:600;color:var(--text2);border-bottom:1px solid var(--border);text-align:right;white-space:nowrap}
table.dt td{padding:8px 10px;border-bottom:1px solid var(--bg3);color:var(--text);vertical-align:middle}
table.dt tr:last-child td{border-bottom:none}
table.dt tr:hover td{background:rgba(255,255,255,.02)}
.tag{display:inline-flex;align-items:center;gap:2px;font-size:10px;padding:2px 6px;border-radius:3px;font-weight:500;font-family:'IBM Plex Mono',monospace}
.tg{background:rgba(63,185,80,.12);color:var(--green)}.tr{background:rgba(248,81,73,.12);color:var(--red)}.tn{background:var(--bg4);color:var(--text2)}.tbl{background:rgba(88,166,255,.12);color:var(--blue)}
.num{font-family:'IBM Plex Mono',monospace}
.hmap{display:grid;grid-template-columns:repeat(24,1fr);gap:2px;margin-top:8px}
.hcell{height:32px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;color:rgba(255,255,255,.7)}
.hlabel{display:grid;grid-template-columns:repeat(24,1fr);gap:2px;margin-bottom:4px}
.hlbl{font-size:9px;color:var(--text2);text-align:center}
.dmap{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-top:8px}
.dcell{border-radius:6px;padding:10px 6px;text-align:center;font-size:11px}
.dcell-lbl{font-size:10px;color:var(--text2);margin-bottom:4px}
.dcell-val{font-size:13px;font-weight:600;font-family:'IBM Plex Mono',monospace}
.rrow{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--bg3)}
.rrow:last-child{border-bottom:none}
.rn{font-size:16px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text2);width:24px;text-align:center;flex-shrink:0}
.rnm{min-width:130px;font-size:12px;font-weight:500}
.rbb{flex:1;height:6px;background:var(--bg4);border-radius:3px;overflow:hidden}
.rbf{height:100%;border-radius:3px}
.rv{font-size:11px;font-family:'IBM Plex Mono',monospace;min-width:60px;text-align:left;color:var(--text2)}
.ri{display:flex;gap:12px;padding:10px;background:var(--bg3);border-radius:8px;border:1px solid var(--border);margin-bottom:6px}
.rrank{font-size:18px;font-weight:700;font-family:'IBM Plex Mono',monospace;color:var(--text2);min-width:24px}
.rb h4{font-size:12px;font-weight:600;margin-bottom:3px}
.rb p{font-size:11px;color:var(--text2);line-height:1.6}
.rec{padding:12px;background:var(--bg3);border-radius:8px;border:1px solid var(--border);border-right:3px solid var(--gold);margin-bottom:6px}
.rec.gn{border-right-color:var(--green)}.rec.rd{border-right-color:var(--red)}.rec.bl{border-right-color:var(--blue)}
.rec-t{font-size:12px;font-weight:600;margin-bottom:3px}
.rec-b{font-size:11px;color:var(--text2);line-height:1.6}
.exec{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:14px;font-size:12px;color:var(--text2);line-height:1.8;margin-top:14px}
.exec strong{color:var(--text)}
.spin{display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:14px}
.sp{width:34px;height:34px;border:3px solid var(--border);border-top-color:var(--gold);border-radius:50%;animation:sp .7s linear infinite}
@keyframes sp{to{transform:rotate(360deg)}}
.mr{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--bg3);font-size:12px}
.mr:last-child{border-bottom:none}
.mr span:first-child{color:var(--text2)}
.mr span:last-child{font-family:'IBM Plex Mono',monospace;font-weight:500}
@media(max-width:900px){.kgrid{grid-template-columns:1fr 1fr}.g2{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="bar">
<div style="display:flex;align-items:center;gap:10px;font-size:15px;font-weight:600">
  <span>&#x1F9C1;</span><span>Munch Bakery - لوحة التحليل المالي</span>
</div>
<div style="display:flex;align-items:center;gap:14px">
  <div class="live-b"><span class="dot"></span>تحديث تلقائي كل ساعة</div>
  <div class="upd" id="upd">-</div>
</div>
</div>
<div class="main" id="app">
<div class="spin"><div class="sp"></div><div style="color:var(--text2)">جارٍ تحميل البيانات...</div></div>
</div>
<script>
var C=['#f0b429','#3fb950','#58a6ff','#f85149','#a371f7','#ff9500','#00d4ff','#ff6b9d'];
var DAYS=['الأحد','الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت'];
var MA=['يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر'];
var D={},B=[],CH={};
function fmt(n){return Math.abs(n)>=1e6?(n/1e6).toFixed(2)+'M':Math.abs(n)>=1e3?(n/1e3).toFixed(1)+'K':Math.round(n).toLocaleString();}
function fs(n){return 'ر.س '+fmt(n);}
function fp(n){return parseFloat(n).toFixed(1)+'%';}
function dt(v){return '<span class="tag '+(v>=0?'tg':'tr')+'">'+(v>=0?'&#9650;':'&#9660;')+' '+Math.abs(v).toFixed(1)+'%</span>';}
function mk(id,cfg){var c=document.getElementById(id);if(!c)return;if(CH[id])CH[id].destroy();CH[id]=new Chart(c,cfg);return CH[id];}
var BASE={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}}};

function load(){
  fetch('data.json?t='+Date.now()).then(function(r){return r.json();}).then(function(data){
    D=data; B=D.branches||[];
    document.getElementById('upd').textContent='آخر تحديث: '+D.updated;
    var now=new Date(),m12=[],ml=[];
    for(var i=11;i>=0;i--){
      var d=new Date(now.getFullYear(),now.getMonth()-i,1);
      m12.push(d.toISOString().slice(0,7));
      var p=d.toISOString().slice(0,7).split('-');
      ml.push(MA[parseInt(p[1])-1]+" '"+p[0].slice(2));
    }
    D._m12=m12; D._ml=ml;
    var mx=B[0]?B[0].total:1;
    B.forEach(function(b){
      var v=m12.map(function(m){return b.monthly&&b.monthly[m]?b.monthly[m]:0;});
      var q4=v.slice(-3).reduce(function(s,x){return s+x;},0);
      var q3=v.slice(-6,-3).reduce(function(s,x){return s+x;},0);
      var q1=v.slice(0,3).reduce(function(s,x){return s+x;},0);
      b.qoq=q3>0?parseFloat(((q4-q3)/q3*100).toFixed(1)):0;
      b.yoy=q1>0?parseFloat(((q4-q1)/q1*100).toFixed(1)):0;
      b.rm=b.gross_margin_real?b.gross_margin_real:(b.cogs_real?b.gross_margin_real:77);
      b.score=Math.round((b.total/mx)*45+(b.rm/90)*35+(b.qoq>0?Math.min(b.qoq/10,1)*20:0));
    });
    var tR=B.reduce(function(s,b){return s+b.total;},0);
    var tT=B.reduce(function(s,b){return s+(b.total_txn||0);},0);
    var tG=B.reduce(function(s,b){return s+(b.gross_profit_real||(b.total*.77));},0);
    var bM=[].concat(B).sort(function(a,z){return z.rm-a.rm;})[0];
    var khtml='<div class="kgrid">';
    khtml+='<div class="kc g"><div class="kl">اجمالي الايرادات</div><div class="kv">'+fs(tR)+'</div><div class="ks n">'+B.length+' فروع</div></div>';
    khtml+='<div class="kc gn"><div class="kl">الارباح الحقيقية</div><div class="kv">'+fs(tG)+'</div><div class="ks up">&#9650; '+fp(tG/tR*100)+' هامش</div></div>';
    khtml+='<div class="kc bl"><div class="kl">اجمالي المعاملات</div><div class="kv">'+fmt(tT)+'</div><div class="ks n">طلب</div></div>';
    khtml+='<div class="kc rd"><div class="kl">متوسط الفاتورة</div><div class="kv">'+fs(tT>0?tR/tT:0)+'</div><div class="ks n">لكل طلب</div></div>';
    khtml+='<div class="kc pu"><div class="kl">اعلى هامش ربح</div><div class="kv" style="font-size:14px;line-height:1.5">'+(bM?bM.name:'-')+'</div><div class="ks up">'+fp(bM?bM.rm:0)+'</div></div>';
    khtml+='</div>';
    var tabs='<div class="tabs">';
    tabs+='<button class="tab on" onclick="sw(0)">&#128202; نظرة عامة</button>';
    tabs+='<button class="tab" onclick="sw(1)">&#128200; الاداء والنمو</button>';
    tabs+='<button class="tab" onclick="sw(2)">&#128176; الربحية الحقيقية</button>';
    tabs+='<button class="tab" onclick="sw(3)">&#129409; هندسة القائمة</button>';
    tabs+='<button class="tab" onclick="sw(4)">&#8987; التوقيت والسلوك</button>';
    tabs+='<button class="tab" onclick="sw(5)">&#128179; طرق الدفع</button>';
    tabs+='<button class="tab" onclick="sw(6)">&#127942; التصنيف والتقرير</button>';
    tabs+='</div>';
    document.getElementById('app').innerHTML='<div class="hdr"><div><h2>لوحة التحليل المالي - Munch Bakery</h2><p>'+B.length+' فروع | بيانات لايف من Odoo POS</p></div><span class="per">&#128197; '+D.date_from+' - '+D.date_to+'</span></div>'+khtml+tabs+'<div id="panes"></div>';
    buildPane(0);
  }).catch(function(e){
    document.getElementById('app').innerHTML='<div style="text-align:center;padding:60px;color:var(--red)">خطأ: '+e.message+'</div>';
  });
}

function sw(i){document.querySelectorAll('.tab').forEach(function(b,j){b.classList.toggle('on',i===j);});buildPane(i);}
function buildPane(i){var pc=document.getElementById('panes');pc.innerHTML='';var p=document.createElement('div');p.className='pane on';pc.appendChild(p);[p0,p1,p2,p3,p4,p5,p6][i](p);}

function p0(el){
  var m12=D._m12,ml=D._ml;
  var legH=B.map(function(b,i){return '<div class="li"><span class="ld" style="background:'+C[i%8]+'"></span>'+b.name+'</div>';}).join('');
  var rows=B.map(function(b){return '<tr><td><strong>'+b.name+'</strong></td><td class="num">'+fs(b.total)+'</td><td class="num">'+fmt(b.total_txn||0)+'</td><td class="num">'+fs(b.avg_ticket||0)+'</td></tr>';}).join('');
  el.innerHTML='<div class="card"><div class="st">الايرادات الشهرية لكل فرع</div><div class="leg">'+legH+'</div><div class="cw"><canvas id="cm" style="height:280px"></canvas></div></div><div class="g2"><div class="card"><div class="st">اجمالي الايرادات</div><div class="cw"><canvas id="ct" style="height:220px"></canvas></div></div><div class="card"><div class="st">الايرادات vs الطلبات</div><table class="dt"><thead><tr><th>الفرع</th><th>الايرادات</th><th>الطلبات</th><th>م. الفاتورة</th></tr></thead><tbody>'+rows+'</tbody></table></div></div>';
  mk('cm',{type:'line',data:{labels:ml,datasets:B.map(function(b,i){return{label:b.name,data:m12.map(function(m){return Math.round(b.monthly&&b.monthly[m]?b.monthly[m]:0);}),borderColor:C[i%8],backgroundColor:C[i%8]+'15',borderWidth:2,pointRadius:3,tension:.4,fill:false};})},options:{...BASE,scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}});
  mk('ct',{type:'bar',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.total;}),backgroundColor:C,borderRadius:5,borderSkipped:false}]},options:{...BASE,scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{display:false}},y:{ticks:{color:'#8b949e',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}});
}

function p1(el){
  var rows=B.map(function(b,i){
    var m=b.qoq>75?'<span class="tag tg">&#8593;ممتاز</span>':b.qoq>65?'<span class="tag tbl">جيد</span>':'<span class="tag tr">&#8595;ضعيف</span>';
    return '<tr><td><span style="display:inline-block;width:7px;height:7px;border-radius:2px;background:'+C[i%8]+';margin-left:7px"></span><strong>'+b.name+'</strong></td><td class="num">'+fs(b.total)+'</td><td><strong>'+fp(b.rm)+'</strong></td><td class="num" style="color:var(--red)">'+fs(b.cogs_real||0)+'</td><td class="num">'+fs(b.avg_ticket||0)+'</td><td>'+dt(b.qoq)+'</td><td>'+(b.yoy===0?'<span class="tag tn">جديد</span>':dt(b.yoy))+'</td></tr>';
  }).join('');
  var anom=B.filter(function(b){return b.qoq<-5||b.rm<60;}).map(function(b){
    return '<div class="card" style="border-right:3px solid var(--red)"><div style="font-size:12px;font-weight:600;color:var(--red);margin-bottom:6px">&#9888;&#65039; '+b.name+'</div>'+(b.qoq<-5?'<div class="mr"><span>تراجع QoQ</span><span style="color:var(--red)">'+fp(b.qoq)+'</span></div>':'')+(b.rm<60?'<div class="mr"><span>هامش منخفض</span><span style="color:var(--red)">'+fp(b.rm)+'</span></div>':'')+'</div>';
  }).join('');
  el.innerHTML='<div class="card"><div class="st">نمو QoQ وYoY</div><div class="leg"><div class="li"><span class="ld" style="background:#f0b429"></span>QoQ</div><div class="li"><span class="ld" style="background:#58a6ff"></span>YoY</div></div><div class="cw"><canvas id="ch" style="height:260px"></canvas></div></div><div class="st">التحليل العمودي</div><div class="card" style="overflow-x:auto"><table class="dt"><thead><tr><th>الفرع</th><th>الايرادات</th><th>هامش حقيقي%</th><th>COGS حقيقية</th><th>م. الفاتورة</th><th>QoQ</th><th>YoY</th></tr></thead><tbody>'+rows+'</tbody></table></div><div class="st">&#9888;&#65039; الشواذ والانحرافات</div>'+(anom||'<div class="card" style="text-align:center;color:var(--text2);padding:20px">&#9989; لا توجد شواذ كبيرة</div>');
  mk('ch',{type:'bar',data:{labels:B.map(function(b){return b.name;}),datasets:[{label:'QoQ',data:B.map(function(b){return b.qoq;}),backgroundColor:'#f0b429',borderRadius:4},{label:'YoY',data:B.map(function(b){return b.yoy===0?null:b.yoy;}),backgroundColor:'#58a6ff',borderRadius:4}]},options:{...BASE,scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e',callback:function(v){return v+'%';},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'},afterDataLimits:function(s){s.min=Math.min(s.min,-12);s.max=Math.max(s.max,15);}}}}});
}

function p2(el){
  var rows=[].concat(B).sort(function(a,b){return b.score-a.score;}).map(function(b){
    return '<tr><td><strong>'+b.name+'</strong></td><td class="num">'+fs(b.total)+'</td><td class="num" style="color:var(--red)">'+fs(b.cogs_real||Math.round(b.total*.225))+'</td><td class="num" style="color:var(--green)"><strong>'+fs(b.gross_profit_real||Math.round(b.total*.77))+'</strong></td><td><strong>'+fp(b.rm)+'</strong></td><td class="num">'+fmt(b.total_txn||0)+'</td><td class="num">'+fs(b.avg_ticket||0)+'</td><td><span class="tag '+(b.score>=70?'tg':b.score>=50?'tbl':'tr')+'">'+b.score+'</span></td></tr>';
  }).join('');
  el.innerHTML='<div class="g2"><div class="card"><div class="st">الهامش الحقيقي لكل فرع</div><div class="cw"><canvas id="cmar" style="height:260px"></canvas></div></div><div class="card"><div class="st">توزيع الارباح الحقيقية</div><div class="cw"><canvas id="cpie" style="height:260px"></canvas></div></div></div><div class="st">جدول الربحية الكامل</div><div class="card" style="overflow-x:auto"><table class="dt"><thead><tr><th>الفرع</th><th>الايرادات</th><th>COGS</th><th>اجمالي الربح</th><th>هامش%</th><th>الطلبات</th><th>م.الفاتورة</th><th>نقاط</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  mk('cmar',{type:'bar',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.rm;}),backgroundColor:B.map(function(b){return b.rm>=75?'#3fb950':b.rm>=65?'#f0b429':'#f85149';}),borderRadius:5,indexAxis:'y'}]},options:{...BASE,indexAxis:'y',scales:{x:{ticks:{color:'#8b949e',callback:function(v){return v+'%';},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'},min:50},y:{ticks:{color:'#8b949e',font:{size:10}},grid:{display:false}}}}});
  mk('cpie',{type:'doughnut',data:{labels:B.map(function(b){return b.name;}),datasets:[{data:B.map(function(b){return b.gross_profit_real||Math.round(b.total*.77);}),backgroundColor:C,borderWidth:0}]},options:{...BASE,cutout:'60%',plugins:{legend:{display:false},tooltip:{callbacks:{label:function(ctx){return ctx.label+': '+fs(ctx.raw);}}}}}});
}

function p3(el){
  var prods=D.products||[];
  var avgR=prods.reduce(function(s,p){return s+p.revenue;},0)/Math.max(prods.length,1);
  var avgM=prods.reduce(function(s,p){return s+p.margin_pct;},0)/Math.max(prods.length,1);
  function nm(p){return p.name.split('/').pop()||p.name;}
  var stars=prods.filter(function(p){return p.revenue>=avgR&&p.margin_pct>=avgM;}).sort(function(a,b){return b.revenue-a.revenue;}).slice(0,8);
  var quest=prods.filter(function(p){return p.revenue<avgR&&p.margin_pct>=avgM;}).sort(function(a,b){return b.margin_pct-a.margin_pct;}).slice(0,8);
  var plow=prods.filter(function(p){return p.revenue>=avgR&&p.margin_pct<avgM;}).sort(function(a,b){return b.revenue-a.revenue;}).slice(0,8);
  var dogs=prods.filter(function(p){return p.revenue<avgR&&p.margin_pct<avgM;}).sort(function(a,b){return a.margin_pct-b.margin_pct;}).slice(0,6);
  function tbl(items,cols){return '<table class="dt"><thead><tr>'+cols.map(function(c){return '<th>'+c+'</th>';}).join('')+'</tr></thead><tbody>'+items.map(function(p){return '<tr><td>'+nm(p)+'</td><td class="num">'+fs(p.revenue)+'</td><td><span class="tag tg">'+fp(p.margin_pct)+'</span></td></tr>';}).join('')+'</tbody></table>';}
  el.innerHTML='<div class="card"><div class="st">مصفوفة هندسة القائمة</div><div class="cw"><canvas id="cme" style="height:300px"></canvas></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px"><div style="background:rgba(63,185,80,.08);border:1px solid rgba(63,185,80,.2);border-radius:6px;padding:8px;font-size:11px"><strong style="color:var(--green)">&#11088; نجوم</strong> - هامش عالٍ + مبيعات عالية</div><div style="background:rgba(88,166,255,.08);border:1px solid rgba(88,166,255,.2);border-radius:6px;padding:8px;font-size:11px"><strong style="color:var(--blue)">&#10067; استفهام</strong> - هامش عالٍ + مبيعات منخفضة</div><div style="background:rgba(240,180,41,.08);border:1px solid rgba(240,180,41,.2);border-radius:6px;padding:8px;font-size:11px"><strong style="color:var(--gold)">&#128004; ابقار حلوب</strong> - هامش منخفض + مبيعات عالية</div><div style="background:rgba(248,81,73,.08);border:1px solid rgba(248,81,73,.2);border-radius:6px;padding:8px;font-size:11px"><strong style="color:var(--red)">&#128021; خسائر</strong> - هامش منخفض + مبيعات منخفضة</div></div></div><div class="g2"><div class="card"><div class="st">&#11088; نجوم</div><table class="dt"><thead><tr><th>المنتج</th><th>ايرادات</th><th>هامش%</th></tr></thead><tbody>'+stars.map(function(p){return '<tr><td>'+nm(p)+'</td><td class="num">'+fs(p.revenue)+'</td><td><span class="tag tg">'+fp(p.margin_pct)+'</span></td></tr>';}).join('')+'</tbody></table></div><div class="card"><div class="st">&#10067; علامات استفهام</div><table class="dt"><thead><tr><th>المنتج</th><th>هامش%</th><th>ايرادات</th></tr></thead><tbody>'+quest.map(function(p){return '<tr><td>'+nm(p)+'</td><td><span class="tag tbl">'+fp(p.margin_pct)+'</span></td><td class="num">'+fs(p.revenue)+'</td></tr>';}).join('')+'</tbody></table></div></div><div class="g2"><div class="card"><div class="st">&#128004; ابقار حلوب</div><table class="dt"><thead><tr><th>المنتج</th><th>ايرادات</th><th>هامش%</th></tr></thead><tbody>'+plow.map(function(p){return '<tr><td>'+nm(p)+'</td><td class="num">'+fs(p.revenue)+'</td><td><span class="tag tn">'+fp(p.margin_pct)+'</span></td></tr>';}).join('')+'</tbody></table></div><div class="card"><div class="st">&#128021; خسائر</div><table class="dt"><thead><tr><th>المنتج</th><th>هامش%</th><th>ايرادات</th></tr></thead><tbody>'+dogs.map(function(p){return '<tr><td>'+nm(p)+'</td><td><span class="tag tr">'+fp(p.margin_pct)+'</span></td><td class="num">'+fs(p.revenue)+'</td></tr>';}).join('')+'</tbody></table></div></div>';
  mk('cme',{type:'scatter',data:{datasets:[
    {label:'&#11088; نجوم',data:stars.map(function(p){return{x:p.revenue,y:p.margin_pct,label:nm(p)};}),backgroundColor:'rgba(63,185,80,.7)',borderColor:'#3fb950',pointRadius:7},
    {label:'&#10067; استفهام',data:quest.map(function(p){return{x:p.revenue,y:p.margin_pct,label:nm(p)};}),backgroundColor:'rgba(88,166,255,.7)',borderColor:'#58a6ff',pointRadius:7},
    {label:'&#128004; حلوب',data:plow.map(function(p){return{x:p.revenue,y:p.margin_pct,label:nm(p)};}),backgroundColor:'rgba(240,180,41,.7)',borderColor:'#f0b429',pointRadius:7},
    {label:'&#128021; خسائر',data:dogs.map(function(p){return{x:p.revenue,y:p.margin_pct,label:nm(p)};}),backgroundColor:'rgba(248,81,73,.7)',borderColor:'#f85149',pointRadius:7}
  ]},options:{...BASE,plugins:{legend:{display:true,position:'top',labels:{color:'#8b949e',font:{size:11},usePointStyle:true}},tooltip:{callbacks:{label:function(ctx){return ctx.raw.label+': '+fs(ctx.raw.x)+' | '+ctx.raw.y+'%';}}}},scales:{x:{title:{display:true,text:'الايرادات',color:'#8b949e'},ticks:{color:'#8b949e',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}},y:{title:{display:true,text:'هامش %',color:'#8b949e'},ticks:{color:'#8b949e',callback:function(v){return v+'%';},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}});
}

function p4(el){
  var hourly=D.hourly||new Array(24).fill(0);
  var daily=D.daily||new Array(7).fill(0);
  var mH=Math.max.apply(null,hourly.concat([1]));
  var mD=Math.max.apply(null,daily.concat([1]));
  var hcells=hourly.map(function(v,h){var op=0.1+v/mH*0.9;return '<div class="hcell" style="background:rgba(240,180,41,'+op+')" title="'+h+':00 - '+fs(v)+'">'+(v>mH*0.3?fmt(v):'')+'</div>';}).join('');
  var hlbls=Array.from({length:24},function(_,h){return '<div class="hlbl">'+(h<10?'0'+h:h)+'</div>';}).join('');
  var dcells=daily.map(function(v,d){return '<div class="dcell" style="background:rgba(240,180,41,'+(0.05+v/mD*0.25)+')"><div class="dcell-lbl">'+DAYS[d]+'</div><div class="dcell-val">'+fmt(v)+'</div></div>';}).join('');
  el.innerHTML='<div class="card"><div class="st">خريطة حرارة ساعية</div><div class="hlabel">'+hlbls+'</div><div class="hmap">'+hcells+'</div><div style="margin-top:8px;font-size:11px;color:var(--text2)">اعلى ساعة: <strong style="color:var(--gold)">'+hourly.indexOf(Math.max.apply(null,hourly))+':00</strong> | '+fs(Math.max.apply(null,hourly))+'</div></div><div class="g2"><div class="card"><div class="st">اداء ايام الاسبوع</div><div class="dmap">'+dcells+'</div></div><div class="card"><div class="st">مقارنة الايام</div><div class="cw"><canvas id="cdaily" style="height:200px"></canvas></div></div></div><div class="card"><div class="st">التوزيع الساعي</div><div class="cw"><canvas id="chourly" style="height:200px"></canvas></div></div>';
  mk('cdaily',{type:'bar',data:{labels:DAYS,datasets:[{data:daily,backgroundColor:daily.map(function(v){return 'rgba(240,180,41,'+(0.3+v/mD*0.7)+')';}),borderRadius:5}]},options:{...BASE,scales:{x:{ticks:{color:'#8b949e',font:{size:10}},grid:{display:false}},y:{ticks:{color:'#8b949e',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}});
  mk('chourly',{type:'line',data:{labels:Array.from({length:24},function(_,h){return (h<10?'0'+h:h)+':00';}),datasets:[{data:hourly,borderColor:'#f0b429',backgroundColor:'rgba(240,180,41,.1)',borderWidth:2,fill:true,tension:.4,pointRadius:2}]},options:{...BASE,scales:{x:{ticks:{color:'#8b949e',font:{size:9}},grid:{color:'rgba(48,54,61,.5)'}},y:{ticks:{color:'#8b949e',callback:function(v){return fmt(v);},font:{size:10}},grid:{color:'rgba(48,54,61,.5)'}}}}});
}

function p5(el){
  var pT=D.payment_totals||{},pM=Object.keys(pT);
  var pC={'Mada Card':'#3fb950','Visa':'#58a6ff','Cash':'#f0b429'};
  function gc(m,i){return pC[m]||C[i%8];}
  var tot=Object.values(pT).reduce(function(s,v){return s+v;},0);
  var rows=pM.map(function(m,i){return '<div class="mr"><span style="display:flex;align-items:center;gap:6px"><span style="width:9px;height:9px;border-radius:2px;background:'+gc(m,i)+';display:inline-block"></span>'+m+'</span><span>'+fs(pT[m])+' <span class="tag tn">'+fp(pT[m]/tot*100)+'</span></span></div>';}).join('');
  var trows=B.map(function(b){var pays=b.payments||{};var t=Object.values(pays).reduce(function(s,v){return s+v;},0);return '<tr><td><strong>'+b.name+'</strong></td>'+pM.map(function(m){return '<td class="num">'+(pays[m]?fp(pays[m]/Math.max(t,1)*100):'-')+'</td>';}).join('')+'<td class="num">'+fs(t)+'</td></tr>';}).join('');
  el.innerHTML='<div class="g2"><div class="card"><div class="st">توزيع طرق الدفع (اجمالي)</div><div class="cw"><canvas id="cpay" style="height:240px"></canvas></div></div><div class="card"><div class="st">مبالغ طرق الدفع</div>'+rows+'</div></div><div class="st">طرق الدفع لكل فرع</div><div class="card" style="overflow-x:auto"><table class="dt"><thead><tr><th>الفرع</th>'+pM.map(function(m){return '<th>'+m+'</th>';}).join('')+'<th>اجمالي</th></tr></thead><tbody>'+trows+'</tbody></table></div>';
  mk('cpay',{type:'doughnut',data:{labels:pM,datasets:[{data:pM.map(function(m){return pT[m]||0;}),backgroundColor:pM.map(function(m,i){return gc(m,i);}),borderWidth:0}]},options:{...BASE,cutout:'60%',plugins:{legend:{display:true,position:'right',labels:{color:'#8b949e',font:{size:11},usePointStyle:true}},tooltip:{callbacks:{label:function(ctx){return ctx.label+': '+fs(ctx.raw)+' ('+fp(ctx.raw/tot*100)+')';}}}}}}); 
}

function p6(el){
  var srt=[].concat(B).sort(function(a,b){return b.score-a.score;});
  var tR=B.reduce(function(s,b){return s+b.total;},0);
  var tG=B.reduce(function(s,b){return s+(b.gross_profit_real||(b.total*.77));},0);
  var tT=B.reduce(function(s,b){return s+(b.total_txn||0);},0);
  var rnk=srt.map(function(b,i){return '<div class="rrow"><div class="rn">'+(i+1)+'</div><div class="rnm">'+b.name+'</div><div class="rbb"><div class="rbf" style="width:'+b.score+'%;background:'+C[B.indexOf(b)%8]+'"></div></div><div class="rv">'+b.score+'pts</div>'+dt(b.qoq)+'<span class="tag '+(b.rm>=75?'tg':b.rm>=65?'tbl':'tr')+'">'+fp(b.rm)+'</span></div>';}).join('');
  var medals=['&#127941;','&#129352;','&#127942;'];
  var top3=srt.slice(0,3).map(function(b,i){return '<div class="ri"><div class="rrank">'+medals[i]+'</div><div class="rb"><h4>'+b.name+'</h4><p>الايرادات: <strong>'+fs(b.total)+'</strong> | هامش: <strong>'+fp(b.rm)+'</strong> | QoQ: '+dt(b.qoq)+'</p></div></div>';}).join('');
  var worst=srt.slice(-2).reverse().map(function(b,i){return '<div class="ri" style="border-right:3px solid var(--red)"><div class="rrank" style="color:var(--red)">'+(i+1)+'</div><div class="rb"><h4>'+b.name+'</h4><p>هامش: <strong>'+fp(b.rm)+'</strong>'+(b.qoq<0?' | QoQ: '+dt(b.qoq):'')+' | اجمالي: <strong>'+fs(b.total)+'</strong></p></div></div>';}).join('');
  el.innerHTML='<div class="g2"><div><div class="st">&#127942; التصنيف المركّب</div><div class="card">'+rnk+'</div></div><div><div class="st">&#127941; اعلى 3 فروع</div>'+top3+'<div class="st" style="margin-top:14px">&#9888;&#65039; يحتاج تدخلاً</div>'+worst+'</div></div><div class="st">&#128161; التوصيات</div><div class="rec gn"><div class="rec-t">&#127919; هندسة القائمة - فرصة فورية</div><div class="rec-b">منتجات علامات الاستفهام تملك هامش عالٍ لكن مبيعات منخفضة - تعزيز عرضها يرفع الايراد.</div></div><div class="rec bl"><div class="rec-t">&#8987; تحسين التوظيف حسب ساعات الذروة</div><div class="rec-b">خريطة الحرارة الساعية تكشف الذروة بدقة - تعديل الجداول يقلل التكلفة التشغيلية.</div></div>'+(B.some(function(b){return b.qoq<-5;})?'<div class="rec rd"><div class="rec-t">&#9888;&#65039; تدخل عاجل</div><div class="rec-b">فروع بتراجع QoQ تتطلب مراجعة تشغيلية فورية.</div></div>':'')+'<div class="exec"><strong>&#128203; الملخص التنفيذي</strong><br><br>اجمالي الايرادات <strong>'+fs(tR)+'</strong> | الربح الحقيقي <strong>'+fs(tG)+'</strong> | هامش <strong>'+fp(tG/tR*100)+'</strong><br>الطلبات <strong>'+fmt(tT)+'</strong> | متوسط الفاتورة <strong>'+fs(tT>0?tR/tT:0)+'</strong><br>الفرع الاول: <strong>'+srt[0].name+'</strong> بنقاط '+srt[0].score+'</div>';
}

load();
</""" + """script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(build_html())
print('index.html generated OK')
