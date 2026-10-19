import urllib.request
import os
from manim import *
import random

class PyramidMystery(MovingCameraScene):
    def construct(self):
        # 1. ATTACH AUDIO (If Piper successfully created it)
        if os.path.exists("voiceover.wav"):
            self.add_sound("voiceover.wav")

        # 2. CONSTANT MOTION (SANDSTORM)
        self.camera.background_color = "#140c04" 
        sand_particles = VGroup(*[
            Dot(radius=random.uniform(0.01, 0.04), color=random.choice([YELLOW_A, GOLD_E, ORANGE]), fill_opacity=random.uniform(0.3, 0.8)) 
            for _ in range(200)
        ])
        for s in sand_particles:
            s.move_to([random.uniform(-8, 8), random.uniform(-15, 15), 0])
            
        def update_sand(mob, dt):
            for s in mob:
                s.shift(LEFT * dt * random.uniform(1.5, 3.5) + DOWN * dt * random.uniform(0.2, 1.0))
                if s.get_x() < -6: s.set_x(6)
                if s.get_y() < -12: s.set_y(12)
                    
        sand_particles.add_updater(update_sand)
        self.add(sand_particles)
        
        # 3. DOWNLOAD REAL IMAGE
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg"
        image_path = "pyramid.jpg"
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
                out_file.write(response.read())
            real_pyramid = ImageMobject(image_path).scale(2.5)
        except:
            real_pyramid = Triangle(color=GOLD, fill_opacity=0.5).scale(3)
            
        real_pyramid.move_to(ORIGIN)

        # 4. SCENE 1: THE HOOK (Extended to 20 seconds)
        title1 = Text("HOW DID THEY", font="sans-serif", weight=BOLD, color=WHITE).scale(1.2).to_edge(UP, buff=2)
        title2 = Text("BUILD THIS?", font="sans-serif", weight=BOLD, color=GOLD).scale(1.5).next_to(title1, DOWN, buff=0.2)
        
        self.camera.frame.add_updater(lambda m, dt: m.scale(1 - 0.008 * dt)) # Slower zoom for longer runtime
        
        self.play(FadeIn(title1, shift=DOWN), run_time=2)
        self.play(FadeIn(title2, shift=UP), FadeIn(real_pyramid, scale=0.8), run_time=3)
        self.wait(15) # Extended wait for Voiceover
        
        # 5. SCENE 2: SLED & RAMP (Extended to 35 seconds)
        self.play(FadeOut(title1), FadeOut(title2), FadeOut(real_pyramid), run_time=2)
        self.camera.frame.clear_updaters()
        self.play(self.camera.frame.animate.scale(1.2).move_to(ORIGIN), run_time=1)
        
        blocks_text = Text("2.5 TON BLOCKS", font="sans-serif", color=WHITE, weight=BOLD).scale(1.2).to_edge(UP, buff=2)
        self.play(Write(blocks_text), run_time=2)
        
        ramp_line = Line(DOWN*2 + LEFT*3, UP*1 + RIGHT*2, color=ORANGE, stroke_width=8)
        sled = Rectangle(width=1.5, height=0.2, color=DARK_BROWN, fill_opacity=1)
        block = Square(side_length=1.2, color=LIGHT_GREY, fill_opacity=0.9).next_to(sled, UP, buff=0)
        sled_group = VGroup(sled, block).move_to(ramp_line.get_start()).rotate(ramp_line.get_angle())
        
        self.play(Create(ramp_line), run_time=2)
        self.play(FadeIn(sled_group, scale=0.8), run_time=2)
        
        self.play(
            MoveAlongPath(sled_group, ramp_line),
            self.camera.frame.animate.scale(0.8).move_to(ramp_line.get_center()),
            run_time=6, rate_func=linear
        )
        self.wait(20) # Extended wait for Voiceover
        
        # 6. SCENE 3: THE CAPSTONE OUTRO (Extended to 25 seconds)
        self.play(FadeOut(blocks_text), FadeOut(ramp_line), FadeOut(sled_group), run_time=2)
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.add_updater(lambda m, dt: m.scale(1 + 0.01 * dt).shift(UP * dt * 0.1))
        
        pyramid_base = Triangle(color=GOLD, fill_opacity=0.2).scale(3.5).move_to(DOWN*2)
        capstone = Triangle(color=YELLOW, fill_opacity=1).scale(0.4).move_to(pyramid_base.get_top() + DOWN*0.2)
        final_text = Text("PERFECTION.", font="sans-serif", weight=BOLD, color=WHITE).scale(1.5).next_to(pyramid_base, UP, buff=1)
        
        self.play(DrawBorderThenFill(pyramid_base), run_time=3)
        self.play(FadeIn(capstone, shift=DOWN*2), Write(final_text), run_time=3)
        self.wait(17) # Extended wait for Voiceover conclusion
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)
