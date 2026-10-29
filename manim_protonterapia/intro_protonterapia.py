from manim import *
import numpy as np

config.background_color = "#07101E"
config.frame_rate = 30


class IntroProtonterapia(Scene):
    def construct(self):
        rng = np.random.default_rng(2026)
        W, H = config.frame_width, config.frame_height
        azul = "#55CCFF"
        cyan = "#7AE7EF"
        dorado = "#FFD07A"
        rojo = "#FF6378"
        gris = "#AAB9CD"
        self.camera.background_color = "#07101E"

        banda = Rectangle(width=W, height=1.40, fill_color="#020711", fill_opacity=0.94, stroke_width=0)
        banda.move_to([0, -H / 2 + 0.70, 0])
        linea = Line([-W / 2, -H / 2 + 1.40, 0], [W / 2, -H / 2 + 1.40, 0], color="#365776", stroke_width=1)
        subt = VGroup()
        inicio_subtitulo = None
        duracion_subtitulo = 0.0
        VELOCIDAD_NARRACION = 2.55
        self.add(banda, linea)
        self.bring_to_front(banda, linea)

        def subtitulo(texto):
            nonlocal subt, inicio_subtitulo, duracion_subtitulo
            if inicio_subtitulo is not None:
                transcurrido = self.time - inicio_subtitulo
                if transcurrido < duracion_subtitulo:
                    self.wait(duracion_subtitulo - transcurrido)
            if len(subt):
                self.remove(subt)
            palabras = texto.split()
            renglones = []
            actual = ""
            for palabra in palabras:
                candidato = (actual + " " + palabra).strip()
                if len(candidato) > 73 and actual:
                    renglones.append(actual)
                    actual = palabra
                else:
                    actual = candidato
            if actual:
                renglones.append(actual)
            if len(renglones) > 2:
                renglones = [" ".join(renglones[:2]), " ".join(renglones[2:])]
            subt = VGroup(*[
                Text(s, font="Arial", font_size=24, color=WHITE, weight=MEDIUM)
                for s in renglones
            ]).arrange(DOWN, buff=0.12)
            if subt.width > W - 1.0:
                subt.scale_to_fit_width(W - 1.0)
            subt.move_to([0, -H / 2 + 0.70, 0])
            self.add(subt)
            self.bring_to_front(banda, linea, subt)
            inicio_subtitulo = self.time
            duracion_subtitulo = max(2.6, len(palabras) / VELOCIDAD_NARRACION + 0.5)

        def rotulo(titulo, descripcion=""):
            a = Text(titulo, font="Arial", font_size=31, weight=BOLD, color=WHITE)
            a.to_edge(UP, buff=0.40)
            if descripcion:
                b = Text(descripcion, font="Arial", font_size=17, color=gris)
                b.next_to(a, DOWN, buff=0.12)
                return VGroup(a, b)
            return VGroup(a)

        def nube(n, ancho=12.5, alto=4.4, color=azul, radio=0.018):
            puntos = np.column_stack((
                rng.uniform(-ancho / 2, ancho / 2, n),
                rng.uniform(-alto / 2, alto / 2, n) + 0.32,
                np.zeros(n)
            ))
            return nube_puntos(points=puntos, color=color, radius=radio), puntos

        def nube_puntos(points, color, radius):
            return PMobject(stroke_width=max(1, int(radius * 150)), color=color).add_points(points)

        def actualizar_puntos(obj, puntos):
            obj.points = np.asarray(puntos)
            return obj

        # 1. Universo y expansion: visualizacion conceptual, no modelo cosmologico.
        subtitulo("Cuando pensamos en protones, quizás lo primero que se nos viene a la cabeza es el origen del universo,")
        n = 1800
        direcciones = rng.normal(size=(n, 2))
        direcciones /= np.linalg.norm(direcciones, axis=1)[:, None]
        radios = rng.random(n) ** 0.65
        destino = np.column_stack((direcciones[:, 0] * radios * 6.5, direcciones[:, 1] * radios * 2.6 + 0.25, np.zeros(n)))
        origen = destino.copy()
        origen[:, :2] *= 0.015
        origen[:, 1] += 0.25
        expansion = nube_puntos(points=origen, color=dorado, radius=0.015)
        etiqueta = rotulo("DEL UNIVERSO A LA MATERIA")
        self.play(FadeIn(etiqueta), FadeIn(expansion), run_time=0.65)
        t = ValueTracker(0)
        expansion.add_updater(lambda m: actualizar_puntos(m, origen + (destino - origen) * t.get_value()))
        self.play(t.animate.set_value(1), run_time=4.2, rate_func=rush_from)
        expansion.clear_updaters()
        self.wait(0.4)

        subtitulo("el Big Bang, la formación de estrellas o incluso los grandes aceleradores de partículas")
        self.play(FadeOut(expansion), run_time=0.45)
        fondo, _ = nube(1050, color="#5380B4", radio=0.008)
        estrella = Circle(radius=0.85, stroke_color=dorado, stroke_width=3, fill_color="#F7A83F", fill_opacity=0.27).shift(UP * 0.25)
        halo = Circle(radius=1.26, stroke_color=dorado, stroke_width=2, stroke_opacity=0.28).shift(UP * 0.25)
        self.play(FadeIn(fondo), Create(halo), FadeIn(estrella), run_time=1.8)
        self.play(estrella.animate.scale(1.07), halo.animate.scale(1.09), run_time=1.3)
        self.play(FadeOut(Group(fondo, estrella, halo, etiqueta)), run_time=0.55)

        # 2. Acelerador: anillo esquematico de alta densidad de particulas.
        subtitulo("que buscan entender los misterios de la materia.")
        titulo_acc = rotulo("ACELERADORES DE PARTÍCULAS", "Representación esquemática")
        anillo = Ellipse(width=8.8, height=3.6, color="#3E718E", stroke_width=7).shift(UP * 0.30)
        guia = Ellipse(width=8.1, height=2.9, color="#78B9D4", stroke_width=1.4).shift(UP * 0.30)
        bloques = VGroup()
        for ang in np.linspace(0, TAU, 16, endpoint=False):
            x, y = 4.37 * np.cos(ang), 1.78 * np.sin(ang) + 0.30
            bloques.add(RoundedRectangle(corner_radius=0.08, width=0.42, height=0.24, fill_color="#346078", fill_opacity=1, stroke_width=0).move_to([x, y, 0]).rotate(ang))
        angs = rng.uniform(0, TAU, 850)
        r = rng.normal(1, 0.025, 850)
        puntos = np.column_stack((4.0 * r * np.cos(angs), 1.43 * r * np.sin(angs) + 0.30, np.zeros(850)))
        haz_circular = nube_puntos(points=puntos, color=cyan, radius=0.012)
        giro = ValueTracker(0)
        haz_circular.add_updater(lambda m: actualizar_puntos(m, np.column_stack((
            4.0 * r * np.cos(angs + giro.get_value()),
            1.43 * r * np.sin(angs + giro.get_value()) + 0.30,
            np.zeros(850)
        ))))
        self.play(FadeIn(titulo_acc), Create(anillo), Create(guia), FadeIn(bloques), FadeIn(haz_circular), run_time=1.1)
        self.play(giro.animate.set_value(3 * TAU), run_time=3.5, rate_func=linear)
        haz_circular.clear_updaters()
        self.play(FadeOut(Group(titulo_acc, anillo, guia, bloques, haz_circular)), run_time=0.6)

        # 3. Giro narrativo a radioterapia.
        subtitulo("Pero ¿y si les dijéramos que estas mismas partículas también pueden utilizarse para combatir el cáncer?")
        pregunta = Text("¿Y SI PUDIERAN COMBATIR EL CÁNCER?", font="Arial", font_size=36, weight=BOLD, color=WHITE).shift(UP * 0.6)
        bajo = Text("De la física fundamental a la medicina", font="Arial", font_size=22, color=cyan).next_to(pregunta, DOWN, buff=0.3)
        self.play(Write(pregunta), FadeIn(bajo, shift=UP * 0.1), run_time=2.2)
        self.wait(1.0)
        self.play(FadeOut(Group(pregunta, bajo)), run_time=0.5)

        # 4. Tejido, tumor y deposicion con maximo cerca del fin de alcance.
        subtitulo("Aunque parezca sorprendente, los protones tienen una propiedad física muy particular:")
        titulo_tejido = rotulo("ENERGÍA DEPOSITADA EN EL TEJIDO", "Modelo conceptual de un haz de protones")
        tejido = RoundedRectangle(width=10.6, height=2.55, corner_radius=0.16, stroke_color="#5D98BB", stroke_width=2, fill_color="#1C455B", fill_opacity=0.49).shift(UP * 0.58)
        tumor = Ellipse(width=1.65, height=1.45, stroke_color=rojo, stroke_width=3, fill_color=rojo, fill_opacity=0.22).move_to([2.20, 0.58, 0])
        etiqueta_tumor = Text("TUMOR", font="Arial", font_size=18, weight=BOLD, color="#FF91A0").move_to(tumor)
        zona = Text("Tejido sano", font="Arial", font_size=18, color="#9FD5EA").move_to([-2.7, 1.46, 0])
        entrada = Arrow(start=[-6.2, 0.58, 0], end=[-5.28, 0.58, 0], color=cyan, buff=0, stroke_width=5)
        self.play(FadeIn(titulo_tejido), FadeIn(tejido), FadeIn(tumor), FadeIn(etiqueta_tumor), FadeIn(zona), GrowArrow(entrada), run_time=1.1)
        x0, x1 = -5.25, 2.30
        dens = 1700
        xx = rng.uniform(x0, x1, dens)
        yy = rng.normal(0.58, 0.27, dens)
        # El muestreo destaca la zona de mayor deposicion cerca del tumor.
        p = 0.20 + 2.5 * np.exp(-0.5 * ((xx - 2.05) / 0.48) ** 2)
        mascara = rng.random(dens) < p / 2.7
        energia_pts = np.column_stack((xx[mascara], yy[mascara], np.zeros(mascara.sum())))
        depositos = nube_puntos(points=energia_pts, color=dorado, radius=0.021)
        delante = nube_puntos(points=np.column_stack((rng.uniform(-5.5, -5.15, 420), rng.normal(0.58, 0.14, 420), np.zeros(420))), color=cyan, radius=0.012)
        self.play(FadeIn(delante), run_time=0.35)
        subtitulo("podemos aprovechar la forma en que depositan su energía en los materiales para irradiar un tumor")
        trayectoria = ValueTracker(x0)
        base = rng.uniform(x0, x1, 1150)
        offsets = rng.normal(0, 0.18, 1150)
        moviles = nube_puntos(points=np.column_stack((base, offsets + 0.58, np.zeros(len(base)))), color=cyan, radius=0.010)
        moviles.add_updater(lambda m: actualizar_puntos(m, np.column_stack((
            np.minimum(x1, x0 + np.mod(base - x0 + (trayectoria.get_value() - x0) * 2.3, x1 - x0)),
            offsets + 0.58,
            np.zeros(len(base))
        ))))
        self.play(FadeIn(moviles), trayectoria.animate.set_value(x1), FadeIn(depositos), run_time=4.0, rate_func=linear)
        moviles.clear_updaters()
        subtitulo("y reducir el daño a los tejidos sanos que lo rodean.")
        self.play(Indicate(tumor, color=rojo, scale_factor=1.05), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(Group(titulo_tejido, tejido, tumor, etiqueta_tumor, zona, entrada, delante, depositos, moviles)), run_time=0.5)

        # 5. Pico de Bragg: curva cualitativa, no calculo dosimetrico.
        subtitulo("Esta técnica se conoce como protonterapia.")
        gran_titulo = Text("PROTONTERAPIA", font="Arial", font_size=55, weight=BOLD, color=WHITE).shift(UP * 1.65)
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 1.25, 0.25], x_length=9.3, y_length=2.65, tips=False, axis_config={"color": "#88A9BE", "stroke_width": 2}).shift(DOWN * 0.25)
        funcion = lambda x: 0.14 + 0.11 * (x / 10) + 0.80 * np.exp(-0.5 * ((x - 7.7) / 0.39) ** 2) if x <= 8.55 else 0.012
        curva = axes.plot(funcion, x_range=[0, 9.6, 0.025], color=dorado, stroke_width=5, use_smoothing=False)
        eje_x = Text("Profundidad", font="Arial", font_size=18, color=gris).next_to(axes, DOWN, buff=0.15)
        eje_y = Text("Dosis", font="Arial", font_size=18, color=gris).next_to(axes, LEFT, buff=0.10)
        pico = Dot(axes.c2p(7.7, funcion(7.7)), radius=0.08, color=rojo)
        anotacion = Text("Pico de Bragg", font="Arial", font_size=22, color=rojo).next_to(pico, UR, buff=0.15)
        pie = Text("Curva ilustrativa: no representa un cálculo de dosis clínico", font="Arial", font_size=14, color=gris).next_to(eje_x, DOWN, buff=0.12)
        self.play(FadeIn(gran_titulo, shift=UP * 0.2), Create(axes), FadeIn(eje_x), FadeIn(eje_y), run_time=0.9)
        self.play(Create(curva), run_time=2.5)
        self.play(FadeIn(pico), FadeIn(anotacion), FadeIn(pie), run_time=0.5)
        self.wait(0.65)
        self.play(FadeOut(Group(gran_titulo, axes, eje_x, eje_y, curva, pico, anotacion, pie)), run_time=0.6)

        # 6. Argentina y CeArP: grafica editorial, sin mapa geografico inventado.
        subtitulo("Y Argentina también está dando pasos importantes en este campo.")
        superior = Text("ARGENTINA", font="Arial", font_size=27, weight=BOLD, color=cyan).shift(UP * 1.55)
        cearp = Text("CeArP", font="Arial", font_size=74, weight=BOLD, color=WHITE).shift(UP * 0.45)
        subt_cearp = Text("Centro Argentino de Protonterapia", font="Arial", font_size=25, color=gris).next_to(cearp, DOWN, buff=0.28)
        linea_acento = Line(LEFT * 2.4, RIGHT * 2.4, stroke_width=3, color=cyan).next_to(subt_cearp, DOWN, buff=0.28)
        self.play(FadeIn(superior), FadeIn(cearp, shift=UP * 0.1), FadeIn(subt_cearp), Create(linea_acento), run_time=1.8)
        subtitulo("Con la construcción del Centro Argentino de Protonterapia (CeArP), el primero de su tipo en Latinoamérica,")
        self.wait(2.35)
        subtitulo("se abre una nueva etapa para el tratamiento del cáncer en nuestro país.")
        self.wait(1.65)
        self.play(FadeOut(Group(superior, cearp, subt_cearp, linea_acento)), run_time=0.5)

        # 7. Investigacion: del acelerador al blanco biologico.
        subtitulo("En paralelo, distintos grupos de investigación están trabajando para estudiar los efectos de los protones")
        titulo_tandar = rotulo("INVESTIGACIÓN EN ARGENTINA", "Acelerador TANDAR · CNEA")
        fuente = RoundedRectangle(width=2.7, height=0.8, corner_radius=0.12, stroke_color=cyan, stroke_width=2, fill_color="#123748", fill_opacity=1).move_to([0, 2.05, 0])
        fuente_txt = Text("Haz de protones", font="Arial", font_size=19, color=WHITE).move_to(fuente)
        muestra = RoundedRectangle(width=2.45, height=0.45, corner_radius=0.08, stroke_color=rojo, stroke_width=2, fill_color=rojo, fill_opacity=0.22).move_to([0, -1.27, 0])
        muestra_txt = Text("Modelo biológico", font="Arial", font_size=18, color=WHITE).next_to(muestra, DOWN, buff=0.15)
        haz = VGroup(*[Line([x, 1.6, 0], [x + rng.normal(0, 0.035), -1.05, 0], stroke_width=1.2, color=cyan, stroke_opacity=0.28) for x in np.linspace(-0.62, 0.62, 75)])
        puntos_irr = nube_puntos(points=np.column_stack((rng.normal(0, 0.49, 1000), rng.uniform(-0.85, 1.4, 1000), np.zeros(1000))), color=cyan, radius=0.009)
        self.play(FadeIn(titulo_tandar), FadeIn(fuente), FadeIn(fuente_txt), FadeIn(muestra), FadeIn(muestra_txt), Create(haz), FadeIn(puntos_irr), run_time=2.0)
        self.wait(1.3)
        subtitulo("y desarrollar nuevas estrategias de irradiación.")
        self.play(Indicate(muestra, color=rojo), run_time=0.9)
        self.wait(0.4)
        subtitulo("Y es justamente en una de estas investigaciones donde comienza nuestro trabajo.")
        titulo_final = Text("NUESTRO TRABAJO", font="Arial", font_size=40, weight=BOLD, color=WHITE).move_to([3.85, 0.05, 0])
        self.play(FadeIn(titulo_final, shift=UP * 0.1), run_time=0.55)
        self.wait(2.3)
        self.play(FadeOut(Group(titulo_tandar, fuente, fuente_txt, muestra, muestra_txt, haz, puntos_irr, titulo_final)), run_time=0.7)
        self.wait(0.2)
        if inicio_subtitulo is not None:
            restante = duracion_subtitulo - (self.time - inicio_subtitulo)
            if restante > 0:
                self.wait(restante)
