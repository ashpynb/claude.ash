// Motor comum dos vídeos da série F2L.
// Cada episódio (epNN.html) carrega epNN_tempo.js (window.TEMPO), este arquivo,
// e depois define as deixas (reset/mov/nota) e a função efeitos(ctx).
// Regras: aprendizados.md (giro na palavra falada, legenda com notação, nada parado).

// ---------- modelo do cubo (mesmo de anim/cubo.html) ----------
const CORES={px:'#e8202a',nx:'#ff8a1c',py:'#ffe31a',ny:'#ffffff',pz:'#19c24a',nz:'#1f5bff'}; // R L U D F B
const S=150, NORM={px:[1,0,0],nx:[-1,0,0],py:[0,1,0],ny:[0,-1,0],pz:[0,0,1],nz:[0,0,-1]};
const LETRA={py:'U',px:'R',nx:'L',pz:'F',ny:'D',nz:'B'};
const I3=()=>[[1,0,0],[0,1,0],[0,0,1]];
const mul=(a,b)=>a.map((r,i)=>b[0].map((_,j)=>r.reduce((s,_,k)=>s+a[i][k]*b[k][j],0)));
const ap=(m,v)=>m.map(r=>r[0]*v[0]+r[1]*v[1]+r[2]*v[2]);
function rot(e,a){const c=Math.cos(a),s=Math.sin(a);if(e==='x')return[[1,0,0],[0,c,-s],[0,s,c]];if(e==='y')return[[c,0,s],[0,1,0],[-s,0,c]];return[[c,-s,0],[s,c,0],[0,0,1]]}
const arred=m=>m.map(r=>r.map(Math.round));
const MOV={R:{e:'x',a:-1,f:p=>p[0]===1},L:{e:'x',a:1,f:p=>p[0]===-1},U:{e:'y',a:-1,f:p=>p[1]===1},D:{e:'y',a:1,f:p=>p[1]===-1},
 F:{e:'z',a:-1,f:p=>p[2]===1},B:{e:'z',a:1,f:p=>p[2]===-1},x:{e:'x',a:-1,f:()=>true},y:{e:'y',a:-1,f:()=>true}};
