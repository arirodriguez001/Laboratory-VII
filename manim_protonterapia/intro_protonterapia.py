from manim import *
import numpy as np
from PIL import Image, ImageFilter

_original_fromarray = Image.fromarray

def _compatible_fromarray(obj, mode=None):
    arr = np.asarray(obj)
    if mode == "RGBA" and arr.ndim == 2:
        arr = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    return _original_fromarray(arr, mode=mode)

Image.fromarray = _compatible_fromarray

config.background_color = "#030914"
config.frame_rate = 30


class IntroProtonterapia(Scene):
    def construct(self):
        self.rng = np.random.default_rng(20261029)
        self.W = config.frame_width
        self.H = config.frame_height
        self.cyan = "#78E7F8"
        self.gold = "#FFD38A"
        self.red = "#FF6478"
        self.fg = "#EEF7FF"
        self.subtitle_bg = Rectangle(width=self.W, height=1.28, fill_color="#02050D", fill_opacity=0.96, stroke_width=0).move_to([0, -self.H / 2 + 0.64, 0]).set_z_index(100)
        self.subtitle_line = Line([-self.W / 2, -self.H / 2 + 1.28, 0], [self.W / 2, -self.H / 2 + 1.28, 0], color="#32647C", stroke_width=1).set_z_index(101)
        self.sub = VGroup()
        self.add(self.subtitle_bg, self.subtitle_line)
        self.cosmos()
        self.acelerador()
        self.pregunta()
        self.terapia()
        self.bragg()
        self.argentina()
        self.tandar()

    def caption(self, text):
        if len(self.sub):
            self.remove(self.sub)
        words = text.split()
        lines = []
        line = ""
        for word in words:
            candidate = (line + " " + word).strip()
            if len(candidate) > 65 and line:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        if len(lines) > 2:
            mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
        self.sub = VGroup(*[Text(s, font="Arial", font_size=25, color=self.fg, weight=MEDIUM) for s in lines]).arrange(DOWN, buff=0.12)
        self.sub.scale_to_fit_width(min(self.sub.width, self.W - 0.9))
        self.sub.move_to([0, -self.H / 2 + 0.64, 0]).set_z_index(102)
        self.add(self.sub)
        return max(2.7, len(words) / 2.4 + 0.4)

    def heading(self, main, small=None):
        a = Text(main, font="Arial", font_size=29, weight=BOLD, color=WHITE).to_edge(UP, buff=0.28)
        if small:
            b = Text(small, font="Arial", font_size=16, color="#A9C4D7").next_to(a, DOWN, buff=0.14)
            return VGroup(a, b)
        return VGroup(a)

    def cloud(self, points, color, stroke=2):
        obj = PMobject(color=color, stroke_width=stroke)
        obj.add_points(np.asarray(points, dtype=float))
        return obj

    def cosmic_texture(self, w=1000, h=540):
        y, x = np.mgrid[0:h, 0:w]
        a = np.zeros((h, w, 3), dtype=float)
        a[:] = [3, 9, 20]
        centers = [(0.23, 0.46, 0.30, 0.15, [18, 77, 155]), (0.62, 0.42, 0.25, 0.24, [87, 28, 130]), (0.52, 0.65, 0.33, 0.13, [28, 92, 137]), (0.81, 0.26, 0.17, 0.14, [109, 42, 78])]
        for cx, cy, sx, sy, rgb in centers:
            field = np.exp(-0.5 * (((x / w - cx) / sx) ** 2 + ((y / h - cy) / sy) ** 2))
            noise = self.rng.uniform(0.55, 1.25, (h, w))
            a += field[..., None] * noise[..., None] * np.array(rgb)
        fine = self.rng.normal(0, 4.8, (h, w, 1))
        a = np.clip(a + fine, 0, 255).astype(np.uint8)
        image = Image.fromarray(a, "RGB").filter(ImageFilter.GaussianBlur(1.6))
        return ImageMobject(np.array(image)).stretch_to_fit_width(self.W).stretch_to_fit_height(self.H)

    def remove_scene(self, *objects):
        self.play(*[FadeOut(o) for o in objects], run_time=0.65)

    def cosmos(self):
        back = self.cosmic_texture()
        p = self.rng.uniform([-6.5, -2.9, 0], [6.5, 3.0, 0], (1050, 3))
        stars = self.cloud(p, "#D8EBFF", 1)
        dirs = self.rng.normal(size=(2300, 2))
        dirs /= np.linalg.norm(dirs, axis=1)[:, None]
        radius = self.rng.random(2300) ** 0.65
        final = np.column_stack((dirs[:, 0] * radius * 6.15, dirs[:, 1] * radius * 2.45 + 0.18, np.zeros(2300)))
        initial = final.copy()
        initial[:, :2] *= 0.015
        initial[:, 1] += 0.18
        explosion = self.cloud(initial, self.gold, 2)
        bright = VGroup(*[Circle(radius=r, stroke_color=self.gold, stroke_opacity=alpha, stroke_width=2).shift(UP * 0.18) for r, alpha in [(0.16, 0.7), (0.3, 0.4), (0.5, 0.18)]])
        label = self.heading("DEL UNIVERSO A LA MATERIA")
        duration = self.caption("Cuando pensamos en protones, quizás lo primero que se nos viene a la cabeza es el origen del universo,")
        self.play(FadeIn(back), FadeIn(stars), FadeIn(explosion), FadeIn(bright), FadeIn(label), run_time=1.15)
        val = ValueTracker(0)
        explosion.add_updater(lambda m: m.set_points(initial + (final - initial) * val.get_value()))
        self.play(val.animate.set_value(1), bright.animate.scale(5), run_time=duration - 1.15, rate_func=rush_from)
        explosion.clear_updaters()
        duration = self.caption("el Big Bang, la formación de estrellas o incluso los grandes aceleradores de partículas")
        sun = Circle(radius=0.75, stroke_width=0, fill_color="#FFB85D", fill_opacity=1).shift(LEFT * 1.3 + UP * 0.2)
        sun_glow = VGroup(*[Circle(radius=r, stroke_width=0, fill_color="#FF9F40", fill_opacity=op).move_to(sun) for r, op in [(1.0, 0.20), (1.27, 0.12), (1.58, 0.06)]])
        surface = self.cloud(np.column_stack((self.rng.normal(-1.3, 0.58, 900), self.rng.normal(0.2, 0.58, 900), np.zeros(900))), self.gold, 2)
        self.play(FadeOut(explosion), FadeOut(bright), FadeIn(sun_glow), FadeIn(sun), FadeIn(surface), run_time=1.5)
        self.play(Rotate(surface, angle=0.4), sun.animate.scale(1.08), run_time=duration - 1.5)
        self.remove_scene(surface, sun, sun_glow, stars, back, label)

    def acelerador(self):
        dur = self.caption("que buscan entender los misterios de la materia.")
        bg = Rectangle(width=self.W, height=self.H, fill_color="#081625", fill_opacity=1, stroke_width=0)
        ring_shadow = Ellipse(width=10.4, height=4.3, color="#0A1925", stroke_width=45).shift(UP * 0.12)
        ring_outer = Ellipse(width=10.4, height=4.3, color="#608DA4", stroke_width=10).shift(UP * 0.12)
        ring_inner = Ellipse(width=9.85, height=3.76, color="#1F4255", stroke_width=17).shift(UP * 0.12)
        beam_path = Ellipse(width=9.45, height=3.41, color=self.cyan, stroke_width=2.4).shift(UP * 0.12)
        pieces = VGroup()
        for theta in np.linspace(0, TAU, 24, endpoint=False):
            pos = [5.13 * np.cos(theta), 2.12 * np.sin(theta) + 0.12, 0]
            block = RoundedRectangle(width=0.75, height=0.35, corner_radius=0.06, stroke_color="#8BA7B6", stroke_width=1.5, fill_color="#28445B", fill_opacity=1).move_to(pos).rotate(theta)
            pieces.add(block)
        t = ValueTracker(0)
        theta = self.rng.uniform(0, TAU, 1200)
        spread = self.rng.normal(1, 0.01, 1200)
        points = np.column_stack((4.73 * spread * np.cos(theta), 1.71 * spread * np.sin(theta) + 0.12, np.zeros(1200)))
        moving = self.cloud(points, self.cyan, 2)
        moving.add_updater(lambda m: m.set_points(np.column_stack((4.73 * spread * np.cos(theta + t.get_value()), 1.71 * spread * np.sin(theta + t.get_value()) + 0.12, np.zeros(1200)))))
        label = self.heading("ACELERADOR DE PARTÍCULAS", "Visualización ilustrativa de un anillo acelerador")
        self.play(FadeIn(bg), FadeIn(ring_shadow), Create(ring_outer), Create(ring_inner), FadeIn(pieces), Create(beam_path), FadeIn(label), FadeIn(moving), run_time=1.4)
        self.play(t.animate.set_value(5 * TAU), run_time=max(dur - 1.4, 2.5), rate_func=linear)
        moving.clear_updaters()
        self.remove_scene(bg, ring_shadow, ring_outer, ring_inner, pieces, beam_path, label, moving)

    def pregunta(self):
        dur = self.caption("Pero ¿y si les dijéramos que estas mismas partículas también pueden utilizarse para combatir el cáncer?")
        background = self.cosmic_texture()
        title = Text("¿Y SI PUDIERAN", font="Arial", color=WHITE, weight=BOLD, font_size=42)
        title2 = Text("COMBATIR EL CÁNCER?", font="Arial", color=self.cyan, weight=BOLD, font_size=42)
        group = VGroup(title, title2).arrange(DOWN, buff=0.24).move_to(UP * 0.4)
        underline = Line(LEFT * 3.2, RIGHT * 3.2, color=self.cyan, stroke_width=3).next_to(group, DOWN, buff=0.38)
        self.play(FadeIn(background), FadeIn(group, shift=UP * 0.3), Create(underline), run_time=1.6)
        self.wait(max(0, dur - 1.6))
        self.remove_scene(group, underline, background)

    def terapia(self):
        a = self.caption("Aunque parezca sorprendente, los protones tienen una propiedad física muy particular:")
        back = Rectangle(width=self.W, height=self.H, fill_color="#08121D", fill_opacity=1, stroke_width=0)
        texture = np.asarray(self.cosmic_texture().pixel_array).copy()
        texture[:, :, 0] = (texture[:, :, 0] * 0.3).astype(np.uint8)
        tissue_img = ImageMobject(texture).stretch_to_fit_width(10.3).stretch_to_fit_height(3.6).shift(UP * 0.3)
        tissue_img.set_opacity(0.38)
        outline = RoundedRectangle(width=10.5, height=3.6, corner_radius=0.28, fill_opacity=0, stroke_color="#5B9AB9", stroke_width=2).shift(UP * 0.3)
        target = Ellipse(width=1.9, height=1.62, stroke_color="#FF8B9C", stroke_width=3, fill_color="#8D2437", fill_opacity=0.65).move_to([2.45, 0.3, 0])
        core = Ellipse(width=1.1, height=1.0, stroke_width=0, fill_color="#E44A63", fill_opacity=0.25).move_to(target)
        micro = self.cloud(np.column_stack((self.rng.normal(2.45, 0.42, 300), self.rng.normal(0.3, 0.33, 300), np.zeros(300))), "#FC9B9C", 1)
        heading = self.heading("PROTONES Y TEJIDO", "Representación conceptual del depósito de energía")
        proton_start = self.rng.uniform(-5.0, -4.65, 900)
        yp = self.rng.normal(0.3, 0.17, 900)
        proton = self.cloud(np.column_stack((proton_start, yp, np.zeros(900))), self.cyan, 2)
        self.play(FadeIn(back), FadeIn(tissue_img), Create(outline), FadeIn(target), FadeIn(core), FadeIn(micro), FadeIn(heading), FadeIn(proton), run_time=1.5)
        self.wait(max(0, a - 1.5))
        b = self.caption("podemos aprovechar la forma en que depositan su energía en los materiales para irradiar un tumor")
        progress = ValueTracker(0)
        xbegin, xend = -5.0, 2.4
        angle_noise = self.rng.normal(0, 0.19, 900)
        phase = self.rng.random(900) * 0.65
        proton.add_updater(lambda m: m.set_points(np.column_stack((np.minimum(xend, xbegin + (xend - xbegin) * np.minimum(1, np.maximum(0, progress.get_value() - phase))), yp + angle_noise * np.maximum(0, progress.get_value() - phase), np.zeros(900)))))
        xdep = np.concatenate((self.rng.uniform(-5.0, 1.55, 500), self.rng.normal(2.12, 0.32, 1550)))
        xdep = np.clip(xdep, -5.0, 2.55)
        ydep = self.rng.normal(0.3, 0.4, len(xdep))
        deposited = self.cloud(np.column_stack((xdep, ydep, np.zeros(len(xdep)))), self.gold, 2)
        deposited.set_opacity(0)
        self.add(deposited)
        self.play(progress.animate.set_value(1.8), deposited.animate.set_opacity(0.88), run_time=b, rate_func=linear)
        proton.clear_updaters()
        c = self.caption("y reducir el daño a los tejidos sanos que lo rodean.")
        self.play(Indicate(target, color=self.red, scale_factor=1.1), run_time=1.4)
        self.wait(max(0, c - 1.4))
        self.remove_scene(back, tissue_img, outline, target, core, micro, heading, proton, deposited)

    def bragg(self):
        duration = self.caption("Esta técnica se conoce como protonterapia.")
        title = Text("PROTONTERAPIA", font="Arial", font_size=55, color=WHITE, weight=BOLD).shift(UP * 2.15)
        axes = Axes(x_range=[0, 10, 2], y_range=[0, 1.25, 0.25], x_length=9.65, y_length=2.95, tips=False, axis_config={"color": "#90B2C7", "stroke_width": 2}).shift(DOWN * 0.22)
        f = lambda x: (0.14 + 0.1 * x / 10 + 0.82 * np.exp(-0.5 * ((x - 7.55) / 0.39) ** 2)) if x < 8.55 else 0.012
        curve = axes.plot(f, x_range=[0, 9.9, 0.025], color=self.gold, stroke_width=5, use_smoothing=False)
        glow = axes.plot(f, x_range=[0, 9.9, 0.025], color="#E88E39", stroke_width=13, stroke_opacity=0.23, use_smoothing=False)
        xt = Text("Profundidad", font="Arial", font_size=18, color="#C0D3DF").next_to(axes, DOWN, buff=0.12)
        yt = Text("Dosis", font="Arial", font_size=18, color="#C0D3DF").next_to(axes, LEFT, buff=0.08)
        peak = Dot(axes.c2p(7.55, f(7.55)), radius=0.09, color=self.red)
        text_peak = Text("Pico de Bragg", font="Arial", font_size=22, color=self.red).next_to(peak, UR, buff=0.16)
        self.play(FadeIn(title), Create(axes), FadeIn(xt), FadeIn(yt), run_time=0.8)
        self.play(Create(glow), Create(curve), run_time=max(2.0, duration - 1.6))
        self.play(FadeIn(peak), FadeIn(text_peak), run_time=0.8)
        self.remove_scene(title, axes, xt, yt, curve, glow, peak, text_peak)

    def argentina(self):
        d1 = self.caption("Y Argentina también está dando pasos importantes en este campo.")
        backdrop = self.cosmic_texture()
        location = Text("ARGENTINA", font="Arial", font_size=30, weight=BOLD, color=self.cyan).shift(UP * 1.75)
        name = Text("CeArP", font="Arial", font_size=87, weight=BOLD, color=WHITE).shift(UP * 0.55)
        expansion = Text("CENTRO ARGENTINO DE PROTONTERAPIA", font="Arial", font_size=24, color="#CCDDEA").next_to(name, DOWN, buff=0.22)
        strip = Line(LEFT * 3.8, RIGHT * 3.8, color=self.cyan, stroke_width=2.8).next_to(expansion, DOWN, buff=0.32)
        self.play(FadeIn(backdrop), FadeIn(location), FadeIn(name, shift=UP * 0.18), FadeIn(expansion), Create(strip), run_time=1.6)
        self.wait(max(0, d1 - 1.6))
        d2 = self.caption("Con la construcción del Centro Argentino de Protonterapia (CeArP), el primero de su tipo en Latinoamérica,")
        self.wait(d2)
        d3 = self.caption("se abre una nueva etapa para el tratamiento del cáncer en nuestro país.")
        self.wait(d3)
        self.remove_scene(backdrop, location, name, expansion, strip)

    def tandar(self):
        d1 = self.caption("En paralelo, distintos grupos de investigación están trabajando para estudiar los efectos de los protones")
        title = self.heading("INVESTIGACIÓN EN ARGENTINA", "Acelerador TANDAR · Comisión Nacional de Energía Atómica")
        source = RoundedRectangle(width=3.0, height=0.7, corner_radius=0.1, fill_color="#25495C", fill_opacity=1, stroke_color=self.cyan, stroke_width=2).move_to([0, 2.03, 0])
        source_text = Text("Haz vertical de protones", font="Arial", font_size=18, color=WHITE).move_to(source)
        modules = VGroup(*[RoundedRectangle(width=1.3, height=0.15, corner_radius=0.03, fill_color="#6F8D98", fill_opacity=1, stroke_color="#AEC7D2", stroke_width=1).move_to([0, y, 0]) for y in [1.25, 0.4, -0.45]])
        target = RoundedRectangle(width=3.4, height=0.38, corner_radius=0.06, fill_color="#B94358", fill_opacity=0.5, stroke_color=self.red, stroke_width=2).move_to([0, -1.15, 0])
        target_text = Text("Modelo experimental", font="Arial", font_size=20, color=WHITE).next_to(target, DOWN, buff=0.18)
        beam = self.cloud(np.column_stack((self.rng.normal(0, 0.46, 1600), self.rng.uniform(-1.08, 1.75, 1600), np.zeros(1600))), self.cyan, 2)
        self.play(FadeIn(title), FadeIn(source), FadeIn(source_text), FadeIn(modules), FadeIn(target), FadeIn(target_text), FadeIn(beam), run_time=1.7)
        self.wait(max(0, d1 - 1.7))
        d2 = self.caption("y desarrollar nuevas estrategias de irradiación.")
        self.play(Indicate(target, color=self.red, scale_factor=1.04), run_time=1.2)
        self.wait(max(0, d2 - 1.2))
        d3 = self.caption("Y es justamente en una de estas investigaciones donde comienza nuestro trabajo.")
        name = Text("NUESTRO TRABAJO", font="Arial", font_size=38, weight=BOLD, color=WHITE).move_to([3.75, 0, 0])
        self.play(FadeIn(name, shift=UP * 0.15), run_time=0.9)
        self.wait(max(0, d3 - 0.9))
        self.remove_scene(title, source, source_text, modules, target, target_text, beam, name)
