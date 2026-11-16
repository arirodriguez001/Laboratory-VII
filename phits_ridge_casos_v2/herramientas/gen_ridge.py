#!/usr/bin/env python3
"""Genera Su_ridge_filter_N.inp y Ce_ridge_filter_N.inp (PHITS) para un ridge de escalera simetrica.
Convencion del ridge original (9 escalones): escalon k=1 es el mas grueso (angosto, en el centro) y el
escalon N es el de espesor cero (el mas ancho).  Espesor del escalon k = (N-k)*c75.
Uso:
  gen_ridge.py --template DAT_ORIG --out DAT_NUEVO --N 11 [--dstep 0.02] [--period 0.63] [--res 0.005]
  gen_ridge.py --template DAT_ORIG --out DAT_NUEVO --widths 0.04,0.04,...,0.18 [--dstep 0.02]   # anchos completos en cm, del mas grueso al de espesor 0
"""
import argparse, os, re
import numpy as np

def analytic_weights(N, p=1.827):
    """Fracciones de area por escalon, indice 0 = espesor 0 (mayor peso). w(s) ~ s^(a-1), a = 1-1/p."""
    a = 1 - 1/p
    w = []
    for i in range(N):
        lo = max(i - 0.5, 0.0); hi = i + 0.5
        w.append((hi**a - lo**a) / a)
    w = np.array(w); return w / w.sum()

def widths_from_weights(N, period, res):
    w = analytic_weights(N)                       # w[i]: espesor i*dstep
    full = w * period                              # cm
    full = np.round(full / res) * res              # discretizar a la resolucion de impresion
    full[0] += period - full.sum()                 # ajustar el escalon ancho para conservar el periodo
    # orden del input: escalon 1 = mas grueso = indice N-1 ... escalon N = indice 0
    return list(full[::-1])

def nm(k):
    """c701..c709 como el original; pasos 10..18 -> c791..c799 (evita nombres de 4 digitos)."""
    return 'c70%d' % k if k <= 9 else 'c79%d' % (k - 9)

def fmt(x):
    return ('%.6g' % x)

