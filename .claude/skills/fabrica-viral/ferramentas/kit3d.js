// Kit 3D "boneco de primitivas" (ficha 09): personagem de cápsulas/esferas com rosto pintado em textura,
// materiais com textura procedural (canvas), luz suave com sombra macia, cenário de quarto e física (cannon-es)
// pré-calculada pra ficar determinística no render quadro a quadro.
import * as THREE from 'three';
import {RoomEnvironment} from './vendor/jsm/environments/RoomEnvironment.js';
import {RoundedBoxGeometry} from './vendor/jsm/geometries/RoundedBoxGeometry.js';
import * as CANNON from './vendor/cannon-es.js';
export {THREE, CANNON};

export const lin = h => new THREE.Color(h).convertSRGBToLinear();
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)), lerp=(a,b,k)=>a+(b-a)*k;
export const ease=k=>{k=clamp(k);return k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2};
export const back=k=>{k=clamp(k);const c=1.9;return 1+(c+1)*Math.pow(k-1,3)+c*Math.pow(k-1,2)};
export const hash=n=>{const s=Math.sin(n*127.1)*43758.5453;return s-Math.floor(s)};

// ---------- render ----------
export function criarRender(W,H){
 const r=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setPixelRatio(1);r.setSize(W,H);
 r.outputEncoding=THREE.sRGBEncoding;r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=.82;
 r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;document.body.prepend(r.domElement);
 const pm=new THREE.PMREMGenerator(r);const env=pm.fromScene(new RoomEnvironment(),.04).texture;return {r,env}}

// ---------- materiais e texturas ----------
const cacheM=new Map();
export function mat(cor,o={}){const k=cor+JSON.stringify(o);if(!o.map&&cacheM.has(k))return cacheM.get(k);
 const m=new THREE.MeshStandardMaterial({color:lin(cor),roughness:o.rough??.75,metalness:o.metal??0,map:o.map||null,transparent:!!o.transp,opacity:o.op??1,emissive:o.emis?lin(o.emis):new THREE.Color(0),emissiveIntensity:o.ei??1,emissiveMap:o.emisMap||null,side:o.side??THREE.FrontSide,envMapIntensity:o.envI??.35});
 if(!o.map)cacheM.set(k,m);return m}
export function tex(w,h,draw,rep){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;t.anisotropy=4;
 if(rep){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(rep[0],rep[1])}t.userData.canvas=c;return t}
