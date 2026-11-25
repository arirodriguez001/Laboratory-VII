#!/usr/bin/env python3
"""Verificacion exacta de la geometria generada: para cada escalon evalua el espesor de PLA en el centro del escalon
y lo compara con el diseno (espesor del escalon k = (N-k)*c75); para laminas compara el espesor total.
Uso: check_exact.py caso_dir ..."""
import sys, re, glob, os, importlib.util
import numpy as np
here = os.path.dirname(os.path.abspath(__file__)); args = sys.argv[1:]; sys.argv = sys.argv[:1]
spec = importlib.util.spec_from_file_location("cg", os.path.join(here, "check_geom.py"))
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
ORIG = [0.04, 0.04, 0.05, 0.05, 0.05, 0.06, 0.07, 0.09, 0.18]
def thick(su, x):
    surf, sets, val = cg.load(su); t = open(su).read().replace('\r', '')
    c75 = val('c75'); c77 = val('c77')
    top = val(re.search(r'^1629\s+%pin_TR%\s+PZ\s+(.*?)\s*(\$|$)', t, flags=re.M).group(1))
    zz = np.linspace(c77 + 1e-9, top - 1e-9, 4000)
    return np.mean([cg.inside(sets, surf, x, z) for z in zz]) * (top - c77), c75, val('c71')
ok = True
for d in [x for x in args if os.path.isdir(x)]:
    name = os.path.basename(d.rstrip('/'))
    su = [s for s in glob.glob(d + '/dat/Su_ridge_filter_*.inp') if (not s.endswith('_9.inp')) or name == 'ref_N9'][0]
    desc = glob.glob(d + '/ridge_*.txt'); lam = glob.glob(d + '/lamina_*.txt')
    if lam:
        n = int(re.search(r'flat(\d+)', su).group(1)); exp = max(n, 1) * 0.02
        th1, _, c71 = thick(su, 0.3); th2, _, _ = thick(su, 0.01)
        good = abs(th1 - exp) < 1e-3 and abs(th2 - exp) < 1e-3; ok &= good
        print("%-14s lamina n=%-2d espesor %.3f cm (esperado %.3f)%s  %s" % (name, n, th1, exp, "  [material AIRE]" if n == 0 else "", "OK" if good else "ERROR"))
        continue
    if desc:
        txt = open(desc[0]).read().split('espesor 0):')[-1]
        w = [float(x) for x in re.findall(r'float64\(([0-9.]+)\)', txt)] or [float(x) for x in re.findall(r'[0-9]+\.[0-9]+|[0-9]+e-?[0-9]+', txt)]
    else:
        w = ORIG
    N = len(w); cum = 0.0; bad = []
    for k, wk in enumerate(w, 1):
        xc = cum + wk / 4            # centro del escalon k en x>0: tramo [cum, cum+wk/2]
        th, c75, c71 = thick(su, xc); cum += wk / 2
        if abs(th - (N - k) * c75) > 1e-3: bad.append((k, round(th, 3), round((N - k) * c75, 3)))
    ok &= not bad
    print("%-14s N=%-2d periodo=%.4f cm  %s %s" % (name, N, sum(w), "OK" if not bad else "ERROR", bad if bad else ""))
print("TODO OK" if ok else "HAY ERRORES")
