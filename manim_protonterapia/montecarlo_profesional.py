from manim import *
import numpy as np

config.background_color = "#0B1323"
config.frame_width = 14.222222
config.frame_height = 8

CIAN = "#44D9E6"
ORO = "#FFD080"
BLANCO = "#EDF3FA"
GRIS = "#A5B6CC"
VERDE = "#68E0B0"


def txt(s, size, pos, color=BLANCO):
    t = Text(s, font="DejaVu Sans", font_size=size, color=color)
    if t.width > 12.5:
        t.scale_to_fit_width(12.5)
    return t.move_to(pos)


class MonteCarlo20s(Scene):
    def construct(self):
        rng = np.random.default_rng(27)
        titulo = txt("MONTE CARLO", 42, [0, 3.1, 0])
        subtitulo = txt("Simular muchas historias para predecir un resultado", 23, [0, 2.45, 0], GRIS)
        material = RoundedRectangle(width=5.2, height=2.7, corner_radius=0.12,
                                    stroke_color=CIAN, stroke_width=1.3,
                                    fill_color=CIAN, fill_opacity=0.08).move_to([-0.2, 0, 0])
        fuente = Dot([-5.2, 0, 0], radius=0.1, color=ORO)
        detector = Rectangle(width=0.12, height=3.1, stroke_width=0,
                             fill_color=VERDE, fill_opacity=0.8).move_to([4.6, 0, 0])
        etiquetas = VGroup(txt("HAZ", 17, [-5.2, 1.9, 0], ORO),
                            txt("MATERIAL", 17, [-0.2, 1.9, 0], CIAN),
                            txt("REGISTRO", 17, [4.6, 1.9, 0], VERDE))
        frase = txt("1. Sorteamos interacciones según probabilidades físicas", 25, [0, -2.4, 0])
        nota = txt("Ilustración conceptual · no representa resultados de PHITS", 14, [0, -3.45, 0], GRIS)
        self.play(FadeIn(titulo), FadeIn(subtitulo), FadeIn(material), FadeIn(fuente),
                  FadeIn(detector), FadeIn(etiquetas), FadeIn(frase), FadeIn(nota), run_time=1)
        puntos = [np.array(p) for p in [[-5.2, 0, 0], [-2.8, 0, 0],
                  [-1.5, 0, 0], [-0.2, 0.22, 0], [1.1, 0.08, 0], [2.4, 0.4, 0], [4.6, 0.7, 0]]]
        proton = Dot(puntos[0], radius=0.075, color=ORO)
        self.add(proton)
        trazas = VGroup()
        for a, b in zip(puntos[:-1], puntos[1:]):
            segmento = Line(a, b, color=ORO, stroke_width=2.5)
            trazas.add(segmento)
            self.play(Create(segmento), proton.animate.move_to(b), run_time=0.5, rate_func=linear)
        self.play(FadeOut(proton), Transform(frase, txt("2. Repetimos con muchas partículas independientes", 25, [0, -2.4, 0])), run_time=1)
        for tanda in range(3):
            rutas, particulas = VGroup(), VGroup()
            for k in range(16):
                ys = [rng.normal(0, 0.055)]
                for j in range(4):
                    ys.append(ys[-1] + rng.normal(0, 0.18))
                fin = ys[-1] + (ys[-1] - ys[-2]) * 1.7
                puntos = [[-5.2, ys[0], 0], [-2.8, ys[0], 0],
                          [-1.5, ys[1], 0], [-0.2, ys[2], 0], [1.1, ys[3], 0],
                          [2.4, ys[4], 0], [4.6, fin, 0]]
                ruta = VMobject().set_points_as_corners(puntos)
                ruta.set_stroke(CIAN if k % 4 == 0 else ORO, width=1.5, opacity=0.38)
                rutas.add(ruta)
                particulas.add(Dot(puntos[0], radius=0.035, color=ORO))
            self.add(particulas)
            self.play(*[Create(r) for r in rutas],
                      *[MoveAlongPath(d, r) for d, r in zip(particulas, rutas)],
                      run_time=1.5, rate_func=linear)
            self.remove(particulas)
            trazas.add(*rutas)
        self.play(FadeOut(VGroup(material, fuente, detector, etiquetas, trazas)),
                  Transform(frase, txt("3. Acumulamos sus contribuciones en un mapa", 25, [0, -2.4, 0])), run_time=0.5)
        filas, cols = 8, 14
        yy, xx = np.mgrid[:filas, :cols]
        p = np.exp(-0.5 * (((xx - 6.5) / 2.8) ** 2 + ((yy - 3.5) / 1.7) ** 2))
        p /= p.sum()
        cuentas = np.zeros_like(p, dtype=int)
        colores = [ManimColor(c) for c in ["#172942", "#155E85", "#19A4B7", "#59DBC9", "#FFD080"]]
        def mapa(n):
            grupo = VGroup()
            for i in range(filas):
                for j in range(cols):
                    v = np.clip(cuentas[i, j] / max(n * p.max(), 1), 0, 0.999)
                    grupo.add(Square(side_length=0.32, stroke_width=0,
                                     fill_color=colores[int(v * 5)], fill_opacity=1).move_to(
                                         [-2.8 + (j - 6.5) * 0.36, (3.5 - i) * 0.36, 0]))
            return grupo
        grilla = mapa(0)
        leyenda = txt("Distribución espacial", 20, [-2.8, 1.85, 0], CIAN)
        idea = VGroup(txt("Más historias", 32, [3.1, 0.7, 0], BLANCO),
                      txt("↓", 36, [3.1, 0, 0], CIAN),
                      txt("Menos ruido estadístico", 23, [3.1, -0.7, 0], VERDE))
        contador = txt("0 muestras", 18, [-2.8, -1.85, 0], GRIS)
        self.play(FadeIn(grilla), FadeIn(leyenda), FadeIn(idea), FadeIn(contador), run_time=0.5)
        anterior = 0
        for n in [80, 400, 2000, 10000, 50000]:
            cuentas += rng.multinomial(n - anterior, p.ravel()).reshape(p.shape)
            anterior = n
            self.play(Transform(grilla, mapa(n)), Transform(contador,
                      txt(f"{n:,} muestras".replace(',', '.'), 18, [-2.8, -1.85, 0], GRIS)), run_time=1)
        self.play(Transform(frase, txt("Así estimamos magnitudes como la fluencia o la dosis", 25, [0, -2.4, 0])), run_time=0.5)
        self.wait(3)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=1)