function parse(seq){return seq.trim().split(/\s+/).filter(Boolean).map(t=>{const m=t.match(/^([RLUDFBxy])(2|')?$/);if(!m)throw new Error('mov inválido '+t);return{txt:t,b:m[1],q:m[2]==='2'?2:(m[2]==="'"?-1:1)}})}
function nomeCasa(p){let n='';if(p[1]===1)n+='U';if(p[1]===-1)n+='D';if(p[2]===1)n+='F';if(p[2]===-1)n+='B';if(p[0]===1)n+='R';if(p[0]===-1)n+='L';return n}
const cuboEl=document.getElementById('cubo');let pecas=[];
for(let x=-1;x<=1;x++)for(let y=-1;y<=1;y++)for(let z=-1;z<=1;z++){if(!x&&!y&&!z)continue;
 const el=document.createElement('div');el.className='peca';const st={};
 const lados={px:x===1,nx:x===-1,py:y===1,ny:y===-1,pz:z===1,nz:z===-1};
 for(const k in lados){const f=document.createElement('div');f.className='f '+k;
  if(lados[k]){const i=document.createElement('i');i.style.background=CORES[k];
   if(Math.abs(x)+Math.abs(y)+Math.abs(z)===1){const b=document.createElement('b');b.textContent=LETRA[k];i.appendChild(b)}
   f.appendChild(i);st[k]=i}
  el.appendChild(f)}
 cuboEl.appendChild(el);pecas.push({el,p0:[x,y,z],nome:nomeCasa([x,y,z]),st})}
function resetar(){for(const q of pecas){q.p=q.p0.slice();q.m=I3()}}
function aplicar(m,frac=1){const d=MOV[m.b],ang=d.a*m.q*Math.PI/2;
 if(frac>=1){const R=arred(rot(d.e,ang));for(const q of pecas)if(d.f(q.p)){q.p=ap(R,q.p);q.m=arred(mul(R,q.m))}return null}
 return{sel:q=>d.f(q.p),R:rot(d.e,ang*frac)}}
function css(m,t){const c=[[m[0][0],-m[0][1],m[0][2]],[-m[1][0],m[1][1],-m[1][2]],[m[2][0],-m[2][1],m[2][2]]];
 return `matrix3d(${c[0][0]},${c[1][0]},${c[2][0]},0,${c[0][1]},${c[1][1]},${c[2][1]},0,${c[0][2]},${c[1][2]},${c[2][2]},0,${t[0]*S},${-t[1]*S},${t[2]*S},1)`}
// off: {nomeDaPeça:[dx,dy,dz]} deslocamento visual extra (peça "voando"), em unidades de peça
function desenhar(anim,off={},esconde=null){for(const q of pecas){const R=anim&&anim.sel(q)?anim.R:I3();const p=ap(R,q.p);const o=off[q.nome];
 q.el.style.visibility=esconde&&esconde(q)?'hidden':'visible';
 q.el.style.transform=css(mul(R,q.m),o?[p[0]+o[0],p[1]+o[1],p[2]+o[2]]:p)}}
const normalAtual=(q,k)=>ap(q.m,NORM[k]);
const faceDe=v=>v[0]===1?'px':v[0]===-1?'nx':v[1]===1?'py':v[1]===-1?'ny':v[2]===1?'pz':'nz';

// ---------- utilidades ----------
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const ease=t=>{t=clamp(t);return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2};
const out=t=>{t=clamp(t);return 1-Math.pow(1-t,3)};
const back=t=>{t=clamp(t);const c=1.9;return 1+(c+1)*Math.pow(t-1,3)+c*Math.pow(t-1,2)};
const lerp=(a,b,t)=>a+(b-a)*t;
const $=id=>document.getElementById(id);
(()=>{let s=3;const r=()=>(s=(s*16807)%2147483647)/2147483647;for(let i=0;i<70;i++){const e=document.createElement('i');e.style.left=r()*1080+'px';e.style.top=r()*1100+'px';e.style.opacity=.2+r()*.6;$('estrelas').appendChild(e)}})();

// ---------- linha do tempo ----------
const B=TEMPO.beats;
const norm=w=>w.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]/g,'');
function palavra(bi,alvo,n=1){let c=0;for(const w of B[bi].words){if(norm(w.w).startsWith(norm(alvo))&&++c===n)return w.t0}
 throw new Error(`palavra "${alvo}" não achada no beat ${bi}: ${B[bi].fala}`)}
const EV=[],NOTA=[];const DUR1=.62,DUR2=.95;
function reset(t,seq=''){EV.push({t,tipo:'reset',seq})}
function mov(t,txt,nota=true,d1=DUR1){for(const m of parse(txt)){const d=m.q===2?DUR2:d1;EV.push({t,tipo:'mov',m,dur:d});if(nota)NOTA.push({t,txt:m.txt});t+=d}return t}
function nota(t,txt){NOTA.push({t,txt})}
function estado(t){let r=0;for(let i=0;i<EV.length;i++)if(EV[i].tipo==='reset'&&EV[i].t<=t)r=i;
 resetar();if(EV[r]&&EV[r].seq)for(const m of parse(EV[r].seq))aplicar(m);
 let anim=null;for(let i=r+1;i<EV.length;i++){const e=EV[i];if(e.tipo!=='mov'||e.t>t)continue;
  const k=(t-e.t)/e.dur;if(k>=1)aplicar(e.m);else anim=aplicar(e.m,ease(k))}
 return anim}

// destaques: luz/dim por face do mundo; foco = só estas peças coloridas (resto cinza); pecaLuz = peças com borda branca
function marcar({luz=[],dim=null,letras=[],cinzaTopo=false,foco=null,pecaLuz=[]}={}){
 for(const q of pecas)for(const k in q.st){const i=q.st[k];const f=faceDe(normalAtual(q,k));
  const L=luz.includes(f)||pecaLuz.includes(q.nome);i.classList.toggle('luz',L);
  i.classList.toggle('dim',(dim&&!L&&dim.includes(f))||(cinzaTopo&&q.p[1]===1)||(foco&&!foco.includes(q.nome)&&!L));
  const b=i.querySelector('b');if(b)b.style.opacity=letras.includes(f)?1:0}}

// ---------- legenda: notação no lugar das letras faladas (pedido da usuária após o ep. 1) ----------
const LET={'érre':'R','éle':'L','u':'U','éfe':'F','dê':'D','xis':'x','ípsilon':'y'};
function gruposLegenda(fala){
 const toks=fala.split(' ');const g=[];
 for(let i=0;i<toks.length;i++){const lim=s=>s.toLowerCase().replace(/[^\p{L}]/gu,'');const pont=s=>(s.match(/[^\p{L}\p{N}]+$/u)||[''])[0];
  const a=lim(toks[i]);
  if(a==='éfe'&&lim(toks[i+1]||'')==='dois'&&lim(toks[i+2]||'')==='éle'){g.push({txt:'F2L'+pont(toks[i+2]),n:3,mv:1});i+=2;continue}
  if(LET[a]!==undefined){let txt=LET[a],n=1,p=pont(toks[i]);const b=lim(toks[i+1]||'');
   if(!p&&b==='linha'){txt+="'";n=2;p=pont(toks[i+1])}else if(!p&&b==='dois'){txt+='2';n=2;p=pont(toks[i+1])}
   g.push({txt:txt+p,n,mv:1});i+=n-1;continue}
  g.push({txt:toks[i],n:1,mv:0})}
 return g}
function legenda(b,t){const g=gruposLegenda(b.fala);const ws=b.words;let wi=0,html=[];
 // casa cada palavra do texto com o tempo do TTS (em ordem)
 const toks=b.fala.split(' ');const tempoTok=[];
 for(const tk of toks){const n=norm(tk);let tw=null;
  for(let j=wi;j<ws.length;j++){const m=norm(ws[j].w);if(m===n||(n&&m.startsWith(n))||(m&&n.startsWith(m))){tw=j;wi=j+1;break}}
  tempoTok.push(tw)}
 let k=0;for(const x of g){let ag=false;for(let j=k;j<k+x.n;j++){const tw=tempoTok[j];if(tw!==null&&t>=ws[tw].t0&&(tw+1>=ws.length?t<ws[tw].t1+.25:t<ws[tw+1].t0))ag=true}
  k+=x.n;html.push(`<span class="${ag?'ag':''} ${x.mv?'mv':''}">${x.txt}</span>`)}
 $('leg').innerHTML=html.join(' ')}

// ---------- quadro ----------
const BASE_X=-26,BASE_Y=-36;
let OCULTA=[]; // ids de overlays que o episódio usa (zerados todo quadro)
function renderAt(t){
 const bi0=B.findIndex(b=>t>=b.t0&&t<b.t1);const bi=bi0===-1?B.length-1:bi0;const b=B[bi];const u=clamp((t-b.t0)/(b.t1-b.t0)),lt=t-b.t0;
 legenda(b,t);
 OCULTA.forEach(i=>$(i).style.opacity=0);
 const v={vx:BASE_X,vy:BASE_Y,vz:0,sc:1,tx:0,ty:0,shx:0,shy:0,flash:0,mk:{},off:{},esconde:null,semNota:false};
 const anim=estado(t);
 efeitos({bi,b,u,lt,t,v,w:(a,n)=>palavra(bi,a,n)});
 v.vy+=Math.sin(t*.9)*3;v.vx+=Math.sin(t*.7)*1.5;
 for(const e of EV){if(e.tipo==='mov'&&t>=e.t&&t-e.t<.35){v.sc*=1+.05*Math.sin(Math.PI*(t-e.t)/.35)}}
 $('chao').style.backgroundPosition=`0 ${t*60}px`;
 marcar(v.mk);desenhar(anim,v.off,v.esconde);
 $('vista').style.transform=`rotateX(${v.vx}deg) rotateY(${v.vy}deg) rotateZ(${v.vz}deg)`;
 $('cam').style.transform=`translate3d(${v.tx+v.shx}px,${v.ty+v.shy}px,0) scale(${v.sc})`;
 let n=null;for(const x of NOTA)if(x.t<=t)n=x;const J=$('jogada');
 if(n&&t-n.t<1.8&&!v.semNota){const k=t-n.t;J.innerHTML=n.txt;J.style.opacity=clamp(k/.06)*clamp((1.8-k)/.25);J.style.transform=`scale(${.5+.5*back(k/.22)})`}else J.style.opacity=0;
 for(const e of EV)if(e.tipo==='reset'&&e.t>0&&t>=e.t&&t-e.t<.08)v.flash=Math.max(v.flash,.35);
 $('flash').style.opacity=v.flash}
function iniciar(){EV.sort((a,b)=>a.t-b.t);NOTA.sort((a,b)=>a.t-b.t);
 window.renderAt=renderAt;window.TOTAL=TEMPO.total;
 window.EVENTOS=()=>({EV:EV.map(e=>({t:e.t,tipo:e.tipo,m:e.m?e.m.txt:e.seq,dur:e.dur})),NOTA});renderAt(0)}
