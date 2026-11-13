// Uso: node render_par.js URL saida_dir inicio fim [borrao]   (renderiza os quadros [inicio,fim) a 30 fps)
// borrao: se a página definir window.BORRAO(t) -> true, o quadro vira média de 5 sub-quadros (borrão de movimento).
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
(async()=>{const [url,out,a,z]=process.argv.slice(2);const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});p.on('pageerror',e=>{console.log('ERR',e.message);process.exitCode=1});
await p.goto(url);await p.waitForFunction('window.pronto===true',{timeout:180000});const total=await p.evaluate('TOTAL');fs.mkdirSync(out,{recursive:true});
if(+a===0)fs.writeFileSync(path.join(out,'eventos.json'),JSON.stringify(await p.evaluate('EVENTOS()')));
const fim=Math.min(+z,Math.round(total*30));for(let i=+a;i<fim;i++){const f=path.join(out,`f${String(i).padStart(5,'0')}.jpg`);if(fs.existsSync(f))continue;const bor=process.argv[6]&&await p.evaluate(t=>!!(window.BORRAO&&BORRAO(t)),i/30);
 if(!bor){await p.evaluate(t=>renderAt(t),i/30);await p.screenshot({path:f,type:'jpeg',quality:90})}
 else{const sub=[];for(let k=0;k<5;k++){await p.evaluate(t=>renderAt(t),(i+k/5-.4)/30);sub.push(await p.screenshot({type:'png'}))}
  await p.evaluate(async(imgs)=>{const c=document.createElement('canvas');c.width=1080;c.height=1920;const g=c.getContext('2d');g.globalAlpha=1/5;
   for(let k=0;k<imgs.length;k++){const im=new Image();im.src='data:image/png;base64,'+imgs[k];await im.decode();g.globalAlpha=1/(k+1);g.drawImage(im,0,0)}window.__bor=c.toDataURL('image/jpeg',.9)},sub.map(b=>b.toString('base64')));
  fs.writeFileSync(f,Buffer.from((await p.evaluate('window.__bor')).split(',')[1],'base64'))}}
console.log('ok',a,fim);await b.close()})();