export const T={
 listras:(base,linha,n=8)=>tex(256,256,(g,w,h)=>{g.fillStyle=base;g.fillRect(0,0,w,h);g.fillStyle=linha;for(let i=0;i<n;i++)g.fillRect(i*w/n,0,w/n*.32,h)}),
 madeira:(c1='#9a6a45',c2='#7d5236')=>tex(512,512,(g,w,h)=>{for(let i=0;i<8;i++){g.fillStyle=i%2?c1:c2;g.fillRect(0,i*h/8,w,h/8);g.fillStyle='rgba(0,0,0,.25)';g.fillRect(0,i*h/8,w,3);
  for(let k=0;k<14;k++){g.strokeStyle='rgba(60,30,10,.18)';g.lineWidth=2;g.beginPath();const y=i*h/8+8+hash(i*20+k)*(h/8-16);g.moveTo(0,y);for(let xx=0;xx<w;xx+=32)g.lineTo(xx,y+Math.sin(xx*.03+k)*3);g.stroke()}
  const off=hash(i)*w;g.fillStyle='rgba(0,0,0,.25)';g.fillRect(off,i*h/8,3,h/8)}},[3,3]),
 papel:(base,bola)=>tex(256,256,(g,w,h)=>{g.fillStyle=base;g.fillRect(0,0,w,h);g.fillStyle=bola;for(let i=0;i<4;i++)for(let j=0;j<4;j++){g.beginPath();g.arc(i*64+(j%2)*32+16,j*64+16,7,0,7);g.fill()}},[6,4]),
 colcha:(c1,c2)=>tex(512,512,(g,w,h)=>{const n=6;for(let i=0;i<n;i++)for(let j=0;j<n;j++){g.fillStyle=(i+j)%2?c1:c2;g.fillRect(i*w/n,j*h/n,w/n,h/n);g.strokeStyle='rgba(255,255,255,.55)';g.setLineDash([8,8]);g.lineWidth=3;g.strokeRect(i*w/n+8,j*h/n+8,w/n-16,h/n-16)}
  g.setLineDash([]);g.fillStyle='rgba(255,255,255,.7)';for(let i=0;i<n;i++)for(let j=0;j<n;j++)if((i+j)%2){g.beginPath();g.arc((i+.5)*w/n,(j+.5)*h/n,10,0,7);g.fill()}}),
 tapete:()=>tex(512,512,(g,w,h)=>{const cs=['#d9606a','#ffd0a0','#7b5cff','#ffd0a0','#d9606a'];cs.forEach((c,i)=>{g.fillStyle=c;g.beginPath();g.arc(w/2,h/2,w/2-i*44,0,7);g.fill()})}),
 piso:(c1,c2)=>tex(256,256,(g,w,h)=>{for(let i=0;i<2;i++)for(let j=0;j<2;j++){g.fillStyle=(i+j)%2?c1:c2;g.fillRect(i*128,j*128,128,128)}g.strokeStyle='rgba(0,0,0,.15)';g.lineWidth=4;g.strokeRect(0,0,w,h)},[8,8]),
 grad:(c1,c2)=>tex(16,512,(g,w,h)=>{const gr=g.createLinearGradient(0,0,0,h);gr.addColorStop(0,c1);gr.addColorStop(1,c2);g.fillStyle=gr;g.fillRect(0,0,w,h)})
};

// ---------- geometrias ----------
export const G={
 cap:(r,l,s=10)=>new THREE.CapsuleGeometry(r,l,6,s*2),
 esf:(r,s=32)=>new THREE.SphereGeometry(r,s,s*.75|0),
 cx:(w,h,d,r=.05)=>new RoundedBoxGeometry(w,h,d,4,Math.min(r,w/2-.001,h/2-.001,d/2-.001)),
 cil:(rt,rb,h,s=32)=>new THREE.CylinderGeometry(rt,rb,h,s)
};
export function malha(g,m,{sombra=true,recebe=true}={}){const o=new THREE.Mesh(g,m);o.castShadow=sombra;o.receiveShadow=recebe;return o}

