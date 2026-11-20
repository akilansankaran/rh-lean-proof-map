import json
import sys

X = json.load(open(sys.argv[1]))
files = sys.argv[2:]

SECTION = r'''<h2 class="tnr" id="excl">Where the new mathematics lies</h2>
<div id="excltext" class="tnr" style="font-size:16px;line-height:1.6;max-width:1100px">
<p>For a pillar $p$ of the proof let $D(p)$ be the set of declarations its proof reaches, and let
$$E(p) \;=\; D(p) \setminus \bigcup_{q \neq p} D(q)$$
be its exclusive support, the part of the formalization that serves $p$ and nothing else. The six pillars below together reach 128,464 of the 128,479 declarations under riemannHypothesis.</p>
<p>Three findings stand out. First, local Langlands and the theta lifts are not independent blocks: $D(\texttt{recTExists})$ lies entirely inside the support of the Galois representations, as do 289 of the 291 declarations under TLiftK, so both enter the proof as ingredients of the construction of Galois representations, which alone holds 78,765 exclusive declarations, or 61% of the proof. Second, the Selmer bound VWin reaches 28,257 declarations, of which 14,315 are shared with the Galois block and 13,934 are its own, concentrated in archimedean base change, block decompositions and inertia eigenvalues. Third, the bridge from VWin to nonvanishing is almost disjoint from everything else: 18,825 of its 19,182 declarations (98%) are exclusive, and they lie in arithmetic geometry, namely embedded resolution of singularities, the arithmetic Hilbert–Samuel theorem and ampleness of heights. If the proof contains a genuinely new argument, these two blocks, the Selmer bound and the height-theoretic bridge, are where a reader should look first.</p>
</div>
<div class="legend" id="legend4" style="margin-top:10px"></div>
<svg id="exclbars" role="img" aria-label="Support of each pillar, split into exclusive and shared parts"></svg>
<h3 class="tnr" style="font-size:17px;margin:18px 0 6px">Containment between pillars</h3>
<p class="sub tnr" style="font-size:15px">Row $a$, column $b$: the share of $D(a)$ that also lies in $D(b)$.</p>
<div id="exclmatrix"></div>
<div id="exclpanel" style="background:var(--surface-2);border-radius:8px;padding:14px 16px;margin-top:12px">Select a pillar to list the modules and declarations in its exclusive support.</div>
<script>
(function(){
const X=__EXCL__;
const NS='http://www.w3.org/2000/svg',mk=(t,a={},p)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e};
const f=n=>n.toLocaleString('en-US'),es=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const tip=document.getElementById('tip');
document.getElementById('legend4').innerHTML='<span><i style="background:#555"></i>exclusive support (pillar colour)</span><span><i style="background:#cfcec9"></i>shared with another pillar</span>'.replace('colour','color');
const P=X.pillars,W=1560,rowH=46,ml=230,mr=380,H=P.length*rowH+40,svg=document.getElementById('exclbars');
svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width','100%');
const mx=Math.max(...P.map(p=>p.support)),sx=v=>(W-ml-mr)*v/mx;
[0,.25,.5,.75,1].forEach(t=>{const x=ml+sx(mx*t);mk('line',{x1:x,x2:x,y1:10,y2:H-24,stroke:'var(--rule)'},svg);const l=mk('text',{x,y:H-6,'text-anchor':'middle','font-size':12,fill:'var(--text-muted)'},svg);l.textContent=f(Math.round(mx*t))});
P.forEach((p,i)=>{const y=14+i*rowH,g=mk('g',{style:'cursor:pointer'},svg),ex=p.excl.n,sh=p.support-ex;
  const lb=mk('text',{x:ml-12,y:y+20,'text-anchor':'end','font-size':15,fill:'var(--text-primary)',style:"font-family:'Times New Roman',Times,serif"},g);lb.textContent=p.name;
  mk('rect',{x:ml,y,width:Math.max(1,sx(ex)),height:28,rx:3,fill:p.color},g);
  if(sh>0)mk('rect',{x:ml+sx(ex)+(ex?2:0),y,width:Math.max(1,sx(sh)-(ex?2:0)),height:28,rx:3,fill:'#cfcec9'},g);
  const v=mk('text',{x:ml+sx(p.support)+8,y:y+19,'font-size':13,fill:'var(--text-secondary)'},g);v.textContent=`${f(ex)} exclusive of ${f(p.support)} (${(100*p.share).toFixed(1)}% of the proof)`;
  mk('rect',{x:0,y:y-6,width:W,height:rowH-4,fill:'transparent'},g);
  g.addEventListener('mousemove',e=>{tip.style.display='block';tip.innerHTML=`<div class="nm">${es(p.name)}</div><div class="md">${es(p.roots.join(', '))}</div><div class="note">${es(p.desc)}</div><div>support ${f(p.support)} · exclusive ${f(ex)} · ${f(p.excl.lines)} lines exclusive</div>`;tip.style.left=Math.min(e.clientX+16,innerWidth-520)+'px';tip.style.top=(e.clientY+16)+'px'});
  g.addEventListener('mouseleave',()=>tip.style.display='none');g.addEventListener('click',()=>show(i))});
let h='<table style="width:auto;border-collapse:collapse"><tr><th></th>'+P.map(p=>`<th style="font-size:13px;padding:6px 8px;font-family:'Times New Roman',Times,serif">${es(p.name)}</th>`).join('')+'</tr>';
P.forEach((a,i)=>{h+=`<tr><th style="text-align:right;font-size:13px;padding:6px 8px;font-family:'Times New Roman',Times,serif">${es(a.name)}</th>`;
  P.forEach((b,j)=>{const v=a.support?X.overlap[i][j]/a.support:0,al=(.08+.8*v).toFixed(2);
    h+=`<td title="${f(X.overlap[i][j])} of ${f(a.support)}" style="text-align:center;font-size:13px;padding:7px 10px;border:2px solid var(--surface-1);background:rgba(42,120,214,${al});color:${v>.55?'#fff':'var(--text-primary)'};font-variant-numeric:tabular-nums">${i===j?'·':(100*v).toFixed(v>0&&v<.01?1:0)+'%'}</td>`});h+='</tr>'});
document.getElementById('exclmatrix').innerHTML=h+'</table>';
function show(i){const p=P[i],e=p.excl;
  document.getElementById('exclpanel').innerHTML=`<div class="nm2" style="font-size:17px">${es(p.name)}</div><div class="meta2">${es(p.roots.join(', '))} · support ${f(p.support)} · exclusive ${f(e.n)} (${f(e.thm)} theorems, ${f(e.defs)} definitions, ${f(e.lines)} lines)</div><p class="note" style="margin:8px 0">${es(p.desc)}</p>`+
  (e.n?`<div style="color:var(--text-secondary)">Largest modules in the exclusive support:</div><ol>${e.mods.map(([m,c])=>`<li>${es(m)} <span class="meta2">${f(c)}</span></li>`).join('')}</ol><div style="color:var(--text-secondary)">Most-cited declarations in the exclusive support:</div><ol>${e.top.map(([n,k,c,s])=>`<li><b>${es(n.split('.').slice(-2).join('.'))}</b> <span class="meta2">${k}, cited ${c} times within the block</span><div class="lean">${es(s)}</div></li>`).join('')}</ol>`:'<p>No declaration is exclusive to this pillar: everything it reaches is also reached by another pillar.</p>')}
})();
</script>
'''

ANCHOR = '<h2 class="tnr">Documents</h2>'
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
