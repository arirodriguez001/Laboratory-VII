
from manim import *
import numpy as np

class PicoBragg(Scene):
    def construct(self):
        self.camera.background_color = "#0B1020"

        titulo = Text(
            "¿Cómo funciona la protonterapia?",
            font_size=34,
            color=WHITE
        ).move_to(UP * 3.4)

        subtitulo = Text(
            "Los protones depositan energía al atravesar la materia",
            font_size=19,
            color=GREY_B
        ).move_to(UP * 2.85)

        self.play(FadeIn(titulo), run_time=1)
        self.play(FadeIn(subtitulo), run_time=0.8)

        tejido = RoundedRectangle(
            width=8,
            height=1.2,
            corner_radius=0.1,
            stroke_color=BLUE_B,
            stroke_width=2,
            fill_color=BLUE_E,
            fill_opacity=0.35
        ).move_to(UP * 1.55)

        etiqueta = Text(
            "TEJIDO",
            font_size=17,
            color=BLUE_A
        ).next_to(tejido, DOWN, buff=0.14)

        self.play(
            FadeIn(tejido),
            FadeIn(etiqueta),
            run_time=1
        )

        ejes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.2, 0.4],
            x_length=8.4,
            y_length=1.75,
            tips=False,
            axis_config={
                "color": GREY_B,
                "include_numbers": False
            }
        ).move_to(DOWN * 1.75)

        eje_x = Text(
            "Profundidad",
            font_size=18,
            color=WHITE
        ).next_to(ejes, DOWN, buff=0.15)

        eje_y = Text(
            "Dosis relativa",
            font_size=17,
            color=WHITE
        ).rotate(PI / 2).next_to(ejes, LEFT, buff=0.15)

        self.play(
            Create(ejes),
            FadeIn(eje_x),
            FadeIn(eje_y),
            run_time=1.2
        )

        def dosis(x):
            entrada = 0.18 + 0.015 * x
            pico = 0.75 * np.exp(
                -0.5 * ((x - 7.1) / 0.45) ** 2
            )
            caida = 1 / (
                1 + np.exp(13 * (x - 7.75))
            )
            return (entrada + pico) * caida

        profundidad = ValueTracker(0.02)

        curva = always_redraw(
            lambda: ejes.plot(
                dosis,
                x_range=[
                    0,
                    max(0.02, profundidad.get_value()),
                    0.025
                ],
                color=YELLOW,
                stroke_width=4
            )
        )

        def posicion_proton():
            x = -4.0 + profundidad.get_value() * 0.84
            return np.array([x, 1.55, 0])

        proton = always_redraw(
            lambda: Dot(
                point=posicion_proton(),
                radius=0.085,
                color=YELLOW
            )
        )

        halo = always_redraw(
            lambda: Circle(
                radius=0.1 + 0.23 * dosis(
                    profundidad.get_value()
                ),
                stroke_width=0,
                fill_color=YELLOW,
                fill_opacity=0.13
            ).move_to(posicion_proton())
        )

        punto_curva = always_redraw(
            lambda: Dot(
                ejes.c2p(
                    profundidad.get_value(),
                    dosis(profundidad.get_value())
                ),
                radius=0.055,
                color=WHITE
            )
        )

        self.add(curva, halo, proton, punto_curva)

        self.play(
            profundidad.animate.set_value(5.5),
            run_time=4,
            rate_func=linear
        )

        self.play(
            profundidad.animate.set_value(7.1),
            run_time=3,
            rate_func=linear
        )

        pico = ejes.c2p(7.1, dosis(7.1))

        marca = Dot(
            pico,
            color=RED,
            radius=0.085
        )

        texto_pico = Text(
            "Pico de Bragg",
            font_size=21,
            color=YELLOW
        ).next_to(marca, UP, buff=0.24)

        self.play(
            FadeIn(marca),
            FadeIn(texto_pico),
            run_time=0.8
        )

        self.play(
            profundidad.animate.set_value(8.2),
            run_time=2,
            rate_func=linear
        )

        self.play(
            FadeOut(halo),
            FadeOut(proton),
            FadeOut(punto_curva),
            run_time=0.7
        )

        conclusion = Text(
            "La dosis máxima se alcanza cerca del final del recorrido",
            font_size=19,
            color=BLUE_A
        ).move_to(UP * 0.35)

        self.play(
            FadeOut(etiqueta),
            FadeIn(conclusion),
            run_time=1
        )

        self.wait(2)
