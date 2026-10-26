from manim import *
import numpy as np

config.background_color = "#0B1323"
config.frame_width = 14.222222
config.frame_height = 8

FONDO = "#0B1323"
PANEL = "#142238"
BLANCO = "#EDF3FA"
GRIS = "#A5B6CC"
CIAN = "#44D9E6"
ORO = "#FFD080"
VERDE = "#68E0B0"
ROSA = "#FF829E"
SEMILLA = 27
PAUSA = 2.5


def texto(s, size=26, color=BLANCO, pos=None):
    t = Text(str(s), font="DejaVu Sans", font_size=size, color=color)
    if t.width > 12.6:
        t.scale_to_fit_width(12.6)
    if pos is not None:
        t.move_to(pos)
    return t


def tarjeta(w, h, pos):
    return RoundedRectangle(width=w, height=h, corner_radius=0.18,
                            stroke_color="#2B415D", stroke_width=1,
                            fill_color=PANEL, fill_opacity=1).move_to(pos)


def camino(puntos, color=ORO, opacity=1):
    r = VMobject().set_points_as_corners(puntos)
    r.set_stroke(color, width=2, opacity=opacity)
    return r


def historias(rng, n):
    resultado = []
    for _ in range(n):
        y = float(rng.normal(0, 0.10))
        puntos = [np.array([-5.4, y, 0.0]), np.array([-2.8, y, 0.0])]
        x, angulo, energia = -2.8, 0.0, 1.0
        while x < 2.6 and energia > 0:
            paso = float(rng.exponential(0.52))
            dx = min(max(paso * np.cos(angulo), 0.04), 2.6 - x)
            y += dx * np.tan(angulo)
            x += dx
            puntos.append(np.array([x, y, 0.0]))
            energia -= dx * 0.105 + float(rng.uniform(0.01, 0.08))
            angulo = float(np.clip(angulo + rng.normal(0, 0.12), -0.65, 0.65))
            if abs(y) > 1.3:
                break
        llega = energia > 0 and x >= 2.6 and abs(y) < 1.3
        if llega:
            y += (4.5 - x) * np.tan(angulo)
            puntos.append(np.array([4.5, y, 0.0]))
        detectado = llega and abs(y) <= 1.5
        resultado.append((puntos, detectado))
    return resultado