// ---------- rosto pintado (textura em casca esférica na frente da cabeça) ----------
const cacheRosto=new Map();
function desenhaRosto(g,w,h,f){g.clearRect(0,0,w,h);const cx=w/2,ey=h*.47,TI='#1b1626';const sur=f.cara==='surpreso'||f.cara==='assustado';
 const pis=f.pisca;const olho=(d)=>{const ex=cx+d*w*.105;
  if(f.cara==='feliz2'){g.strokeStyle=TI;g.lineWidth=w*.022;g.lineCap='round';g.beginPath();g.arc(ex,ey+h*.02,w*.04,Math.PI*1.1,Math.PI*1.9);g.stroke();return}
  if(f.cara==='tonto'){g.strokeStyle=TI;g.lineWidth=w*.014;g.beginPath();for(let a=0;a<12.5;a+=.25){const r=a*w*.0034;g.lineTo(ex+Math.cos(a+f.t*9)*r,ey+Math.sin(a+f.t*9)*r)}g.stroke();return}
  const rx=w*(sur?.05:.042),ry=h*(sur?.062:.052)*pis;g.fillStyle='#fff';g.beginPath();g.ellipse(ex,ey,rx,Math.max(ry,1),0,0,7);g.fill();g.strokeStyle=TI;g.lineWidth=w*.01;g.stroke();
  if(pis>.3){g.save();g.beginPath();g.ellipse(ex,ey,rx,ry,0,0,7);g.clip();g.fillStyle=TI;g.beginPath();g.arc(ex+f.ox*w*.012,ey+f.oy*h*.012,w*(sur?.018:.026),0,7);g.fill();
   g.fillStyle='#fff';g.beginPath();g.arc(ex+f.ox*w*.012+w*.011,ey+f.oy*h*.012-h*.012,w*.009,0,7);g.fill();g.restore()}
  if(f.cara==='relax'||f.cara==='cansado'){g.fillStyle=f.pele;g.fillRect(ex-rx-2,ey-ry-2,rx*2+4,ry*.9);g.strokeStyle=TI;g.lineWidth=w*.012;g.beginPath();g.moveTo(ex-rx,ey-ry*.1);g.lineTo(ex+rx,ey-ry*.1);g.stroke()}};
 olho(-1);olho(1);
 // sobrancelhas
 g.strokeStyle=f.sobr;g.lineWidth=w*.02;g.lineCap='round';[-1,1].forEach(d=>{let y1=h*.36,y2=h*.37;if(sur){y1=y2=h*.32}
  if(f.cara==='confiante'){y1=d<0?h*.37:h*.33;y2=d<0?h*.36:h*.35}if(f.cara==='triste'||f.cara==='preocupado'){y1=h*.33;y2=h*.38}
  g.beginPath();g.moveTo(cx+d*w*.045,y1);g.lineTo(cx+d*w*.15,y2);g.stroke()});
 // bochechas
 g.fillStyle='rgba(255,110,120,.35)';[-1,1].forEach(d=>{g.beginPath();g.ellipse(cx+d*w*.14,h*.6,w*.035,h*.022,0,0,7);g.fill()});
 // boca
 const my=h*.68;g.strokeStyle=TI;g.lineWidth=w*.016;g.fillStyle='#6a1f2a';g.lineCap='round';
 const c=f.cara;if(sur){g.beginPath();g.ellipse(cx,my,w*.03,h*.04,0,0,7);g.fill();g.stroke()}
 else if(c==='tonto'){g.beginPath();g.moveTo(cx-w*.05,my);for(let k=1;k<=6;k++)g.lineTo(cx-w*.05+k*w*.0167,my+(k%2?-h*.014:h*.014));g.stroke()}
 else if(c==='triste'||c==='preocupado'){g.beginPath();g.moveTo(cx-w*.05,my+h*.02);g.quadraticCurveTo(cx,my-h*.03,cx+w*.05,my+h*.02);g.stroke()}
 else if(c==='relax'||c==='cansado'){g.beginPath();g.moveTo(cx-w*.04,my);g.quadraticCurveTo(cx,my+h*.02,cx+w*.04,my);g.stroke()}
 else if(c==='confiante'){g.beginPath();g.moveTo(cx-w*.05,my-h*.005);g.quadraticCurveTo(cx+w*.01,my+h*.04,cx+w*.06,my-h*.02);g.stroke()}
 else{g.beginPath();g.moveTo(cx-w*.06,my-h*.01);g.quadraticCurveTo(cx,my+h*.08,cx+w*.06,my-h*.01);g.closePath();g.fill();g.stroke();g.fillStyle='#fff';g.fillRect(cx-w*.04,my-h*.005,w*.08,h*.014)}
 if(f.bigode){g.fillStyle=f.bigode;g.beginPath();g.ellipse(cx-w*.03,my-h*.035,w*.04,h*.016,.2,0,7);g.ellipse(cx+w*.03,my-h*.035,w*.04,h*.016,-.2,0,7);g.fill()}
 if(f.rugas){g.strokeStyle='rgba(80,40,20,.35)';g.lineWidth=w*.008;g.beginPath();g.moveTo(cx-w*.06,h*.27);g.lineTo(cx+w*.06,h*.27);g.moveTo(cx-w*.05,h*.3);g.lineTo(cx+w*.05,h*.3);g.stroke()}}
