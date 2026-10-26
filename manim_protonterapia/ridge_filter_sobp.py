from manim import *
import numpy as np


class RidgeFilterSOBP(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"
        naranja = ManimColor("#F97316")
        celeste = ManimColor("#38BDF8")
        amarillo = ManimColor("#FBBF24")
        turquesa = ManimColor("#2DD4BF")
        gris = ManimColor("#AAB8CC")

        titulo = Text("Del ridge filter al SOBP", font_size=34, weight=BOLD)
        titulo.to_edge(UP, buff=0.35)
        self.play(FadeIn(titulo, shift=UP * 0.15), run_time=0.8)

        subtitulo = Text("Cada espesor de PLA modifica el alcance", font_size=19, color=gris)
        subtitulo.next_to(titulo, DOWN, buff=0.18)
        self.play(FadeIn(subtitulo), run_time=0.5)

        ancho = 1.32
        altura = 1.26
        base_y = 0.0
        centros = [-2.55, -0.85, 0.85, 2.55]
        base = Rectangle(width=7.5, height=0.15, fill_color="#C2410C", fill_opacity=1, stroke_width=0)
        base.move_to([0, base_y - 0.075, 0])
        dientes = VGroup()
        for x in centros:
            dientes.add(Polygon(
                [x - ancho / 2, base_y, 0],
                [x, base_y + altura, 0],
                [x + ancho / 2, base_y, 0],
                stroke_color="#FDBA74", stroke_width=1.7,
                fill_color=naranja, fill_opacity=0.9
            ))
        pla = Text("PLA", font_size=17, color=naranja).move_to([4.35, 0.55, 0])
        self.play(FadeIn(base), LaggedStart(*[GrowFromEdge(d, DOWN) for d in dientes], lag_ratio=0.12), run_time=1.9)
        self.play(FadeIn(pla), run_time=0.35)

        tejido = RoundedRectangle(
            width=7.5, height=1.28, corner_radius=0.1,
            stroke_color=celeste, stroke_width=2,
            fill_color="#12354B", fill_opacity=0.65
        ).move_to([0, -1.85, 0])
        etiqueta_tejido = Text("TEJIDO", font_size=16, color=celeste).move_to([4.35, -1.85, 0])
        self.play(FadeIn(tejido), FadeIn(etiqueta_tejido), run_time=0.65)

        desplazamientos = [-0.50, -0.26, 0.0, 0.26, 0.50]
        posiciones = [(c + d, 1.0 - abs(d) / (ancho / 2)) for c in centros for d in desplazamientos]
        grupos = VGroup()
        marcas = VGroup()
        techo = tejido.get_top()[1]
        for x, fraccion in posiciones:
            proton = Dot([x, 1.93, 0], radius=0.046, color=amarillo)
            grupos.add(proton)
        self.play(FadeIn(grupos), run_time=0.4)
        self.play(
            *[p.animate.move_to([x, -0.19, 0]) for p, (x, f) in zip(grupos, posiciones)],
            run_time=2.9, rate_func=linear
        )
        for p, (x, fraccion) in zip(grupos, posiciones):
            color = celeste if fraccion < 0.45 else turquesa if fraccion < 0.78 else ManimColor("#A78BFA")
            profundidad = 0.18 + 0.85 * (1 - fraccion)
            destino = np.array([x, techo - profundidad, 0])
            marcas.add(Dot(destino, radius=0.045, color=color))
        self.play(
            *[p.animate.move_to(m.get_center()).set_color(m.get_color()) for p, m in zip(grupos, marcas)],
            run_time=2.5, rate_func=linear
        )
        self.play(FadeOut(grupos), FadeIn(marcas), run_time=0.7)
        conclusion_1 = Text("Mayor espesor de PLA  =  menor alcance", font_size=20, color=celeste)
        conclusion_1.move_to([0, -3.12, 0])
        self.play(FadeIn(conclusion_1), run_time=0.8)
        self.wait(0.8)

        self.play(
            FadeOut(subtitulo), FadeOut(base), FadeOut(dientes), FadeOut(pla),
            FadeOut(tejido), FadeOut(etiqueta_tejido), FadeOut(marcas), FadeOut(conclusion_1),
            run_time=1.0
        )

        descripcion = Text("Superposición de picos de Bragg individuales", font_size=20, color=gris)
        descripcion.move_to([0, 2.48, 0])
        self.play(FadeIn(descripcion), run_time=0.6)

        ejes = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.25, 0.25],
            x_length=9.0, y_length=3.65, tips=False,
            axis_config={"color": GREY_B, "include_numbers": False},
        ).move_to([0.15, -0.62, 0])
        eje_x = Text("Profundidad normalizada", font_size=18).next_to(ejes, DOWN, buff=0.16)
        eje_y = Text("Dosis relativa", font_size=18).rotate(PI / 2).next_to(ejes, LEFT, buff=0.18)
        self.play(Create(ejes), FadeIn(eje_x), FadeIn(eje_y), run_time=1.0)

        centros_picos = np.linspace(4.05, 7.8, 22)
        sigma = 0.28
        def pico(x, centro):
            return np.exp(-0.5 * ((x - centro) / sigma) ** 2)
        def total_sin_normalizar(x):
            return sum(pico(x, c) for c in centros_picos)
        xs = np.linspace(0, 10, 1800)
        factor = max(total_sin_normalizar(x) for x in xs)
        def componente(x, c):
            return 1.03 * pico(x, c) / factor
        def suma(x):
            return 1.03 * total_sin_normalizar(x) / factor

        curvas = VGroup()
        for centro in centros_picos:
            curvas.add(ejes.plot(
                lambda x, c=centro: componente(x, c),
                x_range=[0, 10, 0.035], color=gris, stroke_width=1.2
            ).set_stroke(opacity=0.52))
        self.play(
            LaggedStart(*[Create(c) for c in curvas], lag_ratio=0.055),
            run_time=4.6
        )
        leyenda_individual = VGroup(
            Line(ORIGIN, RIGHT * 0.42, color=gris, stroke_width=2),
            Text("Picos individuales", font_size=16, color=gris)
        ).arrange(RIGHT, buff=0.15).move_to([2.95, 1.99, 0])
        self.play(FadeIn(leyenda_individual), run_time=0.4)

        total = ejes.plot(suma, x_range=[0, 10, 0.018], color=turquesa, stroke_width=5)
        self.play(
            *[c.animate.set_stroke(opacity=0.28) for c in curvas],
            Create(total), run_time=3.3
        )
        etiqueta_sobp = Text("SOBP", font_size=24, weight=BOLD, color=turquesa)
        etiqueta_sobp.move_to(ejes.c2p(6.0, 1.16))
        self.play(FadeIn(etiqueta_sobp), run_time=0.7)
        cierre = Text("La suma extiende la región de dosis elevada", font_size=19, color=celeste)
        cierre.move_to([0, -3.35, 0])
        self.play(FadeIn(cierre), run_time=0.8)
        self.wait(2)
