import urllib.request
import os
from manim import *
import random

class PyramidMystery(MovingCameraScene):
    def construct(self):
        # --- 1. SETUP & AUDIO ---
        if os.path.exists("voiceover.wav"):
            self.add_sound("voiceover.wav")

        self.camera.background_color = "#0a0a0a" # Dark cinematic studio
        
        # Global Grid Background
        grid = NumberPlane(x_range=[-30, 30, 1], y_range=[-30, 30, 1],
                           background_line_style={"stroke_color": DARK_GREY, "stroke_opacity": 0.3})
        self.add(grid)

        # Global Sandstorm (Never stops moving)
        sand_particles = VGroup(*[
            Dot(radius=random.uniform(0.01, 0.04), color=random.choice([YELLOW_A, GOLD_E, ORANGE]), fill_opacity=random.uniform(0.3, 0.6)) 
            for _ in range(300)
        ])
        for s in sand_particles:
            s.move_to([random.uniform(-15, 15), random.uniform(-15, 15), 0])
            
        def update_sand(mob, dt):
            # The sand stays with the camera!
            cam_center = self.camera.frame.get_center()
            for s in mob:
                s.shift(LEFT * dt * random.uniform(2, 4) + DOWN * dt * random.uniform(0.5, 1.5))
                if s.get_x() < cam_center[0] - 10: s.set_x(cam_center[0] + 10)
                if s.get_y() < cam_center[1] - 15: s.set_y(cam_center[1] + 15)
                if s.get_y() > cam_center[1] + 15: s.set_y(cam_center[1] - 15)
                    
        sand_particles.add_updater(update_sand)
        self.add(sand_particles)

        # --- STATION 1: THE HOOK (ORIGIN) [0 - 15s] ---
        # Image Download
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg"
        image_path = "pyramid.jpg"
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
                out_file.write(response.read())
            pyramid_img = ImageMobject(image_path).scale(2)
        except:
            pyramid_img = Triangle(color=GOLD, fill_opacity=0.5).scale(3)
        pyramid_img.move_to(ORIGIN)

        coords = Text("29.9792° N, 31.1342° E", font="Courier New", color=GREEN).scale(0.5).to_corner(UL)
        title1 = Text("THE GREAT MYSTERY", font="sans-serif", weight=BOLD, color=WHITE).scale(1.2).next_to(pyramid_img, UP)
        
        self.play(Create(grid), run_time=1.5)
        self.play(Write(coords), run_time=1)
        self.play(FadeIn(pyramid_img, scale=0.8), run_time=2)
        self.play(Write(title1), run_time=1)
        
        # Dynamic Target ring
        target = Circle(radius=3, color=RED).move_to(ORIGIN)
        self.play(Create(target), run_time=1)
        self.play(target.animate.scale(1.1).set_opacity(0), run_time=1)
        
        self.play(self.camera.frame.animate.scale(0.6), run_time=3)
        self.wait(1.5)
        self.play(self.camera.frame.animate.scale(1.5), run_time=2)

        # --- STATION 2: THE STATS (RIGHT 15) [15 - 35s] ---
        station2_pos = RIGHT * 15
        self.play(self.camera.frame.animate.move_to(station2_pos), run_time=3, rate_func=rate_functions.ease_in_out_cubic)
        
        stat_title = Text("SCALE & MASS", font="sans-serif", weight=BOLD, color=YELLOW).scale(1.5).move_to(station2_pos + UP*3)
        self.play(Write(stat_title), run_time=1)
        
        # Flash numbers rapidly
        num1 = Text("2,300,000", font="sans-serif", color=WHITE, weight=BOLD).scale(2).move_to(station2_pos + UP*1)
        lbl1 = Text("STONE BLOCKS", font="sans-serif", color=LIGHT_GREY).scale(0.8).next_to(num1, DOWN)
        
        self.play(FadeIn(num1, shift=UP), run_time=1)
        self.play(Write(lbl1), run_time=1)
        self.wait(1)
        
        block = Square(side_length=2, color=BLUE, fill_opacity=0.7).move_to(station2_pos + DOWN*2)
        weight_txt = Text("2.5 to 15 TONS", font="sans-serif", color=RED, weight=BOLD).scale(0.8).move_to(block.get_center())
        
        self.play(DrawBorderThenFill(block), run_time=1.5)
        self.play(Write(weight_txt), run_time=1)
        self.play(Indicate(block, color=RED, scale_factor=1.2), run_time=1.5)
        self.play(num1.animate.set_color(YELLOW), run_time=1)
        self.wait(2)

        # --- STATION 3: THE TRANSPORT (DOWN 12) [35 - 55s] ---
        station3_pos = station2_pos + DOWN * 12
        self.play(self.camera.frame.animate.move_to(station3_pos), run_time=3)
        
        trans_title = Text("RIVER TRANSPORT", font="sans-serif", weight=BOLD, color=BLUE_B).scale(1.5).move_to(station3_pos + UP*3)
        self.play(FadeIn(trans_title, shift=DOWN), run_time=1)
        
        # Drawing the Nile
        river = FunctionGraph(lambda x: 0.5 * np.sin(x*2), x_range=[-5, 5], color=BLUE, stroke_width=25).move_to(station3_pos)
        self.play(Create(river), run_time=2)
        
        # Boat moving
        boat = Rectangle(width=1, height=0.4, color=DARK_BROWN, fill_opacity=1).move_to(river.point_from_proportion(0))
        boat_block = Square(side_length=0.4, color=LIGHT_GREY, fill_opacity=1).next_to(boat, UP, buff=0)
        boat_group = VGroup(boat, boat_block)
        
        self.play(FadeIn(boat_group), run_time=1)
        self.play(MoveAlongPath(boat_group, river), run_time=4, rate_func=linear)
        self.play(Flash(boat_group, color=YELLOW), run_time=1)
        
        # Flash a question
        q_mark = Text("HOW?", font="sans-serif", weight=BOLD, color=RED).scale(3).move_to(station3_pos)
        self.play(FadeIn(q_mark, scale=0.5), run_time=1)
        self.play(q_mark.animate.scale(1.5).set_opacity(0), run_time=1.5)
        self.wait(1.5)

        # --- STATION 4: MATH & ALIENS (LEFT 15) [55 - 75s] ---
        station4_pos = station3_pos + LEFT * 15
        self.play(self.camera.frame.animate.move_to(station4_pos), run_time=3)
        
        math_title = Text("PRECISION ENGINEERING", font="sans-serif", weight=BOLD, color=WHITE).scale(1.2).move_to(station4_pos + UP*3)
        self.play(Write(math_title), run_time=1)
        
        # Wireframe Pyramid
        base = Triangle(color=GOLD, stroke_width=4).scale(2.5).move_to(station4_pos + DOWN*1)
        center_line = DashedLine(base.get_top(), base.get_bottom(), color=WHITE)
        angle_arc = Angle(Line(base.get_bottom(), base.get_right()), Line(base.get_bottom(), base.get_top()), radius=0.8, color=RED)
        angle_txt = Text("51.5°", font="sans-serif", color=YELLOW).scale(0.7).next_to(angle_arc, UR, buff=0.1)
        
        self.play(Create(base), run_time=2)
        self.play(Create(center_line), run_time=1)
        self.play(Create(angle_arc), Write(angle_txt), run_time=1.5)
        
        # Orion Constellation overlay flash
        stars = VGroup(*[Dot(radius=0.1, color=BLUE_A).move_to(station4_pos + pos) for pos in [UP*2+LEFT*2, UP*1+LEFT*0.5, ORIGIN]])
        star_lines = VGroup(Line(stars[0], stars[1]), Line(stars[1], stars[2])).set_color(BLUE_C).set_opacity(0.5)
        
        self.play(FadeIn(stars), Create(star_lines), run_time=2)
        self.play(Flash(stars[0]), Flash(stars[1]), Flash(stars[2]), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(stars), FadeOut(star_lines), run_time=1)

        # --- STATION 5: THE OUTRO (BACK TO ORIGIN) [75 - 90s] ---
        self.play(self.camera.frame.animate.move_to(ORIGIN).scale(1.2), run_time=4)
        
        # Swarm of mini blocks flying into the capstone
        swarm = VGroup(*[Square(side_length=0.2, color=GOLD, fill_opacity=0.6).move_to(ORIGIN + [random.uniform(-8, 8), random.uniform(-5, 5), 0]) for _ in range(40)])
        self.play(FadeIn(swarm), run_time=1)
        
        capstone_pos = pyramid_img.get_top() + DOWN*0.5
        self.play(
            *[s.animate.move_to(capstone_pos).set_opacity(0) for s in swarm],
            run_time=2, rate_func=rate_functions.ease_in_expo
        )
        
        # Glowing Capstone
        capstone = Triangle(color=YELLOW, fill_opacity=1).scale(0.5).move_to(capstone_pos)
        glow = Circle(radius=2, color=YELLOW, fill_opacity=0.2).move_to(capstone_pos)
        
        self.play(FadeIn(capstone), FadeIn(glow), run_time=1.5)
        self.play(glow.animate.scale(3).set_opacity(0), run_time=1.5)
        
        final_text = Text("STILL A MYSTERY.", font="sans-serif", weight=BOLD, color=WHITE).scale(2).move_to(DOWN*3)
        self.play(Write(final_text), run_time=2)
        
        # Final pull out
        self.play(self.camera.frame.animate.scale(1.5), run_time=3)
        self.wait(1)
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=2)
