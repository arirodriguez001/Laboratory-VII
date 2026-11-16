#!/usr/bin/env python3
"""Compara la distribucion de alcances medida en la entrada del pouch (espectro T-Track deconvolucionado)
con la predicha por los pesos del ridge de 9 escalones. Uso: ridge_vs_espectro.py espectro.out L_cm"""
import sys, numpy as np
sys.path.insert(0,'/home/claude/scripts')
from espectro_incidente import read, S_water, R_water
d=read(sys.argv[1]); L=float(sys.argv[2])
lo,hi,y=d[:,0],d[:,1],d[:,2]; Ec=(lo+hi)/2
m=(Ec>5)&(y>0)
Phi=y[m]*np.array([S_water(e) for e in Ec[m]])*L
r=np.array([R_water(e) for e in Ec[m]])
Phi0=Phi[r<0.7].mean()        # meseta a baja energia = fluencia total que entra
F=Phi/Phi0
w=np.array([0.04,0.04,0.05,0.05,0.05,0.06,0.07,0.09,0.18]); w=w/w.sum()   # escalon 1 (grueso) ... 9 (fino, t=0)
t=np.arange(8,-1,-1)*0.2            # mm de PLA
shift=1.16*t                        # mm de agua
def pred(rr,r0):
    return np.array([w[shift>=r0-x-1e-9].sum() for x in rr])
best=None
for r0 in np.arange(2.2,2.7,0.01):
    # distribucion suavizada por el ancho del bin (~0.35 mm) con gaussiana sigma 0.15 mm
    from math import erf
    Fp=np.array([sum(wk*0.5*(1+erf(((r0-sk)-x)/(0.15*2**0.5))) for wk,sk in zip(w,shift)) for x in r])
    e=((Fp-F)**2).sum()
    if best is None or e<best[0]: best=(e,r0,Fp)
e,r0,Fp=best
print("Phi0 (meseta) = %.3e ; r0 ajustado = %.2f mm (E=%.2f MeV aprox)"%(Phi0,r0,np.interp(r0,[R_water(x) for x in np.linspace(5,20,300)],np.linspace(5,20,300))))
print(" E_c[MeV]  r=R(E)[mm]  F_medida(>E)  F_predicha_ridge")
for ec,rr,f,fp in zip(Ec[m],r,F,Fp): print("  %6.2f    %5.2f        %5.3f        %5.3f"%(ec,rr,f,fp))
print("Energia mediana incidente aprox (F=0.5): r=%.2f mm"%np.interp(0.5,F[::-1],r[::-1]))
