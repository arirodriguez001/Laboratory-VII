#!/usr/bin/env python3
"""Prueba de la cadena de calculo con una base SINTETICA (modelo r^-a + gaussiana, no es fisica de PHITS):
escribe /tmp/synth/slab_tNN/out/bragg_pouch_z.out y se corre nnls_weights.py sobre ella.  Solo valida que el pipeline
(lectura de archivos, ventana, ajuste, anchos de salida) funciona; los pesos que salen NO sirven para imprimir."""
import numpy as np, os
a=1-1/1.827; k=1.16; R0=2.85; sig=0.08
rho=np.arange(-1,4,0.001)+0.0005; drho=0.001; x=np.arange(0,3.6,0.02)
def B(t):
    Ri=R0-k*t; G=np.exp(-0.5*((rho-Ri)/sig)**2); G/=G.sum()*drho
    return np.array([np.sum(G[rho>z]*(rho[rho>z]-z)**(-a))*drho for z in x])
for n in range(12):
    t=0.2*n; y=B(t); d="/tmp/synth/slab_t%02d/out"%round(t*10); os.makedirs(d,exist_ok=True)
    with open(d+"/bragg_pouch_z.out","w") as f:
        f.write("# sintetico\n")
        for xi,yi in zip(x,y): f.write(" %.5E %.5E %.5E %.4f\n"%(60.28+xi/10-0.001,60.28+xi/10+0.001,yi,0.01))
print("escrito en /tmp/synth; correr:\n  python3 nnls_weights.py --glob '/tmp/synth/slab_t*/out/bragg_pouch_z.out' --front 60.28 --D 2.5 --Tmax 2.25")
