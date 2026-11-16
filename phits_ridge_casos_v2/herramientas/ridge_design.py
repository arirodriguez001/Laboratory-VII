import numpy as np
from math import gamma
p=1.827; a=1-1/p; k=1.16   # water-equivalent factor of PLA
R0=2.85                    # mm, range from gel surface (arriba, ocl chico+disp+gel)
def weights(N):
    # step i has PLA thickness i*0.2 mm, i=0..N-1 ; shift s_i = k*0.2*i ; bin integral of s^(a-1)
    d=1.0
    w=[]
    for i in range(N):
        lo=max(i-0.5,0); hi=i+0.5
        w.append((hi**a-lo**a)/a)
    w=np.array(w); return w/w.sum()
def profile(wts, tsteps, sigma, z):
    # pristine: r^-a convolved with gaussian in range; z in mm, peaks at R_i = R0 - k*t
    rho=np.linspace(-1,4,5001); drho=rho[1]-rho[0]
    out=np.zeros_like(z)
    for w_,t in zip(wts,tsteps):
        Ri=R0-k*t
        G=np.exp(-0.5*((rho-Ri)/sigma)**2); G/=G.sum()*drho
        for j,zz in enumerate(z):
            m=rho>zz
            out[j]+=w_*np.sum(G[m]*(rho[m]-zz)**(-a))*drho
    return out
if __name__=="__main__":
    # current ridge (Excel factors by resolution, thickness 0..1.6 mm)
    cur=np.array([0.18,0.09,0.07,0.06,0.05,0.05,0.05,0.04,0.04]); cur/=cur.sum()
    z=np.linspace(0.0,R0-0.15,200)
    for sig in (0.03,0.06,0.09,0.12):
        res=[]
        for name,w,N in (("actual 9",cur,9),("analit 9",weights(9),9),("analit 10",weights(10),10),("analit 11",weights(11),11),("analit 12",weights(12),12)):
            t=0.2*np.arange(N); y=profile(w,t,sig,z)
            prox=R0-k*t.max()   # nominal proximal edge
            sel=(z>=prox+0.1)&(z<=R0-0.2)
            res.append((name, y[sel].std()/y[sel].mean()*100, prox))
        print("sigma",sig,"  ".join(f"{n}: CV {c:.1f}% (prox {pr:.2f})" for n,c,pr in res))
    print()
    for N in (9,10,11,12):
        w=weights(N); print(N,"pasos tmax=%.1f mm  W_ideal=%.2f mm"%(0.2*(N-1),k*0.2*(N-1)), "pesos:",np.round(w,3))
        print("   anchos (mm) con periodo 6.3 mm:",np.round(w*6.3,2))