class MonteCarloDivulgativo(Scene):
    def limpiar(self):
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.7)

    def cabecera(self, numero, titulo, subtitulo):
        self.play(FadeIn(texto(f"MONTE CARLO  /  {numero}", 16, CIAN, [0, 3.55, 0])),
                  FadeIn(texto(titulo, 37, BLANCO, [0, 2.95, 0])),
                  FadeIn(texto(subtitulo, 21, GRIS, [0, 2.35, 0])), run_time=0.8)

    def pie(self, s, color=GRIS):
        t = texto(s, 21, color, [0, -3.35, 0])
        self.play(FadeIn(t), run_time=0.5)
        return t

    def construct(self):
        rng = np.random.default_rng(SEMILLA)
        self.introduccion()
        self.sorteo(rng)
        self.transporte(rng)
        self.mapa(rng)
        self.convergencia()
        self.cierre()

    def introduccion(self):
        self.cabecera("01", "Una partícula. Muchos futuros posibles.",
                      "¿Cómo predecimos lo que hará un haz de protones?")
        origen = np.array([-5.2, 0, 0])
        fuente = Dot(origen, radius=0.12, color=ORO)
        bloque = tarjeta(4.3, 3.1, [0, 0, 0])
        self.play(FadeIn(bloque), FadeIn(fuente),
                  FadeIn(texto("MATERIAL", 19, CIAN, [0, 1.2, 0])))
        rutas = VGroup()
        for i, yy in enumerate([-1.0, -0.5, 0, 0.6, 1.05]):
            r = camino([origen, [-2.1, 0, 0], [0, yy * 0.35, 0],
                        [2.1, yy, 0], [5.0, yy * 1.4, 0]],
                       CIAN if i % 2 else ORO, 0.65)
            rutas.add(r)
        self.play(LaggedStart(*[Create(r) for r in rutas], lag_ratio=0.2), run_time=3)
        self.pie("No adivinamos cada futuro: muestreamos sus probabilidades.", VERDE)
        self.wait(PAUSA)
        self.limpiar()

    def sorteo(self, rng):
        self.cabecera("02", "Azar, pero con reglas físicas", 
                      "El modelo asigna probabilidades. El sorteo elige un resultado.")
        self.play(FadeIn(tarjeta(11.8, 3.6, [0, -0.1, 0])))
        self.play(FadeIn(texto("EJEMPLO DE MUESTREO", 17, CIAN, [0, 1.25, 0])),
                  FadeIn(texto("¿Qué tipo de interacción ocurre?", 27, BLANCO, [0, 0.7, 0])))
        colores = [CIAN, ORO, ROSA]
        limites = [0, 0.6, 0.9, 1]
        nombres = ["A · 60 %", "B · 30 %", "C · 10 %"]
        for i in range(3):
            a, b = limites[i:i + 2]
            rect = Rectangle(width=(b - a) * 10, height=0.42,
                             fill_color=colores[i], fill_opacity=0.85, stroke_width=0)
            rect.move_to([-5 + (a + b) * 5, -0.15, 0])
            self.play(FadeIn(rect), run_time=0.25)
            self.add(texto(nombres[i], 17, colores[i], [-5 + (a + b) * 5, -0.65, 0]))
        self.add(texto("0", 16, GRIS, [-5, 0.27, 0]),
                 texto("1", 16, GRIS, [5, 0.27, 0]))
        marcador = Triangle(color=BLANCO, fill_opacity=1).scale(0.12).rotate(PI)
        marcador.move_to([-5, 0.3, 0])
        valor = texto("Número aleatorio entre 0 y 1", 21, BLANCO, [0, -1.3, 0])
        self.play(FadeIn(marcador), FadeIn(valor))
        for u in [0.23, 0.78, 0.95, 0.41]:
            indice = min(np.searchsorted(limites[1:], u, side="right"), 2)
            nuevo = texto(f"u = {u:.2f}   →   resultado {['A', 'B', 'C'][indice]}",
                          23, colores[indice], [0, -1.3, 0])
            self.play(marcador.animate.move_to([-5 + 10 * u, 0.3, 0]),
                      Transform(valor, nuevo), run_time=0.8)
            self.wait(0.6)
        self.pie("Porcentajes ilustrativos: cambian con la energía y el material.")
        self.wait(PAUSA)
        self.limpiar()

    def transporte(self, rng):
        self.cabecera("03", "Seguimos una historia", 
                      "Posición, dirección y energía se actualizan a lo largo del recorrido.")
        material = Rectangle(width=5.4, height=2.6, stroke_color=CIAN,
                             stroke_width=1, fill_color=CIAN, fill_opacity=0.08)
        material.move_to([-0.1, 0, 0])
        detector = Rectangle(width=0.16, height=3, color=VERDE, fill_opacity=0.6).move_to([4.5, 0, 0])
        fuente = Dot([-5.4, 0, 0], radius=0.13, color=ORO)
        etiquetas = VGroup(texto("FUENTE", 17, ORO, [-5.4, 1.8, 0]),
                            texto("MATERIAL", 17, CIAN, [-0.1, 1.8, 0]),
                            texto("PLANO DE REGISTRO", 16, VERDE, [4.5, 1.8, 0]))
        self.play(FadeIn(material), FadeIn(detector), FadeIn(fuente), FadeIn(etiquetas))
        puntos = [np.array(p) for p in [[-5.4, 0, 0], [-2.8, 0, 0],
                  [-1.7, 0, 0], [-0.6, 0.25, 0], [0.7, 0.12, 0], [2.6, 0.6, 0], [4.5, 1.0, 0]]]
        proton = Dot(puntos[0], radius=0.075, color=ORO)
        self.add(proton)
        estado = texto("Estado inicial: un protón entra al material", 22, ORO, [0, -2.1, 0])
        self.play(FadeIn(estado))
        mensajes = ["Definimos su posición, dirección y energía",
                    "Muestreamos el recorrido hasta el siguiente evento",
                    "Una interacción puede cambiar su dirección",
                    "El protón transfiere energía al material",
                    "Actualizamos el estado y continuamos",
                    "Si cruza el plano, registramos su contribución"]
        for a, b, mensaje in zip(puntos[:-1], puntos[1:], mensajes):
            segmento = Line(a, b, color=ORO, stroke_width=2.5)
            self.play(Create(segmento), proton.animate.move_to(b),
                      Transform(estado, texto(mensaje, 22, ORO, [0, -2.1, 0])), run_time=1.0)
            self.wait(0.5)
        self.play(FadeOut(proton), FadeOut(estado))
        contador = texto("Historias: 0   |   Cruces: 0", 22, VERDE, [0, -2.1, 0])
        self.play(FadeIn(contador))
        total = 0
        for tanda in range(4):
            datos = historias(rng, 12)
            rutas = VGroup(*[camino(p, ORO if ok else ROSA, 0.38) for p, ok in datos])
            particulas = VGroup(*[Dot(p[0], radius=0.04, color=ORO) for p, _ in datos])
            self.add(particulas)
            self.play(*[MoveAlongPath(d, r) for d, r in zip(particulas, rutas)],
                      *[Create(r) for r in rutas], run_time=1.5, rate_func=linear)
            total += sum(ok for _, ok in datos)
            self.play(FadeOut(particulas), Transform(contador,
                      texto(f"Historias: {(tanda + 1) * 12}   |   Cruces: {total}",
                            22, VERDE, [0, -2.1, 0])), run_time=0.3)
        self.pie("Esquema didáctico: las trayectorias no son una simulación de PHITS.")
        self.wait(PAUSA)
        self.limpiar()

    def mapa(self, rng):
        self.cabecera("04", "De historias a un mapa", 
                      "Dividimos el plano en celdas y acumulamos cruces.")
        filas, columnas = 8, 12
        yy, xx = np.mgrid[:filas, :columnas]
        p = np.exp(-0.5 * (((xx - 5.5) / 2.5) ** 2 + ((yy - 3.5) / 1.8) ** 2))
        p /= p.sum()
        cuentas = np.zeros_like(p, dtype=int)
        paleta = [ManimColor(c) for c in ["#182A42", "#155E85", "#19A4B7", "#59DBC9", "#FFD080"]]
        def grilla(n):
            g = VGroup()
            for i in range(filas):
                for j in range(columnas):
                    v = cuentas[i, j] / max(n * p.max(), 1)
                    color = paleta[min(4, int(np.clip(v, 0, 0.999) * 5))]
                    g.add(Square(side_length=0.35, stroke_width=0,
                                 fill_color=color, fill_opacity=1).move_to(
                                     [-3.0 + (j - 5.5) * 0.39, 0.1 + (3.5 - i) * 0.39, 0]))
            return g
        mapa = grilla(0)
        ntexto = texto("Cruces muestreados: 0", 22, ORO, [2.9, 1.2, 0])
        self.play(FadeIn(mapa), FadeIn(ntexto))
        self.add(texto("Pocos cruces: mucho ruido", 21, GRIS, [2.9, 0.4, 0]),
                 texto("Muchos cruces: patrón más estable", 19, VERDE, [2.9, -0.2, 0]),
                 texto("Oscuro: menos   /   Claro: más", 16, GRIS, [-3, -1.85, 0]))
        anterior = 0
        for n in [50, 200, 800, 3200, 12800, 51200]:
            indices = rng.choice(p.size, size=n - anterior, p=p.ravel())
            cuentas += np.bincount(indices, minlength=p.size).reshape(p.shape)
            anterior = n
            self.play(Transform(mapa, grilla(n)), Transform(ntexto,
                      texto(f"Cruces muestreados: {n:,}".replace(',', '.'),
                            22, ORO, [2.9, 1.2, 0])), run_time=1.2)
            self.wait(0.5)
        self.pie("Mapa normalizado por muestra. Aquí muestreamos impactos de una distribución ilustrativa.")
        self.wait(PAUSA)
        self.limpiar()

    def convergencia(self):
        self.cabecera("05", "¿Cuánto mejora al repetir?", 
                      "Con historias independientes y varianza finita, la incertidumbre cae como 1 / √N.")
        izquierda, derecha, abajo, arriba = -4.8, 4.8, -1.6, 1.45
        self.play(Create(Line([izquierda, abajo, 0], [derecha, abajo, 0], color=GRIS)),
                  Create(Line([izquierda, abajo, 0], [izquierda, arriba, 0], color=GRIS)))
        self.add(texto("Incertidumbre estadística relativa", 17, GRIS, [-2.2, 1.8, 0]),
                 texto("Número de historias N (escala lineal)", 17, GRIS, [0, -2.15, 0]))
        def punto(n):
            return np.array([izquierda + (n - 100) / 9900 * (derecha - izquierda),
                             abajo + (100 / np.sqrt(n)) / 10 * (arriba - abajo), 0])
        curva = camino([punto(n) for n in np.linspace(100, 10000, 180)], CIAN)
        self.play(Create(curva), run_time=2)
        for n in [100, 400, 1600, 10000]:
            self.add(Dot(punto(n), radius=0.06, color=ORO))
            self.play(FadeIn(texto(str(n), 15, GRIS, [punto(n)[0], abajo - 0.25, 0])), run_time=0.25)
        mensaje = texto("4 veces más historias  →  aproximadamente la mitad de incertidumbre", 24, VERDE, [0, -2.85, 0])
        self.play(FadeIn(mensaje))
        self.pie("Tendencia teórica ilustrativa. En conteos Poisson: error relativo ≈ 1 / √conteos.")
        self.wait(PAUSA + 1)
        self.limpiar()

    def cierre(self):
        self.cabecera("06", "¿Qué obtenemos al final?", 
                      "Una estimación de lo que ocurre, junto con su incertidumbre estadística.")
        datos = [("FLUENCIA", "Recorrido de partículas por volumen", CIAN),
                 ("DOSIS", "Energía depositada por unidad de masa", ORO),
                 ("ESPECTRO", "Distribución de energías", VERDE)]
        for y, (titulo, detalle, color) in zip([1.0, -0.15, -1.3], datos):
            grupo = VGroup(tarjeta(11, 0.95, [0, y, 0]),
                            texto(titulo, 22, color, [-3.6, y, 0]),
                            texto(detalle, 22, BLANCO, [1.3, y, 0]))
            self.play(FadeIn(grupo, shift=UP * 0.12), run_time=0.6)
        self.play(FadeIn(texto("Más historias reducen el ruido estadístico.", 24, VERDE, [0, -2.35, 0])))
        self.pie("La precisión también depende de la geometría, los materiales y el modelo físico.")
        self.wait(PAUSA + 2)
