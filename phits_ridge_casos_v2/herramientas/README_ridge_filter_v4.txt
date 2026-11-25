LABORATORIO VII — RIDGE FILTER TANDAR
Guía rápida del notebook (versión 2)
====================================

ARCHIVO: Analisis_ridge_filter_TANDAR_v4.ipynb

1. CÓMO USARLO
---------------
Guardar el notebook en la raíz de phits_ridge_casos_v2:

    phits_ridge_casos_v2/
        Analisis_ridge_filter_TANDAR_v4.ipynb
        README_ridge_filter.txt
        casos/
        herramientas/

Abrirlo en Jupyter o VS Code y ejecutar las celdas en orden.
Si faltan librerías: pip install numpy pandas scipy matplotlib

No ejecuta PHITS ni modifica los inputs. Lee los resultados .out
que ya existen. No hace falta repetir las corridas para abrirlo.

2. QUÉ HACE CADA CELDA
----------------------
La numeración incluye las celdas de texto (Markdown).

01 | Texto — Introducción
     Explica el objetivo del notebook y cómo utilizarlo.

02 | Código — Configuración
     Importa librerías y fija la carpeta, el origen de profundidad,
     el gel (1 mm), el pouch (2 mm), el período (6,3 mm), la
     resolución provisional (25 µm por lado) y las historias objetivo.

03 | Texto — Unidades
     Explica la escala de dosis para 1 nA nominal de la fuente.
     El perfil registra dosis de protones, no dosis total.

04 | Código — Lectura y control de simulaciones
     Lee bragg_pouch_z.out de cada caso. Muestra una tabla con
     historias, estado de finalización, errores geométricos,
     incertidumbres estadísticas y CV dentro del pouch.
     Una corrida completa requiere 50 millones de historias y END.

05 | Texto — Coordenadas
     Explica que x=0 es la entrada del gel y que el pouch ocupa
     x=1 a 3 mm. La profundidad x no es la z global de PHITS.

06 | Código — Picos de Bragg individuales
     Grafica los slabs, calcula la posición y dosis del máximo,
     el cruce distal al 90 % y el ajuste lineal espesor–posición.
     Sirve para ver cuánto se desplaza el pico al agregar PLA.
     El asterisco (*) indica una corrida parcial.
     También calcula FWHM (ancho al 50 %) y ancho al 90 %,
     interpolando los cruces a ambos lados del máximo.
     Muestra la separación entre máximos consecutivos y su relación
     con el FWHM medio del par. Grafica anchos, separaciones y la
     superposición de cada par de picos con máximos igualados.
     El J local mide la variación de esa suma entre los máximos.
     Es solo un diagnóstico: no cambia las dosis ni los pesos
     de los optimizadores. NaN indica un cruce no encontrado.
     Los avisos indican interfaces, cruces fuera de gel+pouch
     o corridas parciales.

07 | Texto — Métodos de optimización
     Explica los tres métodos y las restricciones de fabricación.

08 | Código — Optimización y búsqueda de ventanas
     Combina las curvas de los slabs para obtener una dosis plana.
     Prueba ventanas de 0,5 a 3 mm en diferentes posiciones.
     Compara:
       MC Sara: mínimos cuadrados con la cota original.
       MC con cota física: mínimos cuadrados con ancho mínimo final.
       Programación lineal: minimiza la diferencia relativa entre
       dosis máxima y mínima (J de Mariel).
     También evalúa el redondeo de los anchos y muestra la mejor
     ventana según J para cada extensión y método.
     ALLOW_PARTIAL=True permite usar corridas parciales; False
     exige que todos los slabs estén completos. Requiere t00 a t22.

09 | Texto — Comparación justa
     Explica por qué se comparan los métodos en ventanas idénticas.

10 | Código — Comparación de los tres métodos
     Grafica los filtros completos disponibles y compara los tres
     métodos en las ventanas 0,25–2,50; 1–3 y 0–3 mm.
     Muestra dosis media, CV, J, dosis mínima relativa y pesos,
     antes y después del redondeo. Los anchos quedan también en
     la tabla weights_comparison (ancho completo mm).

11 | Texto — Validez de la suma de slabs
     Explica por qué sumar curvas no equivale necesariamente a
     simular un filtro escalonado real.

12 | Código — Suma de slabs vs. filtro completo PHITS
     Usa los anchos nominales de los filtros existentes y compara
     sus curvas simuladas con la suma ponderada correspondiente.
     Permite detectar las limitaciones de la aproximación por áreas.

13 | Texto — Anillos y espectros
     Explica las regiones radiales y cómo interpretar la fluencia
     espectral a la entrada del pouch.

14 | Código — Anillos y energía
     Grafica la dosis en dos anillos del caso CASE (slab_t02 por
     defecto). Cambiar CASE para estudiar otro caso con ese tally.
     Compara los espectros de t00, t02, ref_N9 y N12 disponibles;
     calcula fluencia integrada y grafica su fracción acumulada.

15 | Texto — Pasos pendientes
     Resume los controles de geometría, materiales, alcance,
     fabricación y validación experimental antes de usar un filtro.

3. CÓMO INTERPRETAR LOS RESULTADOS
---------------------------------
FWHM: distancia entre los cruces al 50 % del máximo del pico.
Separación: distancia entre máximos de dos slabs consecutivos.
Separación/FWHM medio: indicador de solapamiento, sin umbral universal.
J local: variación relativa de la suma de un par entre sus máximos.
         No equivale al J de un SOBP completo.
CV: dispersión de la dosis respecto de su media. Menor es mejor.
J de Mariel: 100 × (1 - dosis mínima / dosis máxima).
             El criterio estudiado es J < 5 %.
Peso: fracción asignada a un espesor de material.
Ancho completo: peso × período del filtro.
Continuo: resultado matemático sin redondeo de fabricación.
Redondeado: resultado adaptado a la resolución provisional.

Una ventana de 3 mm no es necesariamente un SOBP de 3 mm al 90 %.
Las ventanas pueden incluir gel, cinta y pouch. Una dosis plana
longitudinal no demuestra homogeneidad tridimensional.

4. QUÉ MIRAR PRIMERO
--------------------
Si acabás de terminar slab_t02:
    Celda 04: comprobar el estado y los errores.
    Celda 06: comparar su pico, ancho y separación con los demás slabs.
    Celda 08: explorar qué ventanas permiten las curvas disponibles.
    Celda 10: comparar los tres optimizadores en la misma ventana.
    Celda 14: revisar los anillos y el espectro si están disponibles.

Las corridas parciales permiten explorar, no cerrar el diseño.
El PLA y la resolución de impresión son provisionales. No usar los
pesos para fabricar o irradiar sin validar el filtro completo.

Los scripts originales de Sara se conservan. Para generar y
comprobar la geometría se siguen usando gen_ridge.py, check_exact.py
y check_geom.py; el notebook no realiza esas tareas.
