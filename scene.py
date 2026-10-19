import urllib.request
from manim import *
import random

class EasySpaceMystery(MovingCameraScene):
    def construct(self):
        # 1. SETUP & BACKGROUND
        self.camera.background_color = "#020305"
        
        # Download real image of Earth from Wikipedia
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/1024px-The_Earth_seen_from_Apollo_17.jpg"
        image_path = "earth.jpg"
        try:
            urllib.request.urlretrieve(image_url, image_path)
            earth = ImageMobject(image_path).scale(1.5)
        except:
            # Fallback if download fails
            earth = Circle(radius=2, color=BLUE, fill_opacity=1)
            
        earth.move_to(ORIGIN)
        
        # Particles (Starfield)
        stars = VGroup(*[
            Dot(
                point=[random.uniform(-7, 7), random.uniform(-14, 14), 0],
                radius=random.uniform(0.01, 0.04),
                color=random.choice([WHITE, LIGHT_GREY, BLUE_C]),
                fill_opacity=random.uniform(0.2, 0.8)
            ) for _ in range(150)
        ])
        self.add(stars)
        self.wait(2)
        
        # 2. THE HOOK (Text Animations)
        title_top = Text("WHAT HAPPENS IF", font="sans-serif", color=WHITE, weight=BOLD).scale(0.9).to_edge(UP, buff=2)
        title_bot = Text("WE SQUEEZE THE EARTH?", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.9).next_to(title_top, DOWN, buff=0.2)
        
        self.play(FadeIn(title_top, shift=DOWN), run_time=1.5)
        self.play(FadeIn(title_bot, shift=UP), run_time=1.5)
        self.wait(2.5)
        
        # 3. SHOW THE REAL EARTH
        self.play(FadeIn(earth, scale=0.5), run_time=2)
        
        earth_label = Text("Mass: 6 BILLION TRILLION TONS", font="sans-serif", color=LIGHT_GREY).scale(0.5).next_to(earth, DOWN, buff=0.8)
        self.play(Write(earth_label), run_time=2)
        self.wait(3.5)
        
        # 4. THE COMPRESSION METAPHOR
        self.play(FadeOut(title_top), FadeOut(title_bot), FadeOut(earth_label), run_time=1)
        
        metaphor_text = Text("If we compress all that mass...", font="sans-serif", color=WHITE).scale(0.7).to_edge(UP, buff=2.5)
        self.play(Write(metaphor_text), run_time=2)
        self.wait(2.5)
        
        # Visual: Shrinking the Earth into a tiny dot while camera zooms in
        marble = Dot(color=YELLOW, radius=0.08)
        
        self.play(
            Transform(earth, marble),
            self.camera.frame.animate.scale(0.3).move_to(ORIGIN),
            run_time=4.5,
            rate_func=rate_functions.ease_in_out_cubic
        )
        self.wait(2)
        
        # Because camera is zoomed in (scale 0.3), we must scale text way down!
        marble_label = Text("Down to the size of a MARBLE", font="sans-serif", color=RED, weight=BOLD).scale(0.18).next_to(earth, UP, buff=0.1)
        self.play(FadeIn(marble_label, shift=UP*0.05), run_time=2)
        self.wait(3.5)
        
        # 5. THE MIND-BENDING REVEAL
        reveal_text1 = Text("Gravity becomes infinite.", font="sans-serif", color=WHITE).scale(0.12).next_to(marble_label, UP, buff=0.2)
        reveal_text2 = Text("IT BECOMES A BLACK HOLE.", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.16).next_to(reveal_text1, UP, buff=0.08)
        
        self.play(Write(reveal_text1), run_time=2)
        self.play(FadeIn(reveal_text2, scale=1.5), run_time=2)
        self.wait(2)
        
        # Transform the yellow marble into a glowing black hole
        black_hole = Circle(radius=0.08, color=BLACK, fill_opacity=1)
        ring = Ellipse(width=0.4, height=0.1, color=ORANGE, stroke_width=2).move_to(black_hole)
        ring.rotate(PI/8)
        
        self.play(
            Transform(earth, black_hole),
            FadeIn(ring),
            run_time=2
        )
        ring.add_updater(lambda m, dt: m.rotate(dt * 2)) # Spinning accretion disk
        self.wait(4)
        
        # 6. OUTRO
        self.play(
            FadeOut(earth), FadeOut(ring), FadeOut(marble_label), 
            FadeOut(reveal_text1), FadeOut(reveal_text2), FadeOut(metaphor_text),
            run_time=2
        )
        self.wait(1)
        
        outro_text = Text("What else is hiding in space?", font="sans-serif", color=LIGHT_GREY, weight=BOLD).scale(0.15)
        self.play(Write(outro_text), run_time=2)
        self.wait(4)
