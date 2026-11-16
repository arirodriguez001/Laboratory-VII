#!/usr/bin/env python3
"""Evalua la homogeneidad de dosis en el pouch a partir de UN perfil bragg_pouch_z*.out simulado con gel grueso (1,0 mm).
La profundidad x se mide desde la cara frontal del gel (--front, z en cm).
Modos:
  (a) gel variable (default): ventana [g, g+T] y barrido de g.        eval_pouch.py out --front 60.28 --T 2.0 [--gmin 0 --gmax 1.5]
  (b) pileta fija (--D): la cara posterior del pouch esta en x = D mm; ventana [D-T, D] para varios T.
                                                                       eval_pouch.py out --front 60.28 --D 2.5 [--Ts 1.0,1.25,1.5,2.0,2.25,2.5]
--block N elige el N-esimo bloque del archivo (0 = primero); sirve para los archivos por anillos (bragg_pouch_z_anillos.out)."""
import argparse, numpy as np
ap=argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--front",type=float,required=True)
ap.add_argument("--T",type=float,default=2.0); ap.add_argument("--gmax",type=float,default=1.0)
ap.add_argument("--gmin",type=float,default=0.0); ap.add_argument("--D",type=float,default=None)
ap.add_argument("--Ts",default="1.0,1.25,1.5,2.0,2.25,2.5"); ap.add_argument("--block",type=int,default=0)
a=ap.parse_args()
blocks=[[]]
for l in open(a.out):
    t=l.split()
    if len(t)==4:
        try: v=[float(x) for x in t]
        except ValueError: continue
        if blocks[-1] and v[0]<blocks[-1][-1][0]: blocks.append([])
        blocks[-1].append(v)
R=np.array(blocks[a.block]); z=0.5*(R[:,0]+R[:,1]); y=R[:,2]
x=(z-a.front)*10.0                      # mm desde la cara del gel
def stats(s):
    m=y[s].mean(); return m, y[s].std()/m*100, y[s].min()/m, y[s].max()/m
if a.D is not None:
    print("pileta fija: cara posterior del pouch en x = %.2f mm desde el frente del gel; bloque %d"%(a.D,a.block))
    print("%6s %8s %8s %8s %8s %8s"%("T(mm)","g(mm)","media","CV(%)","min/med","max/med"))
    for T in [float(v) for v in a.Ts.split(",")]:
        s=(x>=a.D-T)&(x<=a.D)
        if s.sum()<5: continue
        print("%6.2f %8.2f %8.3f %8.2f %8.3f %8.3f"%((T,a.D-T)+stats(s)))
else:
    print("%6s %8s %8s %8s %8s"%("g(mm)","media","CV(%)","min/med","max/med"))
    best=None
    for g in np.arange(a.gmin,a.gmax+1e-9,0.05):
        s=(x>=g)&(x<=g+a.T)
        if s.sum()<5: continue
        row=(g,)+stats(s)
        print("%6.2f %8.3f %8.2f %8.3f %8.3f"%row)
        if best is None or row[2]<best[2]: best=row
    print("\nmejor g = %.2f mm  (CV = %.2f %%, min/med = %.3f, max/med = %.3f)"%(best[0],best[2],best[3],best[4]))
