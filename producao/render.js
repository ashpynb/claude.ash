// Uso: node render.js pagina.html saida_dir [teste]
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const [pag,out,modo]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
p.on('pageerror',e=>{console.log('ERR',e.message);process.exitCode=1});p.on('console',m=>console.log('LOG',m.text()));
await p.goto('file://'+path.resolve(pag));await p.waitForTimeout(400);
const total=await p.evaluate('TOTAL');fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'eventos.json'),JSON.stringify(await p.evaluate('EVENTOS()')));
let ts=[];if(modo){const B=await p.evaluate('TEMPO.beats');ts=B.map(x=>x.t0+(x.t1-x.t0)*.7)}else for(let i=0;i<Math.round(total*30);i++)ts.push(i/30);
let i=0;for(const t of ts){await p.evaluate(t=>renderAt(t),t);await p.screenshot({path:path.join(out,`f${String(i++).padStart(5,'0')}.jpg`),type:'jpeg',quality:90})}
console.log('frames',i,'total',total);await b.close()})();
