from manim import *
import random

class SpaceMystery(MovingCameraScene):
    def construct(self):
        # 1. SETUP: Dark Cinematic Atmosphere
        self.camera.background_color = "#050608"
        
        # 2. STARFIELD PARTICLES
        stars = VGroup(*[
            Dot(
                point=[random.uniform(-7, 7), random.uniform(-14, 14), 0],
                radius=random.uniform(0.01, 0.03),
                color=random.choice([WHITE, LIGHT_GREY, BLUE_E, YELLOW_E]),
                fill_opacity=random.uniform(0.2, 0.8)
            ) for _ in range(250)
        ])
        self.add(stars)
        self.wait(1)
        
        # 3. DOCUMENTARY UI / RADAR GRID
        grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-15, 15, 1],
            background_line_style={"stroke_color": TEAL, "stroke_width": 1, "stroke_opacity": 0.2}
        )
        self.play(Create(grid, run_time=3, lag_ratio=0.1))
        
        target_text = Text("TARGET: CYGNUS X-1 [BLACK HOLE]", font="Courier New", color=RED).scale(0.5).to_corner(UL)
        self.play(Write(target_text), run_time=1)
        self.wait(1)

        # 4. CINEMATIC TITLES
        title = Text("THE EVENT HORIZON", font="Courier New", weight=BOLD).scale(0.9)
        subtitle = Text("A Space Mystery", font="Courier New", color=BLUE).scale(0.6)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.2).move_to(UP * 5)
        
        self.play(Write(title, run_time=2))
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.wait(2)

        # 5. THE MYSTERY OBJECT: ACCRETION DISK (GLOW)
        black_hole_center = Circle(radius=0.8, color=BLACK, fill_opacity=1)
        
        disk = VGroup()
        colors = [ORANGE, RED_E, YELLOW_D]
        for i in range(12):
            ring = Ellipse(width=4.5 + i*0.25, height=1.5 + i*0.1, color=colors[i%3], stroke_opacity=0.8 - i*0.06, stroke_width=4 + i)
            disk.add(ring)
            
        bh_group = VGroup(disk, black_hole_center).move_to(DOWN * 1.5)
        
        # Animate Accretion Disk entry
        self.play(FadeIn(disk, scale=0.5), FadeIn(black_hole_center), run_time=3)
        
        # Add continuous rotation to the disk (updater runs infinitely)
        disk.add_updater(lambda m, dt: m.rotate(dt * 0.4))
        self.wait(2)

        # 6. MATHEMATICAL OVERLAY
        formula = MathTex(r"r_s", r"=", r"\frac{2GM}{c^2}").scale(1.5).next_to(bh_group, UP, buff=2)
        formula[0].set_color(RED)     # r_s
        formula[2].set_color(YELLOW)  # 2GM/c^2
        
        formula_label = Text("Schwarzschild Radius", font="Courier New", color=WHITE).scale(0.5).next_to(formula, DOWN)
        box = SurroundingRectangle(VGroup(formula, formula_label), color=BLUE, buff=0.4, corner_radius=0.2)
        
        self.play(Write(formula), run_time=2)
        self.play(FadeIn(formula_label), Create(box), run_time=1.5)
        self.wait(1)

        # 7. NARRATIVE TEXT
        narrative = Text(
            "Beyond this threshold,\nspace and time swap roles.\nNot even light escapes.", 
            font="Courier New", 
            color=LIGHT_GREY, 
            line_spacing=1.5
        ).scale(0.5).next_to(box, UP, buff=0.8)

        self.play(Write(narrative), run_time=4)
        self.wait(4)

        # 8. CINEMATIC ZOOM TO THE SINGULARITY
        # Fade out UI elements
        self.play(
            FadeOut(header), FadeOut(target_text), FadeOut(narrative), 
            FadeOut(formula), FadeOut(formula_label), FadeOut(box),
            run_time=1.5
        )
        
        # The zoom
        singularity_text = Text("ERROR: SINGULARITY REACHED", font="Courier New", color=RED).scale(0.04).move_to(bh_group.get_center())
        
        self.play(
            self.camera.frame.animate.scale(0.05).move_to(bh_group.get_center()),
            run_time=5,
            rate_func=ease_in_sine
        )
        
        self.play(Write(singularity_text), run_time=1)
        self.wait(2)
        
        # 9. OUTRO FADE
        self.play(FadeOut(singularity_text), FadeOut(disk), FadeOut(black_hole_center), FadeOut(grid), FadeOut(stars), run_time=2)
        self.wait(1)
