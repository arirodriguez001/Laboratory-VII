import re, sys, numpy as np
def load(path):
    t=open(path).read().replace('\r','')
    env={}
    for m in re.finditer(r'^set:\s*(c\d+)\[\s*(.*?)\s*\]',t,flags=re.M):
        env[m.group(1)]=m.group(2)
    def val(expr,seen=0):
        e=expr
        for _ in range(5):
            e=re.sub(r'c\d+',lambda m: '('+env[m.group(0)]+')' if m.group(0) in env else m.group(0),e)
        return eval(e)
    surf={}
    for m in re.finditer(r'^(\d{4})\s+(?:%pin_TR%\s+)?(PX|PZ)\s+(.*?)(?:\$.*)?$',t,flags=re.M):
        n=int(m.group(1)); 
        if n<1627: continue
        surf[n]=(m.group(2), val(m.group(3).strip()))
    sets={}
    for m in re.finditer(r'^set:%ridge_ladder_(\w)%\[(.*)\]',t,flags=re.M):
        sets[m.group(1)]=m.group(2)
    return surf,sets,val
def inside(sets,surf,x,z):
    def ok(sn):
        s=int(sn); typ,v=surf[abs(s)]; c=x if typ=='PX' else z
        return (c>v) if s>0 else (c<v)
    for g in sets.values():
        for term in g.split(':'):
            ids=re.findall(r'-?\d+',term)
            if all(ok(i) for i in ids): return True
    return False
def thickness_profile(path):
    surf,sets,val=load(path)
    t=open(path).read().replace('\r','')
    c71=val('c71'); c75=val('c75'); c77=val('c77')
    top=surf[1629][1] if 1629 in surf else None
    m=re.search(r'^1629\s+%pin_TR%\s+PZ\s+(.*?)\s*(\$|$)',t,flags=re.M); top=val(m.group(1))
    xs=np.linspace(0,c71,4001)[1:]   # medio periodo
    zs=np.linspace(c77,top,200001)
    th=[]
    for x in xs[::40]:
        # espesor = longitud de z dentro de PLA, via fraccion
        n=800; zz=np.linspace(c77+1e-9,top-1e-9,n)
        f=np.mean([inside(sets,surf,x,z) for z in zz])
        th.append(f*(top-c77))
    th=np.array(th); xs=xs[::40]
    # agrupar por niveles
    lv=np.round(th/c75).astype(int)
    out=[]; 
    for L in sorted(set(lv),reverse=True):
        sel=xs[lv==L]; out.append((L*c75, 2*(sel.max()-sel.min()+ (xs[1]-xs[0])*0) ))
    return c75,c71,out,top-c77
for p in sys.argv[1:]:
    c75,c71,out,H=thickness_profile(p)
    print(p.split('/')[-3] if '/casos/' in p else p.split('/')[-2]); print("  periodo=%.4f cm  altura grilla=%.3f cm"%(2*c71,H))
    print("  (espesor cm, ancho aprox cm):",[(round(a,3),round(b,3)) for a,b in out])
