// Uso: node render_http.js http://127.0.0.1:8765/pagina.html saida_dir [teste]
// Para páginas com módulos ES (three.js + GLTFLoader): precisam de servidor http, não file://.
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const [url,out,modo]=process.argv.slice(2);
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
p.on('pageerror',e=>{console.log('ERR',e.message);process.exitCode=1});p.on('console',m=>{if(m.type()==='error')console.log('LOG',m.text())});
await p.goto(url);await p.waitForFunction('window.pronto===true',{timeout:180000});
const total=await p.evaluate('TOTAL');fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'eventos.json'),JSON.stringify(await p.evaluate('EVENTOS()')));
let ts=[];if(modo){const B=await p.evaluate('TEMPO.beats');ts=B.map(x=>x.t0+(x.t1-x.t0)*.72)}else for(let i=0;i<Math.round(total*30);i++)ts.push(i/30);
let i=0,t0=Date.now();for(const t of ts){await p.evaluate(t=>renderAt(t),t);await p.screenshot({path:path.join(out,`f${String(i++).padStart(5,'0')}.jpg`),type:'jpeg',quality:90});if(i%200==0)console.log(i,((Date.now()-t0)/i|0)+'ms/f')}
console.log('frames',i,'total',total);await b.close()})();
