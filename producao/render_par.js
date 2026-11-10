// Uso: node render_par.js URL saida_dir inicio fim   (renderiza os quadros [inicio,fim) a 30 fps)
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const [url,out,a,z]=process.argv.slice(2);const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});p.on('pageerror',e=>{console.log('ERR',e.message);process.exitCode=1});
await p.goto(url);await p.waitForFunction('window.pronto===true',{timeout:180000});const total=await p.evaluate('TOTAL');fs.mkdirSync(out,{recursive:true});
if(+a===0)fs.writeFileSync(path.join(out,'eventos.json'),JSON.stringify(await p.evaluate('EVENTOS()')));
const fim=Math.min(+z,Math.round(total*30));for(let i=+a;i<fim;i++){const f=path.join(out,`f${String(i).padStart(5,'0')}.jpg`);if(fs.existsSync(f))continue;await p.evaluate(t=>renderAt(t),i/30);await p.screenshot({path:f,type:'jpeg',quality:90})}
console.log('ok',a,fim);await b.close()})();
