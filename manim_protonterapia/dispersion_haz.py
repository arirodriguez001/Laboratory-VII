from manim import *
import numpy as np

class DispersionHaz(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        amarillo = YELLOW
        naranja = ManimColor("#F97316")
        azul = ManimColor("#38BDF8")
        cian = TEAL_A
        violeta = ManimColor("#A78BFA")
        gris = GREY_B

        titulo = Text(
            "Dispersión del haz de protones",
            font_size=32,
            weight=BOLD,
            color=WHITE
        ).move_to(UP * 3.25)

        subtitulo = Text(
            "Esquema conceptual del montaje experimental",
            font_size=17,
            color=GREY_B
        ).move_to(UP * 2.82)

        self.play(FadeIn(titulo), FadeIn(subtitulo), run_time=1)

        eje = DashedLine(
            start=[0, 2.75, 0],
            end=[0, -2.6, 0],
            color=GREY_D,
            dash_length=0.12,
            stroke_width=1.2
        ).set_opacity(0.35)

        self.play(FadeIn(eje), run_time=0.4)

        dispersor1 = Rectangle(
            width=4.2,
            height=0.16,
            fill_color=GREY_C,
            fill_opacity=1,
            stroke_width=0
        ).move_to([0, 1.85, 0])

        ridge_base = Rectangle(
            width=4.2,
            height=0.16,
            fill_color="#C2410C",
            fill_opacity=1,
            stroke_width=0
        ).move_to([0, 0.85, 0])

        dientes = VGroup()
        dientes_x = [-1.5, -0.75, 0, 0.75, 1.5]
        for x in dientes_x:
            d = Polygon(
                [x - 0.33, 0.93, 0],
                [x, 1.28, 0],
                [x + 0.33, 0.93, 0],
                stroke_color="#FDBA74",
                stroke_width=1.2,
                fill_color=naranja,
                fill_opacity=0.9
            )
            dientes.add(d)

        dispersor2 = Rectangle(
            width=4.2,
            height=0.16,
            fill_color=GREY_C,
            fill_opacity=1,
            stroke_width=0
        ).move_to([0, -0.2, 0])

        oclusor = Circle(
            radius=0.23,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=1
        ).move_to([0, -0.2, 0])

        pouch = RoundedRectangle(
            width=6.3,
            height=0.95,
            corner_radius=0.08,
            stroke_color=azul,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.28
        ).move_to([0, -2.0, 0])

        etiqueta1 = Text(
            "1er dispersor",
            font_size=16,
            color=gris
        ).move_to([3.5, 1.85, 0])

        etiqueta2 = Text(
            "Ridge filter",
            font_size=16,
            color="#FDBA74"
        ).move_to([3.4, 1.07, 0])

        etiqueta3 = Text(
            "2° dispersor / oclusor",
            font_size=16,
            color=gris
        ).move_to([4.0, -0.2, 0])

        etiqueta4 = Text(
            "Plano del pouch",
            font_size=16,
            color=BLUE_A
        ).move_to([3.6, -2.0, 0])

        self.play(FadeIn(dispersor1), FadeIn(etiqueta1), run_time=0.45)
        self.play(FadeIn(ridge_base), FadeIn(dientes), FadeIn(etiqueta2), run_time=0.75)
        self.play(FadeIn(dispersor2), FadeIn(oclusor), FadeIn(etiqueta3), run_time=0.55)
        self.play(FadeIn(pouch), FadeIn(etiqueta4), run_time=0.55)

        texto_haz = Text(
            "Haz inicial angosto",
            font_size=17,
            color=amarillo
        ).move_to([3.35, 2.45, 0])

        self.play(FadeIn(texto_haz), run_time=0.4)

        n = 32

        x0 = np.linspace(-0.16, 0.16, n)

        protones = VGroup(*[
            Dot([x, 2.55, 0], radius=0.035, color=amarillo)
            for x in x0
        ])

        trails = VGroup(*[
            TracedPath(
                p.get_center,
                stroke_color=amarillo,
                stroke_width=1.6,
                dissipating_time=0.7
            )
            for p in protones
        ])

        self.add(*trails)
        self.play(FadeIn(protones), run_time=0.5)

        self.play(
            *[
                p.animate.move_to([x, 2.05, 0])
                for p, x in zip(protones, x0)
            ],
            run_time=1.0,
            rate_func=linear
        )

        texto1 = Text(
            "El primer dispersor abre el haz",
            font_size=17,
            color=WHITE
        ).move_to([0, 2.45, 0])

        self.play(FadeOut(texto_haz), FadeIn(texto1), run_time=0.4)

        spread1 = np.linspace(-0.75, 0.75, n)
        wav1 = 0.05 * np.sin(np.linspace(0, 3 * PI, n))
        x1 = spread1 + wav1

        self.play(
            *[
                p.animate.move_to([x, 1.45, 0])
                for p, x in zip(protones, x1)
            ],
            run_time=1.4,
            rate_func=linear
        )

        texto2 = Text(
            "El ridge filter modula la energía del haz",
            font_size=17,
            color=WHITE
        ).move_to([0, 2.45, 0])

        self.play(FadeOut(texto1), FadeIn(texto2), run_time=0.4)

        spread2 = np.linspace(-0.95, 0.95, n)
        wav2 = 0.08 * np.sin(np.linspace(0, 4 * PI, n))
        x2 = spread2 + wav2

        colores_ridge = []
        for i in range(n):
            xi = x2[i]
            if abs(xi) < 0.22:
                colores_ridge.append(violeta)
            elif abs(xi) < 0.55:
                colores_ridge.append(amarillo)
            else:
                colores_ridge.append(cian)

        self.play(
            *[
                p.animate.move_to([x, 0.45, 0]).set_color(c)
                for p, x, c in zip(protones, x2, colores_ridge)
            ],
            run_time=1.6,
            rate_func=linear
        )

        texto3 = Text(
            "El segundo dispersor ensancha el campo",
            font_size=17,
            color=WHITE
        ).move_to([0, 2.45, 0])

        self.play(FadeOut(texto2), FadeIn(texto3), run_time=0.4)

        spread3 = np.linspace(-1.65, 1.65, n)
        wav3 = 0.10 * np.sin(np.linspace(0, 5 * PI, n))
        x3 = spread3 + wav3

        bloquear = list(range(14, 18))

        anims_stage3 = []
        for i, (p, x) in enumerate(zip(protones, x3)):
            if i in bloquear:
                anims_stage3.append(
                    p.animate.move_to([0, -0.2, 0]).set_opacity(0)
                )
            else:
                anims_stage3.append(
                    p.animate.move_to([x, -0.65, 0])
                )

        self.play(
            *anims_stage3,
            run_time=1.8,
            rate_func=linear
        )

        self.play(
            Flash(
                oclusor.get_center(),
                color=RED,
                flash_radius=0.34,
                num_lines=10
            ),
            run_time=0.6
        )

        texto4 = Text(
            "En el pouch se obtiene una cobertura más uniforme",
            font_size=17,
            color=WHITE
        ).move_to([0, 2.45, 0])

        self.play(FadeOut(texto3), FadeIn(texto4), run_time=0.4)

        survivors_idx = [i for i in range(n) if i not in bloquear]
        survivors = [protones[i] for i in survivors_idx]
        survivors_colors = [colores_ridge[i] for i in survivors_idx]

        x4 = np.linspace(-2.6, 2.6, len(survivors))
        x4 = x4 + 0.04 * np.sin(np.linspace(0, 3 * PI, len(survivors)))

        self.play(
            *[
                p.animate.move_to([x, -2.0, 0])
                for p, x in zip(survivors, x4)
            ],
            run_time=1.8,
            rate_func=linear
        )

        impactos = VGroup()
        for p in survivors:
            impacto = Circle(
                radius=0.07,
                stroke_color=p.get_color(),
                stroke_width=1.6,
                fill_color=p.get_color(),
                fill_opacity=0.10
            ).move_to(p.get_center())
            impactos.add(impacto)

        campo_uniforme = RoundedRectangle(
            width=5.55,
            height=0.42,
            corner_radius=0.05,
            stroke_width=0,
            fill_color=TEAL_A,
            fill_opacity=0.28
        ).move_to([0, -2.0, 0])

        etiqueta_uniforme = Text(
            "Cobertura más homogénea",
            font_size=16,
            color=TEAL_A
        ).move_to([0, -2.55, 0])

        self.play(
            *[FadeIn(i, scale=0.5) for i in impactos],
            FadeIn(campo_uniforme),
            FadeIn(etiqueta_uniforme),
            run_time=0.9
        )

        self.play(
            FadeOut(protones),
            run_time=0.5
        )

        cierre = Text(
            "La dispersión transversal ayuda a cubrir uniformemente el área de irradiación",
            font_size=18,
            color=BLUE_A
        ).move_to(DOWN * 3.25)

        self.play(
            FadeOut(texto4),
            Write(cierre),
            run_time=1.3
        )

        self.wait(2)