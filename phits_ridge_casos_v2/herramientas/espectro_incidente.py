#!/usr/bin/env python3
"""Deconvoluciona un espectro T-Track (flujo por MeV) medido DENTRO de un volumen de agua de espesor L
para recuperar la fluencia incidente acumulada Phi_{>E}.
Relacion: phi(E) * S(E) * L = Phi_{>E}   (proton frenandose dentro del volumen; valida mientras el proton
que entra con E0>E todavia pasa por E dentro del volumen).
Uso: espectro_incidente.py archivo.out L_cm"""
import sys, re, numpy as np
me=0.510999; mp=938.272; K=0.307075
def S_water(E):  # MeV/cm, Bethe, I=75 eV, sin correcciones de capa (ok > 3 MeV)
    I=75e-6; g=1+E/mp; b2=1-1/g**2
    Tmax=2*me*b2*g**2/(1+2*g*me/mp+(me/mp)**2)
    return K*0.5551/b2*(0.5*np.log(2*me*b2*g**2*Tmax/I**2)-b2)
def R_water(E):  # CSDA mm, integracion numerica
    e=np.linspace(0.05,E,4000); return np.trapezoid(1/S_water(e),e)*10 + 0.0
def read(fn):
    rows=[]
    for l in open(fn):
        if l.startswith('#') or not l.strip(): continue
        p=l.split()
        if len(p)>=3:
            try: rows.append([float(p[0]),float(p[1]),float(p[2]),float(p[3]) if len(p)>3 else 0])
            except ValueError: pass
    return np.array(rows)
def analyze(fn,L):
    d=read(fn); lo,hi,y=d[:,0],d[:,1],d[:,2]; Ec=(lo+hi)/2
    m=y>0
    print("== %s  (L=%.2f mm)"%(fn.split('laboratory-vii/')[-1],L*10))
    print("  E_c[MeV]   phi[1/cm2/MeV]   phi*S*L [=Phi>E]   R(E)[mm]")
    for e,yy in zip(Ec[m],y[m]):
        print("  %7.3f   %12.4e   %14.4e   %6.3f"%(e,yy,yy*S_water(e)*L,R_water(e)))
    return Ec,y
if __name__=="__main__":
    analyze(sys.argv[1],float(sys.argv[2]))
