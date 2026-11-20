import json
import sys

X = json.load(open(sys.argv[1]))
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pillar_math import MATH
X['math'] = MATH
files = sys.argv[2:]

SECTION = r'''<h2 class="tnr" id="excl">Pillars of argumentation</h2>
<div id="excltext" class="tnr" style="font-size:16px;line-height:1.6;max-width:1100px">
<p>We call a <i>pillar</i> one of the six results in the upper layers of the tree on which the remainder of the proof primarily relies. These include the analytic reduction (rh_of_every, critLine), the Galois representations of Row0b, the theta lifts of TLiftK, the local Langlands correspondence (recTExists), the Selmer bound VWin, and the bridge from VWin to nonvanishing. A declaration is <i>reached</i> by $p$ if it can be arrived at from $p$ by following references, that is, if it appears in the statement or proof of $p$, or in the statement or proof of a declaration that does so, and so on down to the foundations. For a pillar $p$ let $D(p)$ be the set of declarations reached by $p$, and let
$$E(p) \;=\; D(p) \setminus \bigcup_{q \neq p} D(q)$$
be its exclusive support. That is, $E(p)$ is the component of the formalization that serves $p$ and is exclusive to $p$. The six pillars that we identified together reach 128,464 of the 128,479 declarations under riemannHypothesis.</p>
<p>Three findings emerge from this pillar-based characterization. First, the pillars of local Langlands and of the theta lifts are not independent blocks: $D(\texttt{recTExists})$ lies entirely inside the support of the Galois representations, as do 289 of the 291 declarations under TLiftK, so both enter the proof as ingredients of the construction of Galois representations, which alone holds 78,765 exclusive declarations, or 61% of the proof. Second, the Selmer bound VWin reaches 28,257 declarations, of which 14,315 are shared with the Galois block and 13,934 are its own, concentrated in archimedean base change, block decompositions and inertia eigenvalues. Third, the bridge from VWin to nonvanishing is almost disjoint from the rest of the proof: 18,825 of its 19,182 declarations (98%) are exclusive, and they lie in arithmetic geometry, namely embedded resolution of singularities, the arithmetic Hilbert–Samuel theorem and ampleness of heights. If the proof contains a genuinely new argument, these two blocks, the Selmer bound and the height-theoretic bridge, are where this new argument might lie.</p>
</div>
<div id="legend4"></div>
<svg id="exclbars" role="img" aria-label="Support of each pillar, split into exclusive and shared parts"></svg>
<div id="exclpanel" style="background:var(--surface-2);border-radius:8px;padding:14px 16px;margin-top:8px">Select a circle or a name above, or a row of the table below, to list the modules and declarations in that pillar's exclusive support.</div>
<h3 class="tnr" style="font-size:17px;margin:18px 0 6px">Containment between pillars</h3>
<p class="sub tnr" style="font-size:15px">Row $a$, column $b$: the share of $D(a)$ that also lies in $D(b)$.</p>
<div id="exclmatrix"></div>
<script>
(function(){
const X=__EXCL__;
const NS='http://www.w3.org/2000/svg',mk=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const f=n=>n.toLocaleString('en-US'),es=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const T=()=>document.getElementById('tip');
document.getElementById('legend4').innerHTML='';
const P=X.pillars,W=1560,H=780,svg=document.getElementById('exclbars');svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width','100%');
const by=n=>P.findIndex(p=>p.name===n),iG=by('Galois representations'),iS=by('Selmer bound'),iL=by('Local Langlands'),iT=by('Theta lifts'),iB=by('Nonvanishing bridge'),iA=by('Analytic reduction');
const k=255/Math.sqrt(P[iG].support),R=i=>Math.max(5,k*Math.sqrt(P[i].support)),A=n=>Math.PI*k*k*n;
const lens=(r1,r2,d)=>{if(d>=r1+r2)return 0;if(d<=Math.abs(r1-r2))return Math.PI*Math.min(r1,r2)**2;
  const a1=r1*r1*Math.acos((d*d+r1*r1-r2*r2)/(2*d*r1)),a2=r2*r2*Math.acos((d*d+r2*r2-r1*r1)/(2*d*r2));return a1+a2-.5*Math.sqrt((-d+r1+r2)*(d+r1-r2)*(d-r1+r2)*(d+r1+r2))};
const solve=(r1,r2,t)=>{let lo=Math.abs(r1-r2),hi=r1+r2;for(let n=0;n<60;n++){const m=(lo+hi)/2;lens(r1,r2,m)>t?lo=m:hi=m}return (lo+hi)/2};
const C={};C[iG]=[780,410];
const dGS=solve(R(iG),R(iS),A(X.overlap[iG][iS]));C[iS]=[C[iG][0]+dGS*Math.cos(-.35),C[iG][1]+dGS*Math.sin(-.35)];
const dLS=solve(R(iL),R(iS),A(X.overlap[iL][iS])),ux=(C[iG][0]-C[iS][0])/dGS,uy=(C[iG][1]-C[iS][1])/dGS;C[iL]=[C[iS][0]+ux*dLS,C[iS][1]+uy*dLS+18];
C[iT]=[C[iS][0]+ux*(R(iS)*.62),C[iS][1]+uy*(R(iS)*.62)-48];
const dGB=solve(R(iG),R(iB),A(Math.max(1,X.overlap[iB][iG])));C[iB]=[C[iG][0]+dGB*Math.cos(Math.PI*.9),C[iG][1]+dGB*Math.sin(Math.PI*.9)+40];
C[iA]=[C[iG][0]-R(iG)*.55,C[iG][1]-R(iG)-60];
const defs=mk('defs',{},svg);
P.forEach((p,i)=>{const g=mk('radialGradient',{id:'eg'+i,cx:'38%',cy:'34%',r:'75%'},defs);mk('stop',{offset:'0%','stop-color':p.color,'stop-opacity':.42},g);mk('stop',{offset:'100%','stop-color':p.color,'stop-opacity':.16},g)});
const order=[iG,iB,iS,iL,iT,iA],gc=mk('g',{},svg),gl=mk('g',{},svg);
order.forEach(i=>{const p=P[i],[x,y]=C[i],r=R(i),g=mk('g',{style:'cursor:pointer'},gc);
  mk('circle',{cx:x,cy:y,r,fill:`url(#eg${i})`,stroke:p.color,'stroke-width':i===iA||i===iT?1.5:2,'stroke-opacity':.9},g);
  g.addEventListener('mousemove',e=>{const tip=T();if(!tip)return;tip.style.display='block';tip.innerHTML=`<div class="nm">${es(p.name)}</div><div class="md">${es(p.roots.join(', '))}</div><div class="note">${es(p.desc)}</div><div>reaches ${f(p.support)} · exclusive ${f(p.excl.n)} · ${f(p.excl.lines)} exclusive lines</div>`;tip.style.left=Math.min(e.clientX+16,innerWidth-520)+'px';tip.style.top=(e.clientY+16)+'px'});
  g.addEventListener('mouseleave',()=>{const tip=T();if(tip)tip.style.display='none'});g.addEventListener('click',()=>show(i))});
const lab=(i,tx,ty,anchor)=>{const p=P[i],[x,y]=C[i],r=R(i),dx=tx-x,dy=ty-y,dd=Math.hypot(dx,dy)||1,ex=x+dx/dd*r,ey=y+dy/dd*r;
  mk('path',{d:`M${ex},${ey} L${tx},${ty}`,stroke:p.color,'stroke-width':1,'stroke-opacity':.8,fill:'none'},gl);mk('circle',{cx:ex,cy:ey,r:2.2,fill:p.color},gl);
  const t1=mk('text',{x:tx+(anchor==='start'?6:-6),y:ty-2,'text-anchor':anchor,'font-size':18,'font-weight':700,fill:p.color,style:"font-family:'Times New Roman',Times,serif;cursor:pointer"},gl);t1.textContent=p.name;t1.addEventListener('click',()=>show(i));
  const t2=mk('text',{x:tx+(anchor==='start'?6:-6),y:ty+17,'text-anchor':anchor,'font-size':14.5,fill:'var(--text-secondary)',style:"font-family:'Times New Roman',Times,serif"},gl);t2.textContent=`${f(p.support)} reached · ${f(p.excl.n)} exclusive (${(100*p.share).toFixed(1)}%)`};
lab(iG,C[iG][0]-80,C[iG][1]+R(iG)+38,'end');lab(iS,C[iS][0]+R(iS)+70,C[iS][1]-R(iS)-14,'start');lab(iL,C[iS][0]+R(iS)+70,C[iS][1]+R(iS)+30,'start');
lab(iT,C[iS][0]+R(iS)+70,C[iS][1]-R(iS)+62,'start');lab(iB,C[iB][0]-R(iB)-40,C[iB][1]-R(iB)-30,'end');lab(iA,C[iA][0]-70,C[iA][1]+4,'end');
const cap=mk('text',{x:W/2,y:H-10,'text-anchor':'middle','font-size':14,fill:'var(--text-muted)',style:"font-family:'Times New Roman',Times,serif;font-style:italic"},svg);cap.textContent='Circle areas are proportional to the number of declarations reached by each pillar.';
let h='<table style="width:auto;border-collapse:collapse"><tr><th></th>'+P.map(p=>`<th style="font-size:13px;padding:6px 8px;font-family:'Times New Roman',Times,serif">${es(p.name)}</th>`).join('')+'</tr>';
P.forEach((a,i)=>{h+=`<tr data-i="${i}" style="cursor:pointer"><th style="text-align:right;font-size:13px;padding:6px 8px;font-family:'Times New Roman',Times,serif;text-decoration:underline dotted">${es(a.name)}</th>`;
  P.forEach((b,j)=>{const v=a.support?X.overlap[i][j]/a.support:0,al=(.08+.8*v).toFixed(2);
    h+=`<td title="${f(X.overlap[i][j])} of ${f(a.support)}" style="text-align:center;font-size:13px;padding:7px 10px;border:2px solid var(--surface-1);background:rgba(42,120,214,${al});color:${v>.55?'#fff':'var(--text-primary)'};font-variant-numeric:tabular-nums">${i===j?'·':(100*v).toFixed(v>0&&v<.01?1:0)+'%'}</td>`});h+='</tr>'});
const MX=document.getElementById('exclmatrix');MX.innerHTML=h+'</table>';MX.querySelectorAll('tr[data-i]').forEach(r=>r.addEventListener('click',()=>show(+r.dataset.i)));
function show(i){const p=P[i],e=p.excl,PN=document.getElementById('exclpanel');
  PN.innerHTML=`<div class="nm2" style="font-size:17px">${es(p.name)}</div><div class="meta2">${es(p.roots.join(', '))} · support ${f(p.support)} · exclusive ${f(e.n)} (${f(e.thm)} theorems, ${f(e.defs)} definitions, ${f(e.lines)} lines)</div><p class="note" style="margin:8px 0">${es(p.desc)}</p>`+
  (e.n?`<div style="color:var(--text-secondary)">Largest modules in the exclusive support:</div><ol>${e.mods.map(([m,c])=>`<li>${es(m)} <span class="meta2">${f(c)}</span></li>`).join('')}</ol><div style="color:var(--text-secondary)">Most-cited declarations in the exclusive support:</div><ol>${e.top.map(([n,k,c,s])=>`<li style="margin:6px 0"><b>${es(n.split('.').slice(-2).join('.'))}</b> <span class="meta2">${k}, cited ${c} times within the block</span>${X.math[n]?`<div class="note" style="margin:3px 0">${X.math[n]}</div>`:''}<details><summary style="cursor:pointer;color:var(--text-muted);font-size:12.5px">Lean statement</summary><div class="lean">${es(s)}</div></details></li>`).join('')}</ol>`:'<p>No declaration is exclusive to this pillar: everything it reaches is also reached by another pillar.</p>');PN.scrollIntoView({behavior:'smooth',block:'nearest'})}
})();
</script>
'''

ANCHOR = '<h2 class="tnr" id="s-docs">Documents</h2>'
KATEX_OLD = "renderMathInElement(document.getElementById('gnote'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"
KATEX_NEW = "['gnote','excltext','exclmatrix'].forEach(id=>{const e=document.getElementById(id);if(e)renderMathInElement(e,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})});document.querySelectorAll('#excl ~ p.sub').forEach(e=>renderMathInElement(e,{delimiters:[{left:'$',right:'$',display:false}]}))"
block = SECTION.replace('__EXCL__', json.dumps(X, ensure_ascii=False, separators=(',', ':')))
for p in files:
    s = open(p).read()
    if 'id="excl"' in s:
        a = s.index('<h2 class="tnr" id="excl">')
        b = s.index(ANCHOR)
        s = s[:a] + s[b:]
    assert s.count(ANCHOR) == 1, p
    s = s.replace(ANCHOR, block + ANCHOR).replace(KATEX_OLD, KATEX_NEW)
    open(p, 'w').write(s)
    print(p.split('/')[-1], 'ok')
