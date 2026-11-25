#!/usr/bin/env python3
"""Genera todos los casos PHITS (tandas A, B y C) a partir del caso base 'oclusor chico + dispersor + posicionador arriba + gel'.
Todos con gel de 1,0 mm: el perfil en profundidad medido desde la cara del gel no depende de g; g se elige despues
con eval_pouch.py.  Tally Bragg fino 60.2-60.8 cm en 300 bins (0,02 mm).
  A  ref_N9, N10, N11, N12           ridges de 9 a 12 escalones (pesos analiticos; N9 = ridge original)
  B  slab_t00 ... slab_t22           lamina uniforme de PLA de t mm (t = 0, 0.2, ..., 2.2) en lugar del ridge
  C  N12_res025um/050um/100um        N12 con anchos de escalon redondeados a la resolucion de impresion
Tallies agregados a todos: espectro fino (0,1 MeV) en lamina de 0,1 mm a la entrada del pouch, total y por anillos,
y dosis en profundidad por anillos."""
import os, shutil, re, subprocess, sys
SRC="/home/claude/arirodriguez001/laboratory-vii/variantes oclusor dispersor/oclusor_chico_posicionador_arriba_mas_gel"
DST="/home/claude/phits_new/casos"
GEN="/home/claude/phits_new/gen_ridge.py"
GEL=1.0   # mm
EXTRA_TALLIES = """

[T-Track]
title = Espectro de protones en la entrada del pouch (lamina de 0.1 mm, bins de 0.1 MeV)
mesh = xyz
x-type = 2
nx = 1
xmin = -0.5
xmax = 0.5
y-type = 2
ny = 1
ymin = -0.5
ymax = 0.5
z-type = 2
nz = 1
zmin = 60.38
zmax = 60.39
part = proton
e-type = 2
emin = 0.0
emax = 20.0
ne = 200
axis = eng
unit = 2
file = ./out/espectro_entrada_pouch.out
epsout = 1

[T-Track]
title = Espectro en la entrada del pouch por anillos (0-0.4 y 0.4-0.8 cm)
mesh = r-z
r-type = 2
rmin = 0.0
rmax = 0.8
nr = 2
z-type = 2
zmin = 60.38
zmax = 60.39
nz = 1
part = proton
e-type = 2
emin = 0.0
emax = 20.0
ne = 200
axis = eng
unit = 2
file = ./out/espectro_entrada_anillos.out
epsout = 1

[T-Deposit]
title = Bragg peak en el pouch por anillos (0-0.4 y 0.4-0.8 cm)
mesh = r-z
r-type = 2
rmin = 0.0
rmax = 0.8
nr = 2
z-type = 2
zmin = 60.2
zmax = 60.8
nz = 300
part = proton
output = dose
unit = 0
axis = z
file = ./out/bragg_pouch_z_anillos.out
epsout = 1
"""
def base(name):
    d=os.path.join(DST,name); os.makedirs(d+"/out"); os.makedirs(d+"/talies")
    for f in ("principal.inp","phits.in","compartida.slurm"): shutil.copy(os.path.join(SRC,f), d)
    shutil.copytree(SRC+"/dat", d+"/dat")
    shutil.copy(SRC+"/talies/tallies.inp", d+"/talies/tallies.inp")
    return d
def set_ridge(d, tag):
    p=d+"/principal.inp"; s=open(p,"rb").read().decode()
    s=s.replace("infl:{./dat/Su_ridge_filter_9.inp}","infl:{./dat/Su_ridge_filter_%s.inp}"%tag).replace("infl:{./dat/Ce_ridge_filter_9.inp}","infl:{./dat/Ce_ridge_filter_%s.inp}"%tag)
    assert "Su_ridge_filter_%s.inp"%tag in s and "Ce_ridge_filter_%s.inp"%tag in s
    open(p,"wb").write(s.encode())
def finish(d, name):
    front="%.3f"%(60.38-GEL/10)
    p=d+"/principal.inp"; s=open(p,"rb").read().decode()
    assert "60.305 60.58" in s
    s=s.replace("60.305 60.58","%s 60.58"%front).replace("0.25cm de altura total, 0.075 respecto pouch","gel %.2f mm respecto pouch"%GEL)
    open(p,"wb").write(s.encode())
    p=d+"/talies/tallies.inp"; s=open(p,"rb").read().decode()
    s=re.sub(r"(zmin = )60(\s*\r?\n\s*zmax = )62(\s*\r?\n\s*nz = )300", r"\g<1>60.2\g<2>60.8\g<3>300", s)
    assert "zmin = 60.2" in s
    nl = "\r\n" if "\r\n" in s else "\n"
    s = s.rstrip() + nl + EXTRA_TALLIES.replace("\n", nl)
    open(p,"wb").write(s.encode())
    p=d+"/compartida.slurm"; s=open(p,"rb").read().decode()
    assert '"oclchicoposarribamasgel"' in s
    s=s.replace('"oclchicoposarribamasgel"','"ridge_%s"'%name)
    open(p,"wb").write(s.encode())
shutil.rmtree(DST, ignore_errors=True); os.makedirs(DST)
# --- Tanda A
for name,N in (("ref_N9",9),("N10",10),("N11",11),("N12",12)):
    d=base(name)
    if N!=9:
        tag="N%d"%N
        subprocess.check_call([sys.executable,"-I",GEN,"--template",SRC+"/dat","--out",d+"/dat","--tag",tag,"--res","0.001","--N",str(N)], stdout=open(d+"/ridge_%s.txt"%tag,"w"))
        set_ridge(d,tag)
    finish(d,name)
# --- Tanda B: laminas uniformes
for n in range(0,12):
    t=n*0.2; name="slab_t%02d"%round(t*10)
    d=base(name); tag="flat%d"%n
    subprocess.check_call([sys.executable,"-I",GEN,"--template",SRC+"/dat","--out",d+"/dat","--tag",tag,"--flat",str(n),"--ngrid","12"], stdout=open(d+"/lamina_%s.txt"%tag,"w"))
    set_ridge(d,tag); finish(d,name)
# --- Tanda C: N12 con anchos redondeados
for um,res in ((25,0.0025),(50,0.005),(100,0.01)):
    name="N12_res%03dum"%um; d=base(name); tag="N12r%d"%um
    subprocess.check_call([sys.executable,"-I",GEN,"--template",SRC+"/dat","--out",d+"/dat","--tag",tag,"--N","12","--res",str(res)], stdout=open(d+"/ridge_%s.txt"%tag,"w"))
    set_ridge(d,tag); finish(d,name)
print(sorted(os.listdir(DST)))