function texRosto(f){const k=JSON.stringify({...f,t:f.cara==='tonto'?Math.round(f.t*8):0});if(cacheRosto.has(k))return cacheRosto.get(k);
 const t=tex(512,512,(g,w,h)=>desenhaRosto(g,w,h,f));if(cacheRosto.size>400)cacheRosto.clear();cacheRosto.set(k,t);return t}

// ---------- BONECO ----------
// Pose: corpo de pé na origem (pés em y=0). Unidade ~ 1 = altura do tronco.
export function boneco(P){
 const g=new THREE.Group();const pele=mat(P.pele,{rough:.55});
 const listra=P.roupa==='pijama';const corR=P.roupa==='traje'?'#f2f2f4':P.cor;
 const mRoupa=listra?mat('#ffffff',{map:T.listras(corR,'#cfe0ff',6),rough:.8}):mat(corR,{rough:.8});
 const mCalca=listra?mRoupa:mat(P.calca||'#2c3250',{rough:.8});
 const gordo={magro:.85,normal:1,fofo:1.25}[P.corpo||'normal'];
 const quadril=new THREE.Group();quadril.position.y=.95;g.add(quadril);
 const tronco=malha(G.cap(.34*gordo,.42),mRoupa);tronco.position.y=.45;tronco.scale.set(1,1,.78);quadril.add(tronco);
 if(listra){[.62,.45,.28].forEach(y=>{const bt=malha(G.esf(.03,10),mat('#ffffff',{rough:.3}),{sombra:false});bt.position.set(0,y,.27*gordo);quadril.add(bt)})}
 const pescoco=new THREE.Group();pescoco.position.y=.92;quadril.add(pescoco);
 const cab=new THREE.Group();cab.position.y=.36;pescoco.add(cab);
 const cabeca=malha(G.esf(.36,40),pele);cabeca.scale.set(1,1.02,.96);cab.add(cabeca);
 [-1,1].forEach(d=>{const o=malha(G.esf(.075,16),pele);o.position.set(d*.35,-.02,0);o.scale.set(.6,1,1);cab.add(o)});
 const nariz=malha(G.esf(.05,16),mat(P.pele,{rough:.5}));nariz.position.set(0,-.04,.35);cab.add(nariz);
 // rosto pintado
 const fMat=new THREE.MeshBasicMaterial({transparent:true,depthWrite:false,toneMapped:false});
 const rosto=new THREE.Mesh(new THREE.SphereGeometry(.3615,48,36,Math.PI*.15,Math.PI*.7,Math.PI*.18,Math.PI*.62),fMat);rosto.scale.copy(cabeca.scale);rosto.renderOrder=2;cab.add(rosto);
 // cabelo
 const mCab=mat(P.cabCor,{rough:.9});
 if(P.cab==='curto'||P.cab==='cacheado'){const c=malha(new THREE.SphereGeometry(.375,40,30,0,Math.PI*2,0,Math.PI*.42),mCab);c.rotation.x=-.32;c.position.set(0,.02,-.02);c.scale.set(1.02,1.05,1);cab.add(c);
  if(P.cab==='cacheado')for(let i=0;i<22;i++){const a=hash(i)*Math.PI*2,e=.15+hash(i+7)*.5;const b=malha(G.esf(.09,12),mCab);b.position.set(Math.cos(a)*Math.cos(e)*.36,.1+Math.sin(e)*.3,Math.sin(a)*Math.cos(e)*.36-.04);cab.add(b)}
  const fr=malha(G.cap(.06,.32),mCab);fr.rotation.z=Math.PI/2;fr.position.set(.02,.27,.25);fr.rotation.y=.1;cab.add(fr)}
 if(P.cab==='topete'){const c=malha(new THREE.SphereGeometry(.375,40,30,0,Math.PI*2,0,Math.PI*.38),mCab);c.rotation.x=-.3;c.position.set(0,.02,-.03);cab.add(c);
  const tp=malha(G.cap(.11,.2,8),mCab);tp.rotation.set(1.3,0,0);tp.position.set(0,P.bone?.27:.36,P.bone?.3:.18);tp.scale.set(1.7,1,1);cab.add(tp);const tp2=malha(G.esf(.13,14),mCab);tp2.position.set(.04,P.bone?.3:.43,P.bone?.32:.25);tp2.scale.set(1.6,.75,1.1);cab.add(tp2)}
 // boné virado pra trás (aba na nuca), deixa o topete aparecer na testa
 if(P.bone){const mB=mat(P.bone,{rough:.7});const capG=new THREE.Group();cab.add(capG);const cp=malha(new THREE.SphereGeometry(.39,36,24,0,Math.PI*2,0,Math.PI*.4),mB);capG.add(cp);
  const aba=malha(G.cil(.25,.25,.035,24),mB);aba.scale.set(1,1,1.2);aba.position.set(0,.22,-.36);aba.rotation.x=-.25;capG.add(aba);const bt=malha(G.esf(.035,8),mB);bt.position.set(0,.39,0);capG.add(bt);
  const fecho=malha(G.cx(.14,.06,.03,.01),mat('#f4f4f4'));fecho.position.set(0,.18,-.37);capG.add(fecho);capG.rotation.x=-.55;capG.position.set(0,.03,-.05)}
 if(P.cab==='lados'){[-1,1].forEach(d=>{const s=malha(G.esf(.13,16),mCab);s.position.set(d*.32,.05,-.08);s.scale.set(.6,1,1.2);cab.add(s)});const s2=malha(G.esf(.15,16),mCab);s2.position.set(0,.05,-.3);s2.scale.set(1.6,.9,.6);cab.add(s2)}
 // óculos 3D
 const oc=new THREE.Group();const mOc=mat('#1b1626',{rough:.3});[-1,1].forEach(d=>{const ar=malha(new THREE.TorusGeometry(.085,.014,10,32),mOc,{sombra:false});ar.position.set(d*.12,.05,.345);ar.scale.y=.85;oc.add(ar);
  const le=malha(new THREE.CircleGeometry(.085,24),new THREE.MeshStandardMaterial({color:0x223344,transparent:true,opacity:.0,roughness:.1}),{sombra:false});le.position.copy(ar.position);le.position.z+=.002;le.scale.y=.85;oc.add(le);oc.userData['lente'+d]=le;
  const ha=malha(G.cap(.012,.28,4),mOc,{sombra:false});ha.rotation.x=Math.PI/2;ha.position.set(d*.205,.06,.2);oc.add(ha)});
 const ponte=malha(G.cap(.012,.05,4),mOc,{sombra:false});ponte.rotation.z=Math.PI/2;ponte.position.set(0,.07,.36);oc.add(ponte);oc.visible=!!P.oculos;cab.add(oc);
 // capacete de astronauta
 const cap=malha(G.esf(.56,40),new THREE.MeshPhysicalMaterial({color:0xcfe8ff,transparent:true,opacity:.22,roughness:.05,metalness:0,envMapIntensity:1.5}),{sombra:false});cap.visible=false;cab.add(cap);
 const gola=malha(new THREE.TorusGeometry(.36,.07,12,32),mat('#cfd3db',{rough:.4}));gola.rotation.x=Math.PI/2;gola.position.y=-.38;gola.visible=false;cab.add(gola);
 // braços
 const bracos=[-1,1].map(d=>{const omb=new THREE.Group();omb.position.set(d*.36*gordo,.72,0);quadril.add(omb);
  const b=malha(G.cap(.1,.42),mRoupa);b.position.y=-.27;omb.add(b);const m=malha(G.esf(.12,20),P.roupa==='traje'?mat('#bfc3cc'):pele);m.position.y=-.55;omb.add(m);
  const pol=malha(G.cap(.04,.08),pele);pol.position.set(0,-.55,.1);pol.visible=false;omb.add(pol);return {omb,mao:m,pol}});
 // pernas
 const pernas=[-1,1].map(d=>{const q=new THREE.Group();q.position.set(d*.15,.05,0);quadril.add(q);
  const p=malha(G.cap(.12,.62),mCalca);p.position.y=-.45;q.add(p);const pe=malha(G.esf(.15,20),mat(P.roupa==='traje'?'#bfc3cc':'#f4f4f4',{rough:.6}));pe.scale.set(.85,.6,1.3);pe.position.set(0,-.88,.06);q.add(pe);return {q,p,pe}});
 Object.assign(g.userData,{quadril,cab,pescoco,bracos,pernas,rosto,fMat,oc,cap,gola,tronco,P});
 g.traverse(o=>{if(o.isMesh&&o!==rosto){o.castShadow=o.castShadow;}});
 return g}
