# Casos PHITS para validar y refinar los pesos del ridge filter

Base: `variantes oclusor dispersor/oclusor_chico_posicionador_arriba_mas_gel` (oclusor chico + dispersor + posicionador arriba,
fuente 19,5 MeV, atenuador en aire). Todos los casos usan **gel de 1,0 mm** (cara del gel en z = 60,28 cm; pouch de 2 mm en
z = 60,38-60,58 cm). El perfil en profundidad medido desde la cara del gel no depende del espesor de gel, asi que el gel/posicion
del pouch se elige despues con `eval_pouch.py` (ventana [g, g+T] o, para la pileta fija, [D-T, D]).
Cada caso: 5000 x 10000 = 5e7 historias (igual que el original). Los 19 casos se corren igual que el original (`compartida.slurm`).

## Casos (19)
| Tanda | Carpetas | Que cambia |
|---|---|---|
| A | `ref_N9`, `N10`, `N11`, `N12` | ridge original de 9 escalones y ridges de 10, 11 y 12 con pesos analiticos (anchos redondeados a 10 um); N12: espesor max 2,2 mm, anchos en `ridge_N12.txt` |
| B | `slab_t00` ... `slab_t22` | en lugar del ridge, una **lamina uniforme de PLA** de t = 0; 0,2; ... 2,2 mm (NN = decimas de mm). `slab_t00` es la misma geometria con la celda llena de **aire** (sin PLA). Sirven para medir la base B_t(x) |
| C | `N12_res025um`, `N12_res050um`, `N12_res100um` | N12 con anchos redondeados a 25, 50 y 100 um (la impresion real redondea asi) |

## Tallies (en todos los casos)
Los originales (`bragg_pouch_z.out`: dosis en profundidad r<0,5 cm, z 60,2-60,8 cm en 300 bins de 0,02 mm; `bragg_pouch_r`, `histograma_dosis`,
`espectro.out`, `track_xy`) mas tres nuevos:
- `espectro_entrada_pouch.out`: T-Track en una lamina de 0,1 mm (z 60,38-60,39 cm, |x|,|y|<0,5 cm), 0-20 MeV en 200 bins de 0,1 MeV, 1/cm2/MeV/fuente. Es el espectro que entra al pouch, sin deconvolucion.
- `espectro_entrada_anillos.out`: igual, en dos anillos (r 0-0,4 y 0,4-0,8 cm). El pouch del modelo mide +-0,8 cm en y, por eso no hay anillo mas externo.
- `bragg_pouch_z_anillos.out`: dosis en profundidad (mismo z y bins) en los dos anillos; un bloque por anillo (`--block 0/1`).

## Como evaluar
1. **Tanda A y C**, perfil en profundidad con la pileta fija (D = 2,5 mm: gel 0,5 mm + pouch 2 mm):
   `python3 eval_pouch.py casos/N12/out/bragg_pouch_z.out --front 60.28 --D 2.5`  (CV por espesor de pouch T)
   Con gel variable: `eval_pouch.py ... --front 60.28 --T 2.0 --gmax 1.5`.
   Anillos: `--block 0` y `--block 1` sobre `bragg_pouch_z_anillos.out`.
2. **Espectro**: comparar `espectro_entrada_pouch.out` con los pesos nominales (fraccion acumulada de alcances; ver `espectro_incidente.py` / `ridge_vs_espectro.py`, ya sin necesidad de deconvolucionar porque la lamina es fina; usar L = 0,01 cm).
3. **Tanda B**: pesos optimos a partir de la base,
   `python3 nnls_weights.py --glob 'casos/slab_t*/out/bragg_pouch_z.out' --front 60.28 --D 2.5 --Tmax 2.25`
   Imprime pesos, CV por ventana y los anchos completos para `gen_ridge.py --widths ...` (generar el ridge nuevo y simularlo para confirmar).

## Validacion hecha (sin PHITS)
- `check_exact.py casos/*`: para cada escalon evalua el espesor de PLA de la geometria generada en el centro del escalon y lo compara con el diseno: los 19 casos dan OK (periodo 0,6300 cm en los ridges; espesor de lamina = n x 0,2 mm en B).
- Los tres tallies nuevos se escribieron siguiendo el formato de los tallies existentes; **no se ejecutaron**: conviene mirar el primer `phits.out` por errores de sintaxis.
- `nnls_weights.py` y `eval_pouch.py` se probaron con una base sintetica (`test_sintetico.py`) y con la salida existente del repo; eso valida el calculo, no la fisica.

## Limites
- La ventana [D-T, D] desde la cara del gel incluye el gel (x < 1 mm en estos casos) y el pouch; la dosis se lee igual en ambos (densidades parecidas, 1,03-1,04 g/cm3).
- Un ridge con peso 0 en un escalon no se puede construir: `nnls_weights.py` impone un ancho minimo (`--minw`, 25 um).
- Estadistica: si el error relativo en el tally fino (0,02 mm) supera el 1 %, duplicar maxbch.
- N12_res100um (anchos a 100 um) es una cota del error de redondeo: probablemente se aparte del diseno.
- `slab_t00` y la geometria de los demas: la cara plana de salida queda en c77+11*c75 como en N12; en `ref_N9` queda en c77+8*c75 (0,6 mm mas arriba), diferencia en aire despreciable.
