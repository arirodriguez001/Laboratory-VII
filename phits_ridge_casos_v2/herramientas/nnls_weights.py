#!/usr/bin/env python3
"""Calcula los pesos (anchos de escalon) del ridge que dan la dosis mas plana, a partir de la base B_t(x) simulada
con laminas uniformes de PLA (casos slab_tNN, NN = t en decimas de mm: 00, 02, ..., 22).
  D(x) = sum_i w_i B_{t_i}(x),   w_i >= wmin (ancho minimo imprimible),  sum w_i = 1,  t_i = 0, 0.2, ..., (n-1)*0.2 mm
Se minimiza || A w - 1 ||^2 sobre la ventana [D - Tmax, D] (minimos cuadrados acotados) y luego se normaliza w; el nivel de dosis es libre.
Uso:
  nnls_weights.py --glob 'casos/slab_t*/out/bragg_pouch_z.out' --front 60.28 --D 2.5 --Tmax 2.25 [--period 0.63 --res 0.0025 --block 0]
Imprime pesos, anchos completos (cm, del escalon mas grueso al de espesor 0, listos para gen_ridge.py --widths) y el CV por
ventana [D-T, D] para: minimos cuadrados continuo y redondeado, pesos analiticos de N escalones y el ridge original de 9."""
import argparse, glob, os, re, sys
import numpy as np
from scipy.optimize import lsq_linear
ap=argparse.ArgumentParser()
ap.add_argument("--glob",required=True); ap.add_argument("--front",type=float,required=True)
ap.add_argument("--D",type=float,default=2.5); ap.add_argument("--Tmax",type=float,default=2.25)
ap.add_argument("--Ts",default="1.0,1.25,1.5,2.0,2.25"); ap.add_argument("--period",type=float,default=0.63)
ap.add_argument("--res",type=float,default=0.0025); ap.add_argument("--block",type=int,default=0)
ap.add_argument("--nmax",type=int,default=12)
ap.add_argument("--minw",type=float,default=0.0025,help="ancho completo minimo por escalon en cm (default 25 um, resolucion de la impresora)")
a=ap.parse_args()
def load(path,block):
    blocks=[[]]
    for l in open(path):
        t=l.split()
        if len(t)==4:
            try: v=[float(x) for x in t]
            except ValueError: continue
            if blocks[-1] and v[0]<blocks[-1][-1][0]: blocks.append([])
            blocks[-1].append(v)
    R=np.array(blocks[block]); return (0.5*(R[:,0]+R[:,1])-a.front)*10.0, R[:,2]
files=sorted(glob.glob(a.glob))
basis={}
for f in files:
    m=re.search(r"slab_t(\d\d)",f)
    if not m: continue
    t=int(m.group(1))/10.0; basis[round(t,1)]=load(f,a.block)
ts=sorted(basis)[:a.nmax]
if len(ts)<3: sys.exit("faltan casos slab_tNN: encontrados %s"%ts)
xg=np.arange(0.0,a.D+0.3,0.02)
A=np.array([np.interp(xg,*basis[t]) for t in ts]).T      # columnas = B_t en la grilla comun
win=(xg>=a.D-a.Tmax)&(xg<=a.D)
wmin=a.minw/a.period                       # un escalon con peso 0 no se puede construir: cota inferior = ancho minimo imprimible
sol=lsq_linear(A[win],np.ones(win.sum()),bounds=(np.full(len(ts),wmin),np.inf)); w=sol.x; lvl=1.0/w.sum(); w=w/w.sum()
def cv(wt,T):
    s=(xg>=a.D-T)&(xg<=a.D); d=A[s]@wt; return d.std()/d.mean()*100
def analytic(N,p=1.827):
    aa=1-1/p; ww=np.array([(( i+0.5)**aa-max(i-0.5,0)**aa)/aa for i in range(N)]); return ww/ww.sum()
def rounded(wt,res,period):
    full=np.round(wt*period/res)*res; full[0]+=period-full.sum(); return full/period
Ts=[float(v) for v in a.Ts.split(",")]
cands=[("minimos cuadrados (continuo)",w),("min. cuadrados redond. %.0f um"%(a.res*1e4),None)]
wr=rounded(w,a.res,a.period); cands[1]=(cands[1][0],wr)
for N in (9,10,11,12):
    if N<=len(ts): cands.append(("analitico N%d"%N,np.pad(analytic(N),(0,len(ts)-N))))
orig=np.array([0.18,0.09,0.07,0.06,0.05,0.05,0.05,0.04,0.04]); orig=orig/orig.sum()
if len(ts)>=9: cands.append(("ridge original 9",np.pad(orig,(0,len(ts)-9))))
print("Espesores de PLA disponibles (mm):",ts)
print("Ventana de ajuste: x en [%.2f, %.2f] mm desde el frente del gel; pileta fija D = %.2f mm\n"%(a.D-a.Tmax,a.D,a.D))
print("Pesos por espesor (fraccion de area):")
print("  t(mm)   "+"  ".join("%5.1f"%t for t in ts))
for name,wt in cands:
    print("  %-30s"%name+"  ".join("%5.3f"%v for v in wt))
print("\nCV (%) de la dosis en la ventana [D-T, D]:")
print("  %-30s"%"T (mm)"+"  ".join("%6.2f"%T for T in Ts))
for name,wt in cands:
    print("  %-30s"%name+"  ".join("%6.2f"%cv(wt,T) for T in Ts))
full=(wr*a.period)[::-1]                      # del mas grueso (indice n-1) al de espesor 0
keep=[x for x in full]
while keep and keep[0]<=0: keep.pop(0)      # descartar escalones gruesos con peso 0
print("\nanchos completos (cm) para gen_ridge.py --widths, escalon 1 (grueso) -> espesor 0 (%d escalones, tmax %.1f mm):"%(len(keep),0.2*(len(keep)-1)))
print(",".join("%.4f"%x for x in keep))
print("nivel de dosis relativo del ridge optimizado = %.3f (unidades del tally por fuente)"%lvl)