// aplica pose/expressão
export function pose(b,o={},t=0){const u=b.userData,P=u.P;
 const resp=Math.sin(t*2.4)*.012;u.tronco.scale.set(1+resp,1+resp*.5,.78+resp);
 u.bracos.forEach((br,i)=>{const d=i?1:-1;const a=(i?o.bD:o.bE)??.12;br.omb.rotation.z=d*a;br.omb.rotation.x=(i?o.bDx:o.bEx)??0;br.pol.visible=!!(i&&o.joinha)});
 u.pernas.forEach((p,i)=>{const s=o.perna??1;p.p.scale.set(s,1,s);p.q.rotation.x=o.sentado?-1.45:(i?o.pDx:o.pEx)??0;if(o.tremor)p.q.rotation.z=Math.sin(t*50+i)*.03});
 u.cab.rotation.set(o.cabX??0,o.cabY??0,o.cabZ??0);u.quadril.rotation.x=o.inclina??0;
 u.oc.visible=o.oculos!==undefined?!!o.oculos:!!P.oculos;const esc=o.escuros?1:0;['lente-1','lente1'].forEach(k=>{u.oc.userData[k].material.opacity=esc*.95});
 u.cap.visible=u.gola.visible=!!o.capacete;
 let pis=o.pisca??((hash(Math.floor(t*1.6)+7)>.82&&(t*1.6%1)<.16)?.1:1);
 const f={cara:o.cara||'feliz',pisca:Math.round(pis*4)/4,ox:o.olhar?.[0]??0,oy:o.olhar?.[1]??0,sobr:P.cab==='lados'||P.cab==='careca'?P.cabCor:P.cabCor,pele:P.pele,bigode:o.bigode||null,rugas:!!o.rugas,t};
 u.fMat.map=texRosto(f);u.fMat.needsUpdate=true}