def build_su(template_su, full_widths, dstep):
    N = len(full_widths)
    txt = template_su.replace('\r', '')
    lines = txt.split('\n')
    out = []
    i = 0
    # 1) cabecera de parametros
    out.append(lines[0])                           # c70
    for k, w in enumerate(full_widths, 1):
        out.append('set: %s[ %s/2 ]\t$step %d width' % (nm(k), fmt(w), k))
    out.append('set: c71[ ' + ' + '.join(nm(k) for k in range(1, N+1)) + ' ]\t$half width')
    # lineas c75, c76, c77, %pin_TR% originales
    idx = next(j for j, l in enumerate(lines) if l.startswith('set: c75'))
    out.append('set: c75[ %s ]\t$steps thickness' % fmt(dstep))
    j = idx + 1
    while not lines[j].startswith('$[ Surface ]'):
        out.append(lines[j]); j += 1
    # 2) superficies hasta el ladder
    while not lines[j].startswith('$RIDGE filter ladder'):
        l = lines[j]
        if re.match(r'^1629 ', l):
            l = '1629 %pin_TR% PZ (c77+' + str(N-1) + '*c75)\t$bottom of ladders'
        out.append(l); j += 1
    out.append(lines[j])                           # $RIDGE filter ladder (U=2)
    # 3) escalera
    terms = []
    s = 1632
    cum = []
    for k in range(1, N):                          # escalones 1..N-1
        cum.append(nm(k))
        c = '+'.join(cum)
        pxm, pxp, pz = s, s+1, s+2
        out.append('$step %d' % k)
        out.append('%d PX -(%s)' % (pxm, c))
        out.append('%d PX  (%s)' % (pxp, c))
        if k < N-1:
            out.append('%d %%pin_TR%% PZ (c77+%s)' % (pz, 'c75' if k == 1 else '%d*c75' % k))
        if k == 1:
            terms.append('(%d -%d)' % (pxm, pxp))
        else:
            terms.append('(%d %d -%d)' % (prev_pz, pxm, pxp))
        prev_pz = pz
        s += 3
    names = []
    for g in range(0, len(terms), 5):
        lab = 'abcdefgh'[g//5]
        names.append(lab)
        out.append('set:%%ridge_ladder_%s%%[%s]' % (lab, ':'.join(terms[g:g+5])))
    return '\n'.join(out), names

def build_ce(template_ce, N, names):
    txt = template_ce.replace('\r', '')
    chain = ' \n\t\t\t: '.join('%ridge_ladder_' + n + '%' for n in names)
    txt = re.sub(r'2606 %PLA%.*?\$ladder', '2606 %PLA% ' + chain + ' U=4\t$ladder', txt, flags=re.S)
    txt = re.sub(r'2607 %air%.*?\$air', '2607 %air% #(' + chain + ') U=4\t$air', txt, flags=re.S)
    sm = '+'.join((nm(k) if N-k == 1 else '%d*%s' % (N-k, nm(k))) for k in range(1, N))
    txt = re.sub(r'set:%vol_rfgrid%\[.*?\]\s*\$PI',
                 'set:%vol_rfgrid%[(15.850477*c75*(' + sm + ')/c71)] $PI', txt)
    return txt

def build_flat(template_su, template_ce, n, ngrid=12):
    """Reemplaza el ridge por una lamina uniforme de PLA de espesor n*c75 sobre todo el periodo.
    La cara plana (aguas abajo) queda en c77+(ngrid-1)*c75, igual que un ridge de ngrid escalones; la lamina crece
    hacia aguas arriba.  n=0 -> sin PLA (la celda se llena con aire).  Mantiene los anchos c701..c709 del template
    solo para definir c71 (periodo de la celda)."""
    nn = max(n, 1)
    su = template_su.replace('\r', '').split('\n')
    out = []; j = 0
    while not su[j].startswith('$RIDGE filter ladder'):
        l = su[j]
        if re.match(r'^1629 ', l):
            l = '1629 %pin_TR% PZ (c77+' + str(ngrid-1) + '*c75)\t$bottom of ladders'
        out.append(l); j += 1
    out.append(su[j])
    out.append('$flat slab: %d steps of c75 (n=0 -> air)' % n)
    out.append('1632 %%pin_TR%% PZ (c77+%d*c75)' % (ngrid-1-nn))
    out.append('set:%ridge_ladder_a%[(1632 1630 -1631)]')
    ce = template_ce.replace('\r', '')
    mat = '%PLA%' if n > 0 else '%air%'
    ce = re.sub(r'2606 %PLA%.*?\$ladder', '2606 ' + mat + ' %ridge_ladder_a% U=4\t$ladder', ce, flags=re.S)
    ce = re.sub(r'2607 %air%.*?\$air', '2607 %air% #(%ridge_ladder_a%) U=4\t$air', ce, flags=re.S)
    ce = re.sub(r'set:%vol_rfgrid%\[.*?\]\s*\$PI', 'set:%vol_rfgrid%[(15.850477*c75*' + str(nn) + ')] $PI', ce)
    return '\n'.join(out), ce

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--N', type=int); ap.add_argument('--widths')
    ap.add_argument('--dstep', type=float, default=0.02)
    ap.add_argument('--period', type=float, default=0.63)
    ap.add_argument('--res', type=float, default=0.005)
    ap.add_argument('--tag', default=None)
    ap.add_argument('--flat', type=int, default=None, help='n escalones de c75: lamina uniforme en lugar del ridge')
    ap.add_argument('--ngrid', type=int, default=12)
    a = ap.parse_args()
    if a.flat is not None:
        su = open(os.path.join(a.template, 'Su_ridge_filter_9.inp')).read()
        ce = open(os.path.join(a.template, 'Ce_ridge_filter_9.inp')).read()
        su_new, ce_new = build_flat(su, ce, a.flat, a.ngrid); tag = a.tag or 'flat%d' % a.flat
        os.makedirs(a.out, exist_ok=True)
        open(os.path.join(a.out, 'Su_ridge_filter_%s.inp' % tag), 'w', newline='\n').write(su_new)
        open(os.path.join(a.out, 'Ce_ridge_filter_%s.inp' % tag), 'w', newline='\n').write(ce_new)
        print('lamina uniforme: %d x c75 = %.3f mm de PLA' % (a.flat, a.flat*a.dstep*10)); raise SystemExit
    if a.widths: fw = [float(x) for x in a.widths.split(',')]
    else: fw = widths_from_weights(a.N, a.period, a.res)
    N = len(fw); tag = a.tag or str(N)
    su = open(os.path.join(a.template, 'Su_ridge_filter_9.inp')).read()
    ce = open(os.path.join(a.template, 'Ce_ridge_filter_9.inp')).read()
    su_new, names = build_su(su, fw, a.dstep); ce_new = build_ce(ce, N, names)
    os.makedirs(a.out, exist_ok=True)
    open(os.path.join(a.out, 'Su_ridge_filter_%s.inp' % tag), 'w', newline='\n').write(su_new)
    open(os.path.join(a.out, 'Ce_ridge_filter_%s.inp' % tag), 'w', newline='\n').write(ce_new)
    print('N=%d escalones, espesor max=%.3f cm, periodo=%.4f cm' % (N, (N-1)*a.dstep, sum(fw)))
    print('anchos completos (cm), escalon 1 (grueso) -> N (espesor 0):', [round(x, 4) for x in fw])
