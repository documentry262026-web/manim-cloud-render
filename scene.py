import urllib.request
import os
from manim import *
import random

class PyramidDocumentary(MovingCameraScene):
    def construct(self):
        # --- 1. SYNC WITH DYNAMIC AUDIO DURATION ---
        if os.path.exists("voiceover.wav"):
            self.add_sound("voiceover.wav")
            
        try:
            with open("duration.txt", "r") as f:
                total_duration = float(f.read())
        except:
            total_duration = 300.0 # 5 min fallback
            
        # We have 5 main visual phases. We give each phase equal time.
        # We subtract 10 seconds for transitions/animations to be safe.
        phase_time = (total_duration / 5.0) - 2.0 

        # --- 2. THE "NEVER STILL" CINEMATIC UPDATERS ---
        self.camera.background_color = "#050505"
        
        # A. Infinite Global Grid
        grid = NumberPlane(x_range=[-50, 50, 1], y_range=[-50, 50, 1],
                           background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.15})
        self.add(grid)
        
        # B. Radar Scanner (Sweeps across the screen constantly)
        radar_line = Line(UP*20, DOWN*20, color=GREEN, stroke_width=2, stroke_opacity=0.3)
        radar_line.set_x(-15)
        def update_radar(m, dt):
            m.shift(RIGHT * dt * 4)
            if m.get_x() > 15: m.set_x(-15)
        radar_line.add_updater(update_radar)
        self.add(radar_line)

        # C. Infinite Cinematic Sandstorm
        sand_particles = VGroup(*[
            Dot(radius=random.uniform(0.01, 0.05), color=random.choice([YELLOW_A, GOLD_E, ORANGE]), fill_opacity=random.uniform(0.2, 0.5)) 
            for _ in range(350)
        ])
        for s in sand_particles:
            s.move_to([random.uniform(-20, 20), random.uniform(-15, 15), 0])
            
        def update_sand(mob, dt):
            cam_center = self.camera.frame.get_center()
            for s in mob:
                s.shift(LEFT * dt * random.uniform(2, 5) + DOWN * dt * random.uniform(0.5, 2.0))
                if s.get_x() < cam_center[0] - 15: s.set_x(cam_center[0] + 15)
                if s.get_y() < cam_center[1] - 10: s.set_y(cam_center[1] + 10)
        sand_particles.add_updater(update_sand)
        self.add(sand_particles)

        # --- CHAPTER 1: THE HOOK (ORIGIN) ---
        # Download real image
        image_path = "pyramid.jpg"
        req = urllib.request.Request("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg", headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file: out_file.write(response.read())
            img = ImageMobject(image_path).scale(3)
        except:
            img = Triangle(color=GOLD, fill_opacity=0.5).scale(4)
            
        title = Text("THE PYRAMID ENIGMA", font="sans-serif", weight=BOLD, color=WHITE).scale(1.5).to_edge(UP)
        
        self.play(FadeIn(img, scale=0.8), Write(title), run_time=2)
        
        # Camera slowly drifts across the image to keep motion
        self.camera.frame.add_updater(lambda m, dt: m.scale(1 - 0.002 * dt).shift(RIGHT * dt * 0.1))
        self.wait(phase_time) # Waits exactly as long as the audio needs!

        # --- CHAPTER 2: THE IMPOSSIBLE SCALE (RIGHT 20) ---
        station_2 = RIGHT * 20
        self.camera.frame.clear_updaters()
        self.play(self.camera.frame.animate.move_to(station_2).scale(1.2), run_time=3)
        
        c1_title = Text("CHAPTER 1: THE SCALE", font="sans-serif", color=YELLOW, weight=BOLD).move_to(station_2 + UP*3.5)
        self.play(FadeIn(c1_title, shift=DOWN), run_time=1)
        
        # Holographic Blueprint Block
        block = Square(side_length=3, color=BLUE, stroke_width=6).move_to(station_2)
        grid_block = VGroup(*[Line(block.get_corner(UL) + DOWN*i*0.5, block.get_corner(UR) + DOWN*i*0.5, color=BLUE, stroke_opacity=0.3) for i in range(1, 6)])
        weight_txt = Text("2,300,000 BLOCKS", font="sans-serif", color=RED).scale(1.2).move_to(station_2)
        
        self.play(Create(block), Create(grid_block), run_time=2)
        self.play(Write(weight_txt), run_time=1)
        
        # Rotating geometric rings around the block to keep it dynamic
        ring1 = Ellipse(width=5, height=1.5, color=TEAL).move_to(station_2)
        ring2 = Ellipse(width=1.5, height=5, color=GREEN).move_to(station_2)
        ring1.add_updater(lambda m, dt: m.rotate(dt * 1))
        ring2.add_updater(lambda m, dt: m.rotate(-dt * 1.5))
        self.add(ring1, ring2)
        
        self.camera.frame.add_updater(lambda m, dt: m.scale(1 + 0.002 * dt))
        self.wait(phase_time - 4)

        # --- CHAPTER 3: ORION ALIGNMENT (UP 15) ---
        station_3 = station_2 + UP * 15
        self.camera.frame.clear_updaters()
        self.play(self.camera.frame.animate.move_to(station_3), run_time=3)
        
        c2_title = Text("CHAPTER 2: COSMIC ALIGNMENT", font="sans-serif", color=BLUE_B, weight=BOLD).move_to(station_3 + UP*3.5)
        self.play(FadeIn(c2_title), run_time=1)
        
        # Draw 3 Pyramids
        p1 = Triangle(color=GOLD, stroke_width=5).scale(1.5).move_to(station_3 + LEFT*3 + DOWN*1)
        p2 = Triangle(color=GOLD, stroke_width=5).scale(1.2).move_to(station_3 + DOWN*1)
        p3 = Triangle(color=GOLD, stroke_width=5).scale(0.8).move_to(station_3 + RIGHT*2.5 + DOWN*0.5)
        self.play(Create(p1), Create(p2), Create(p3), run_time=2)
        
        # Draw Orion Stars
        s1 = Dot(radius=0.15, color=WHITE).move_to(p1.get_top() + UP*2)
        s2 = Dot(radius=0.15, color=WHITE).move_to(p2.get_top() + UP*2)
        s3 = Dot(radius=0.15, color=WHITE).move_to(p3.get_top() + UP*2)
        lines = VGroup(DashedLine(s1, p1.get_top()), DashedLine(s2, p2.get_top()), DashedLine(s3, p3.get_top())).set_color(BLUE)
        
        self.play(FadeIn(VGroup(s1, s2, s3)), Create(lines), run_time=2)
        
        # Pulsing stars updater
        def pulse_stars(m, dt):
            m.set_opacity(0.5 + 0.5 * np.sin(self.renderer.time * 5))
        s1.add_updater(pulse_stars)
        s2.add_updater(pulse_stars)
        s3.add_updater(pulse_stars)
        
        self.camera.frame.add_updater(lambda m, dt: m.shift(UP * dt * 0.1))
        self.wait(phase_time - 5)

        # --- CHAPTER 4: SECRET CHAMBERS (LEFT 20) ---
        station_4 = station_3 + LEFT * 20
        self.camera.frame.clear_updaters()
        self.play(self.camera.frame.animate.move_to(station_4), run_time=3)
        
        c3_title = Text("CHAPTER 3: THE INTERIOR", font="sans-serif", color=PURPLE, weight=BOLD).move_to(station_4 + UP*3.5)
        self.play(Write(c3_title), run_time=1)
        
        # Draw a complex cross-section
        cross_section = Triangle(color=WHITE).scale(3).move_to(station_4)
        tunnel = Line(cross_section.get_bottom() + LEFT*2 + UP*1, cross_section.get_center(), color=RED, stroke_width=6)
        kings_chamber = Rectangle(width=1, height=0.5, color=YELLOW, fill_opacity=1).move_to(cross_section.get_center() + UP*0.5)
        queens_chamber = Rectangle(width=0.8, height=0.4, color=BLUE, fill_opacity=1).move_to(cross_section.get_center() + DOWN*0.5)
        
        self.play(Create(cross_section), run_time=1.5)
        self.play(Create(tunnel), run_time=1)
        self.play(FadeIn(kings_chamber), FadeIn(queens_chamber), run_time=1)
        
        # Holographic scanning line moving up and down the pyramid
        scan_line = Line(LEFT*4, RIGHT*4, color=GREEN).move_to(station_4 + DOWN*2)
        scan_line.add_updater(lambda m, dt: m.set_y(station_4[1] - 2 + 4 * abs(np.sin(self.renderer.time * 0.5))))
        self.add(scan_line)
        
        self.wait(phase_time - 4.5)

        # --- CHAPTER 5: CONCLUSION & CTA (BACK TO ORIGIN) ---
        self.play(self.camera.frame.animate.move_to(ORIGIN).scale(1.3), run_time=4)
        
        cta_text = Text("SUBSCRIBE FOR MORE MYSTERIES", font="sans-serif", weight=BOLD, color=RED).scale(1.2).move_to(DOWN*3.5)
        self.play(Write(cta_text), run_time=2)
        
        # Make the original pyramid glow heavily
        glow = img.copy().set_color(GOLD).set_opacity(0.4)
        self.add(glow)
        glow.add_updater(lambda m, dt: m.scale(1.001).set_opacity(m.get_fill_opacity() * 0.99))
        
        self.camera.frame.add_updater(lambda m, dt: m.scale(1 + 0.005 * dt))
        self.wait(phase_time - 6)
        
        # Final fade out
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)