// ---------- física pré-calculada ----------
// objetos: [{forma:'caixa'|'esfera', tam:[...], pos:[x,y,z], vel:[...], ang:[...]}], chao em y=chaoY, extras: caixas estáticas
export function simular(objs,{chaoY=0,estaticos=[],dur=4,dt=1/120}={}){
 const w=new CANNON.World({gravity:new CANNON.Vec3(0,-9.8,0)});w.defaultContactMaterial.restitution=.35;w.defaultContactMaterial.friction=.4;
 const chao=new CANNON.Body({mass:0,shape:new CANNON.Plane()});chao.quaternion.setFromEuler(-Math.PI/2,0,0);chao.position.y=chaoY;w.addBody(chao);
 estaticos.forEach(e=>{const b=new CANNON.Body({mass:0,shape:new CANNON.Box(new CANNON.Vec3(e.tam[0]/2,e.tam[1]/2,e.tam[2]/2))});b.position.set(...e.pos);w.addBody(b)});
 const bs=objs.map(o=>{const sh=o.forma==='esfera'?new CANNON.Sphere(o.tam[0]):new CANNON.Box(new CANNON.Vec3(o.tam[0]/2,o.tam[1]/2,o.tam[2]/2));
  const b=new CANNON.Body({mass:o.massa??.2,shape:sh});b.position.set(...o.pos);if(o.vel)b.velocity.set(...o.vel);if(o.ang)b.angularVelocity.set(...o.ang);if(o.rot)b.quaternion.setFromEuler(...o.rot);b.linearDamping=.05;b.angularDamping=.1;w.addBody(b);return b});
 const fr=[];const n=Math.ceil(dur*30);for(let i=0;i<=n;i++){fr.push(bs.map(b=>[b.position.x,b.position.y,b.position.z,b.quaternion.x,b.quaternion.y,b.quaternion.z,b.quaternion.w]));for(let k=0;k<4;k++)w.step(dt)}
 return (meshes,tt)=>{const i=clamp(Math.floor(tt*30),0,n),k=clamp(tt*30-i,0,1),a=fr[i],b=fr[Math.min(n,i+1)];meshes.forEach((m,j)=>{m.position.set(lerp(a[j][0],b[j][0],k),lerp(a[j][1],b[j][1],k),lerp(a[j][2],b[j][2],k));m.quaternion.set(a[j][3],a[j][4],a[j][5],a[j][6])})}}

