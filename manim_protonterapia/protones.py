
from manim import *
import numpy as np


class RidgeFilterReal(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        naranja = ManimColor("#F97316")
        amarillo = ManimColor("#FBBF24")
        azul = ManimColor("#38BDF8")
        violeta = ManimColor("#A78BFA")

        titulo = Text(
            "Ridge filter",
            font_size=34,
            weight=BOLD
        ).move_to(UP * 3.25)

        subtitulo = Text(
            "Modulación de la energía de los protones",
            font_size=19,
            color=GREY_B
        ).move_to(UP * 2.82)

        self.play(
            FadeIn(titulo),
            FadeIn(subtitulo),
            run_time=1
        )

        ancho_diente = 1.35
        altura_diente = 1.25
        centros = [-2.475, -0.825, 0.825, 2.475]
        y_base = 0.15

        base = Rectangle(
            width=7.7,
            height=0.16,
            stroke_width=0,
            fill_color="#C2410C",
            fill_opacity=1
        ).move_to([0, y_base - 0.08, 0])

        dientes = VGroup()

        for x in centros:
            diente = Polygon(
                [x - ancho_diente / 2, y_base, 0],
                [x, y_base + altura_diente, 0],
                [x + ancho_diente / 2, y_base, 0],
                stroke_color="#FDBA74",
                stroke_width=1.8,
                fill_color=naranja,
                fill_opacity=0.88
            )
            dientes.add(diente)

        self.play(FadeIn(base), run_time=0.5)

        self.play(
            LaggedStart(
                *[
                    GrowFromEdge(d, DOWN)
                    for d in dientes
                ],
                lag_ratio=0.13
            ),
            run_time=2
        )

        etiqueta_pla = Text(
            "PLA",
            font_size=17,
            color="#FDBA74"
        ).move_to([4.35, 0.75, 0])

        self.play(FadeIn(etiqueta_pla), run_time=0.4)

        tejido = RoundedRectangle(
            width=7.7,
            height=1.6,
            corner_radius=0.1,
            stroke_color=azul,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.38
        ).move_to([0, -1.88, 0])

        tejido_label = Text(
            "TEJIDO",
            font_size=17,
            color=BLUE_A
        ).move_to([4.45, -1.85, 0])

        self.play(
            FadeIn(tejido),
            FadeIn(tejido_label),
            run_time=0.8
        )

        leyenda_haz = Text(
            "Haz incidente",
            font_size=18,
            color=amarillo
        ).move_to([4.35, 2.02, 0])

        self.play(FadeIn(leyenda_haz), run_time=0.4)

        posiciones = []
        fracciones = []

        for centro in centros:
            for desplazamiento in [-0.46, 0.0]:
                posiciones.append(
                    centro + desplazamiento
                )
                fracciones.append(
                    1 - abs(desplazamiento)
                    / (ancho_diente / 2)
                )

        protones = VGroup()
        lineas = VGroup()

        for x in posiciones:
            protones.add(
                Dot(
                    point=[x, 2.12, 0],
                    radius=0.07,
                    color=amarillo
                )
            )

            lineas.add(
                DashedLine(
                    [x, 2.37, 0],
                    [x, 1.52, 0],
                    color=amarillo,
                    stroke_width=1.5,
                    dash_length=0.12
                ).set_opacity(0.4)
            )

        self.play(
            FadeIn(lineas),
            FadeIn(protones),
            run_time=0.8
        )

        self.play(
            *[
                p.animate.move_to([x, -0.12, 0])
                for p, x in zip(
                    protones, posiciones
                )
            ],
            run_time=3,
            rate_func=linear
        )

        colores_salida = [
            interpolate_color(
                azul,
                violeta,
                fraccion
            )
            for fraccion in fracciones
        ]

        self.play(
            *[
                p.animate.set_color(color)
                for p, color in zip(
                    protones, colores_salida
                )
            ],
            FadeOut(lineas),
            FadeOut(leyenda_haz),
            run_time=0.8
        )

        destinos = []

        for x, fraccion in zip(
            posiciones, fracciones
        ):
            alcance = (
                0.35 + 0.95 * (1 - fraccion)
            )

            destino_y = (
                tejido.get_top()[1] - alcance
            )

            destinos.append(
                np.array([x, destino_y, 0])
            )

        self.play(
            *[
                p.animate.move_to(destino)
                for p, destino in zip(
                    protones, destinos
                )
            ],
            run_time=2.5,
            rate_func=linear
        )

        marcas = VGroup()

        for destino, color in zip(
            destinos, colores_salida
        ):
            marca = Circle(
                radius=0.13,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.13
            ).move_to(destino)

            marcas.add(marca)

        self.play(
            *[
                FadeIn(marca, scale=0.6)
                for marca in marcas
            ],
            run_time=0.7
        )

        self.play(
            FadeOut(protones),
            run_time=0.5
        )

        cierre = Text(
            "Distintos espesores de PLA producen distintos alcances",
            font_size=19,
            color=BLUE_A
        ).move_to(DOWN * 3.3)

        self.play(
            Write(cierre),
            run_time=1.5
        )

        self.wait(2)
