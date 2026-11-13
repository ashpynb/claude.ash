// Renderiza 1 quadro por beat (a 75% do beat) e confere as camadas HTML: dentro da tela e sem sobreposição.
const {chromium}=require('playwright');(async()=>{const [url,pref]=process.argv.slice(2);const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto(url);await p.waitForFunction('window.pronto',{timeout:120000});const B=await p.evaluate('TEMPO.beats');const prob=[];
for(let i=0;i<B.length;i++){for(const f of [.35,.8]){const t=B[i].t0+(B[i].t1-B[i].t0)*f;await p.evaluate(t=>renderAt(t),t);
 const r=await p.evaluate(()=>{const sel=['#titulo','#num span','#tema','#chips span','#selo span','#card span','#leg','.etq'];const vis=[];
  for(const s of sel)document.querySelectorAll(s).forEach(e=>{let o=1,n=e;while(n&&n!==document.body){o*=+getComputedStyle(n).opacity;n=n.parentElement}if(o<.05||!e.textContent.trim())return;const q=e.getBoundingClientRect();vis.push({s,q:{l:q.left,r:q.right,t:q.top,b:q.bottom},txt:e.textContent.slice(0,20)})});
  const pr=[];vis.forEach(v=>{if(v.q.l<20||v.q.r>1060||v.q.t<0||v.q.b>1920)pr.push('fora da tela: '+v.s+' "'+v.txt+'" '+Math.round(v.q.l)+'..'+Math.round(v.q.r))});
  for(let a=0;a<vis.length;a++)for(let c=a+1;c<vis.length;c++){const A=vis[a].q,C=vis[c].q;if(vis[a].s===vis[c].s&&vis[a].s==='#chips span')continue;if(A.l<C.r&&C.l<A.r&&A.t<C.b&&C.t<A.b)pr.push('sobrepõe: '+vis[a].s+' x '+vis[c].s)}
  const leg=document.querySelector('#leg');const lh=parseFloat(getComputedStyle(leg).lineHeight);const nl=Math.round(leg.getBoundingClientRect().height/lh);if(nl>2)pr.push('legenda com '+nl+' linhas');return pr});
 r.forEach(x=>prob.push('beat '+i+' ('+f+'): '+x));
 if(f===.8)await p.screenshot({path:pref+String(i).padStart(2,'0')+'.jpg',type:'jpeg',quality:80})}}
console.log(prob.length?prob.join('\n'):'CSS ok: nada fora da tela nem sobreposto');await b.close()})();