// ---------- poeirinha de fundo (inserts) ----------
export function poeira(n=60,cor='#ffe6b0'){const g=new THREE.BufferGeometry();const p=new Float32Array(n*3);for(let i=0;i<n;i++){p[i*3]=(hash(i)-.5)*8;p[i*3+1]=hash(i+3)*8;p[i*3+2]=(hash(i+5)-.5)*4-1}
 g.setAttribute('position',new THREE.BufferAttribute(p,3));const pts=new THREE.Points(g,new THREE.PointsMaterial({color:lin(cor),size:.05,transparent:true,opacity:.8}));pts.userData.base=p.slice();return pts}
export function animaPoeira(pts,t){const a=pts.geometry.attributes.position,b=pts.userData.base;for(let i=0;i<a.count;i++){a.array[i*3+1]=((b[i*3+1]+t*.15+Math.sin(t+i)*.05)%8);a.array[i*3]=b[i*3]+Math.sin(t*.5+i)*.08}a.needsUpdate=true}

// ---------- ficha 10: corte transversal, etiquetas, câmera em trilha ----------
// corte(renderer, grupo, plano): recorta todos os materiais do grupo no plano (mostra o lado de dentro).
// Ex.: corte(r, terreno, new THREE.Plane(new THREE.Vector3(0,0,-1), 0)) corta tudo com z > 0.
export function corte(r,grupo,plano){r.localClippingEnabled=true;grupo.traverse(o=>{if(!o.isMesh)return;const ms=Array.isArray(o.material)?o.material:[o.material];
 o.material=ms.map(m=>{const c=m.clone();c.clippingPlanes=[plano];c.clipShadows=true;c.side=THREE.DoubleSide;return c});if(o.material.length===1)o.material=o.material[0]})}
// face de corte: textura de terra/parede no plano de corte (põe no lugar do que foi cortado)
// furos: [[x0,y0,x1,y1],...] em coordenadas da face (centro em 0,0) pra deixar ver o que está cortado por dentro
export function faceCorte(w,h,tipo='terra',furos=[]){const t=tex(512,512,(g,W,H)=>{if(tipo==='terra'){g.fillStyle='#7a3a22';g.fillRect(0,0,W,H);for(let i=0;i<900;i++){g.fillStyle=`rgba(${hash(i)>.5?'40,15,5':'150,80,50'},${.25+hash(i+1)*.3})`;g.beginPath();g.arc(hash(i+2)*W,hash(i+3)*H,1+hash(i+4)*4,0,7);g.fill()}}
  else{g.fillStyle='#d9d4c8';g.fillRect(0,0,W,H);g.strokeStyle='rgba(0,0,0,.12)';for(let y=0;y<H;y+=32){g.beginPath();g.moveTo(0,y);g.lineTo(W,y);g.stroke()}}});t.wrapS=t.wrapT=THREE.RepeatWrapping;t.repeat.set(.25,.25);
 const sh=new THREE.Shape();sh.moveTo(-w/2,-h/2);sh.lineTo(w/2,-h/2);sh.lineTo(w/2,h/2);sh.lineTo(-w/2,h/2);sh.closePath();
 furos.forEach(([x0,y0,x1,y1])=>{const f=new THREE.Path();f.moveTo(x0,y0);f.lineTo(x0,y1);f.lineTo(x1,y1);f.lineTo(x1,y0);f.closePath();sh.holes.push(f)});
 return new THREE.Mesh(new THREE.ShapeGeometry(sh),new THREE.MeshStandardMaterial({map:t,roughness:.95}))}
