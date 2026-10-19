from manim import *

class MyFirstAnimation(Scene):
    def construct(self):
        # 1. Create a title
        title = Text("Cloud Manim Render", font_size=40, color=BLUE)
        title.to_edge(UP)

        # 2. Create a circle and a square
        circle = Circle(radius=1.5, color=YELLOW, fill_opacity=0.5)
        square = Square(side_length=2.5, color=RED, fill_opacity=0.5)

        # 3. Animate elements
        self.play(Write(title))
        self.wait(0.5)
        
        self.play(DrawBorderThenFill(circle))
        self.wait(0.5)

        # Transform circle into square
        self.play(Transform(circle, square))
        self.wait(1)

        # Fade everything out
        self.play(FadeOut(title), FadeOut(circle))
        self.wait(0.5)
