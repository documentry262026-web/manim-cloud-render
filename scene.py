import urllib.request
from manim import *
import random

class PyramidMystery(MovingCameraScene):
    def construct(self):
        # ==========================================
        # SETUP: BACKGROUND & CONTINUOUS MOTION DUST
        # ==========================================
        self.camera.background_color = "#0a0602" # Deep desert night/sepia
        
        # Create continuous drifting dust/sand particles
        dust = VGroup()
        for _ in range(200):
            d = Dot(radius=random.uniform(0.01, 0.04), color=random.choice([YELLOW_E, GOLD_E, WHITE]), fill_opacity=random.uniform(0.2, 0.6))
            d.move_to([random.uniform(-8, 8), random.uniform(-15, 15), 0])
            d.vx = random.uniform(-0.3, 0.3)
            d.vy = random.uniform(-0.3, 0.3)
            # This updater guarantees the particles NEVER stop moving
            d.add_updater(lambda m, dt: m.shift(RIGHT * m.vx * dt + UP * m.vy * dt))
            dust.add(d)
            
        self.add(dust)

        # ==========================================
        # SCENE 1: THE HOOK & REAL IMAGE
        # ==========================================
        # Download image WITH a User-Agent so Wikipedia doesn't block it!
        image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg"
        image_path = "pyramid.jpg"
        try:
            req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(image_path, 'wb') as out_file:
                out_file.write(response.read())
            pyramid_img = ImageMobject(image_path).scale(2.5)
        except:
            pyramid_img = Triangle(color=GOLD, fill_opacity=0.5).scale(4)

        pyramid_img.move_to(DOWN * 2)
        
        # Add continuous slow zoom to the image so it is NEVER still
        pyramid_img.add_updater(lambda m, dt: m.scale(1 + 0.02 * dt))
        
        self.play(FadeIn(pyramid_img), run_time=2)
        
        title_top = Text("HOW DID THEY", font="sans-serif", color=WHITE, weight=BOLD).scale(0.9).to_edge(UP, buff=2)
        title_bot = Text("BUILD THIS?", font="sans-serif", color=YELLOW, weight=BOLD).scale(1.2).next_to(title_top, DOWN, buff=0.2)
        
        # Keep everything moving while writing text
        self.play(Write(title_top), self.camera.frame.animate.shift(DOWN * 0.5), run_time=2)
        self.play(FadeIn(title_bot, shift=UP), self.camera.frame.animate.shift(DOWN * 0.5), run_time=2)
        
        # Slow pan instead of a static wait
        self.play(self.camera.frame.animate.scale(0.9).shift(DOWN * 0.5), run_time=3)

        # ==========================================
        # SCENE 2: THE 2.3 MILLION BLOCKS
        # ==========================================
        self.play(FadeOut(pyramid_img), FadeOut(title_top), FadeOut(title_bot), run_time=1.5)
        
        # Reset camera
        self.play(self.camera.frame.animate.move_to(ORIGIN).scale(1/0.9), run_time=1.5)
        
        block_text1 = Text("2.3 MILLION", font="sans-serif", color=GOLD, weight=BOLD).scale(1.1).to_edge(UP, buff=1.5)
        block_text2 = Text("STONE BLOCKS", font="sans-serif", color=WHITE).scale(0.8).next_to(block_text1, DOWN)
        
        self.play(Write(block_text1), FadeIn(block_text2, shift=DOWN), run_time=2)

        # Cascading grid of blocks
        blocks = VGroup(*[Square(side_length=0.4, color=GOLD_E, fill_opacity=0.7) for _ in range(48)])
        blocks.arrange_in_grid(rows=8, cols=6, buff=0.1).next_to(block_text2, DOWN, buff=1)
        
        # Animate blocks falling into place while camera slowly pans down
        self.play(
            LaggedStart(*[FadeIn(b, shift=DOWN*2) for b in blocks], lag_ratio=0.05),
            self.camera.frame.animate.shift(DOWN * 1.5),
            run_time=4
        )
        
        weight_text = Text("EACH WEIGHING UP TO 15 TONS", font="sans-serif", color=RED_A).scale(0.6).next_to(blocks, DOWN, buff=0.8)
        
        # Highlight one block continuously
        target_block = blocks[20]
        target_block.add_updater(lambda m, dt: m.rotate(dt * 0.5).set_color(RED))
        
        self.play(Write(weight_text), self.camera.frame.animate.scale(0.8).move_to(target_block), run_time=3.5)

        # ==========================================
        # SCENE 3: THE RAMP METHOD (ANIMATIC)
        # ==========================================
        self.play(FadeOut(blocks), FadeOut(block_text1), FadeOut(block_text2), FadeOut(weight_text), run_time=1.5)
        
        # Reset camera while moving
        self.play(self.camera.frame.animate.move_to(ORIGIN).scale(1/0.8), run_time=2)
        
        method_text = Text("PULLED ON WOODEN SLEDS", font="sans-serif", color=WHITE).scale(0.7).to_edge(UP, buff=2)
        self.play(Write(method_text), run_time=1.5)
        
        # Draw the Ramp
        ramp = Polygon(LEFT*3 + DOWN*2, RIGHT*3 + DOWN*2, RIGHT*3 + UP*1, color=LIGHT_GREY, fill_opacity=0.2)
        self.play(Create(ramp), run_time=2)
        
        # Draw the Sled & Block
        sled = Line(start=LEFT*0.5, end=RIGHT*0.5, color=ORANGE, stroke_width=6)
        block = Square(side_length=0.8, color=GOLD, fill_opacity=0.9)
        block.next_to(sled, UP, buff=0)
        sled_group = VGroup(sled, block).move_to(ramp.get_vertices()[0] + UP*0.5)
        sled_group.rotate(ramp.get_angle())
        
        rope = Line(sled_group.get_right(), sled_group.get_right() + RIGHT*2 + UP*1, color=WHITE)
        
        self.play(FadeIn(sled_group), Create(rope), run_time=1.5)
        
        # Animate pulling up the ramp
        pull_group = VGroup(sled_group, rope)
        self.play(
            pull_group.animate.shift(RIGHT*4.5 + UP*2.25), 
            self.camera.frame.animate.shift(RIGHT*1 + UP*0.5), # Camera follows the pull
            run_time=4,
            rate_func=linear
        )
        
        # ==========================================
        # SCENE 4: NIGHT SKY ALIGNMENT
        # ==========================================
        self.play(FadeOut(ramp), FadeOut(pull_group), FadeOut(method_text), run_time=1.5)
        
        # Change to night sky (Turn dust into stars)
        self.play(
            self.camera.frame.animate.move_to(UP*2).scale(1.2),
            dust.animate.set_color(WHITE),
            run_time=3
        )
        
        align_text1 = Text("ALIGNED TO TRUE NORTH", font="sans-serif", color=BLUE_A, weight=BOLD).scale(0.8).move_to(UP*5)
        align_text2 = Text("Margin of error: 0.05 degrees", font="sans-serif", color=LIGHT_GREY).scale(0.5).next_to(align_text1, DOWN)
        
        pyramid_silhouette = Triangle(color=BLACK, fill_opacity=1).scale(3).move_to(DOWN*2)
        pyramid_glow = Triangle(color=BLUE_E, fill_opacity=0.3).scale(3.1).move_to(DOWN*2)
        
        self.play(FadeIn(pyramid_glow), FadeIn(pyramid_silhouette), Write(align_text1), run_time=2.5)
        self.play(FadeIn(align_text2, shift=UP), run_time=1.5)
        
        # Shoot a laser/alignment beam up to the stars
        beam = Line(pyramid_silhouette.get_top(), pyramid_silhouette.get_top() + UP*8, color=TEAL, stroke_width=4)
        
        # Keep zooming out slowly to show scale
        self.play(
            Create(beam), 
            self.camera.frame.animate.scale(1.1).shift(UP*1), 
            run_time=4
        )
        
        # ==========================================
        # OUTRO
        # ==========================================
        outro = Text("A MYSTERY THAT STILL CAPTIVATES US", font="sans-serif", color=YELLOW).scale(0.6).move_to(UP*1)
        
        self.play(
            FadeIn(outro, shift=UP),
            self.camera.frame.animate.shift(UP*0.5),
            run_time=3
        )
        
        # Final fade out
        self.play(
            FadeOut(outro), FadeOut(beam), FadeOut(pyramid_silhouette), FadeOut(pyramid_glow),
            FadeOut(align_text1), FadeOut(align_text2),
            run_time=2
        )
        
        # Let the dust/stars drift out
        self.play(self.camera.frame.animate.scale(0.9), run_time=3)