// etiquetas: pílula branca com ponto colorido que segue um ponto 3D (HTML por cima do canvas)
const ETQ=[];
export function etiqueta(texto,alvo,{cor='#e8503c',dy=0}={}){const e=document.createElement('div');e.className='etq';e.innerHTML=`<i style="background:${cor}"></i>${texto}`;
 Object.assign(e.style,{position:'absolute',left:0,top:0,display:'flex',alignItems:'center',gap:'12px',background:'#fff',color:'#1b1626',font:"34px 'Lilita','Inter',sans-serif",padding:'10px 22px 12px',borderRadius:'40px',boxShadow:'0 8px 0 rgba(0,0,0,.25)',opacity:0,whiteSpace:'nowrap',pointerEvents:'none'});
 e.firstChild&&Object.assign(e.firstChild.style,{display:'inline-block',width:'18px',height:'18px',borderRadius:'50%'});document.body.appendChild(e);const o={e,alvo,dy,t0:null};ETQ.push(o);return o}
// chamar depois de posicionar a câmera, a cada quadro: mostra as etiquetas cujo t0 <= t
export function atualizaEtiquetas(cam,t,W,H){const v=new THREE.Vector3();for(const o of ETQ){if(o.t0===null||t<o.t0||(o.t1&&t>o.t1)){o.e.style.opacity=0;continue}
 (o.alvo.isObject3D?o.alvo.getWorldPosition(v):v.copy(o.alvo));v.y+=o.dy;v.project(cam);if(v.z>1){o.e.style.opacity=0;continue}const k=clamp((t-o.t0)/.25);
 o.e.style.opacity=clamp((t-o.t0)/.1);o.e.style.transform=`translate(${(v.x*.5+.5)*W}px,${(-v.y*.5+.5)*H}px) translate(-50%,-100%) scale(${.5+.5*back(k)})`}}
// câmera em trilha: pontos [[x,y,z],...] e alvos; u de 0 a 1 percorre a curva (voo contínuo)
export function trilha(pontos,alvos){const c=new THREE.CatmullRomCurve3(pontos.map(p=>new THREE.Vector3(...p)),false,'centripetal');const a=new THREE.CatmullRomCurve3(alvos.map(p=>new THREE.Vector3(...p)),false,'centripetal');
 return (cam,u)=>{u=clamp(u);cam.position.copy(c.getPointAt(u));cam.lookAt(a.getPointAt(u))}}
// muitas cópias baratas (carros, árvores): InstancedMesh com lista de [x,y,z,rotY,escala]
export function copias(geo,m,lista){const im=new THREE.InstancedMesh(geo,m,lista.length);im.castShadow=im.receiveShadow=true;const M=new THREE.Matrix4(),Q=new THREE.Quaternion(),E=new THREE.Euler();
 lista.forEach((p,i)=>{E.set(0,p[3]||0,0);Q.setFromEuler(E);M.compose(new THREE.Vector3(p[0],p[1],p[2]),Q,new THREE.Vector3().setScalar(p[4]||1));im.setMatrixAt(i,M)});return im}
