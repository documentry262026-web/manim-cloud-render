import urllib.request
import os
import json
import random
import numpy as np
from manim import *

class PyramidDocumentary(MovingCameraScene):
    def run_seq(self, total_time, steps, focus_mob=None):
        """
        Executes a list of animation lambdas across total_time.
        Guarantees NO step takes longer than 1.5s by injecting active micro-animations
        (Flashes, Pulses, Camera Micro-Zooms) so the screen is NEVER still.
        """
        n = len(steps)
        step_time = min(1.5, total_time / max(n, 1))
        elapsed = 0.0

        for step_fn in steps:
            rt = min(step_time, max(0.4, total_time - elapsed))
            step_fn(rt)
            elapsed += rt

        toggle = 0
        while total_time - elapsed > 0.15:
            chunk = min(1.1, total_time - elapsed)
            if focus_mob is not None:
                if toggle % 3 == 0:
                    self.play(Indicate(focus_mob, color=YELLOW, scale_factor=1.08), run_time=chunk)
                elif toggle % 3 == 1:
                    self.play(Flash(focus_mob.get_center(), color=GOLD, flash_radius=1.2), run_time=chunk)
                else:
                    shift_dir = UP * 0.15 if toggle % 2 == 0 else DOWN * 0.15
                    self.play(self.camera.frame.animate.shift(shift_dir), run_time=chunk)
            else:
                self.play(self.camera.frame.animate.scale(0.98 if toggle % 2 == 0 else 1.02), run_time=chunk)
            elapsed += chunk
            toggle += 1

    def construct(self):
        # --- 1. LOAD AUDIO & EXACT SENTENCE DURATIONS ---
        if os.path.exists("voiceover.wav"):
            self.add_sound("voiceover.wav")

        if os.path.exists("durations.json"):
            with open("durations.json", "r") as f:
                D = json.load(f)
        else:
            D = [8.0] * 25

        self.camera.background_color = "#08080c"

        # --- 2. GLOBAL INFINITE INVESTIGATION BOARD & SANDSTORM ---
        grid = NumberPlane(
            x_range=[-60, 60, 1], y_range=[-60, 60, 1],
            background_line_style={"stroke_color": TEAL_E, "stroke_opacity": 0.25}
        )
        self.add(grid)

        sand_particles = VGroup(*[
            Dot(
                radius=random.uniform(0.015, 0.045),
                color=random.choice([YELLOW_A, GOLD_E, ORANGE]),
                fill_opacity=random.uniform(0.3, 0.65)
            ) for _ in range(280)
        ])
        for s in sand_particles:
            s.move_to([random.uniform(-16, 16), random.uniform(-10, 10), 0])

        def update_sand(mob, dt):
            c = self.camera.frame.get_center()
            for s in mob:
                s.shift(LEFT * dt * random.uniform(2.2, 4.2) + DOWN * dt * random.uniform(0.4, 1.4))
                if s.get_x() < c[0] - 12: s.set_x(c[0] + 12)
                if s.get_y() < c[1] - 8: s.set_y(c[1] + 8)
                if s.get_y() > c[1] + 8: s.set_y(c[1] - 8)

        sand_particles.add_updater(update_sand)
        self.add(sand_particles)

        # Download real Pyramid image with browser User-Agent
        image_path = "pyramid.jpg"
        req = urllib.request.Request(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        try:
            with urllib.request.urlopen(req) as resp, open(image_path, 'wb') as out:
                out.write(resp.read())
            pyramid_img = ImageMobject(image_path).scale(1.8)
        except:
            pyramid_img = Triangle(color=GOLD, fill_opacity=0.6).scale(2.8)
        pyramid_img.move_to(ORIGIN)

        # =========================================================================
        # [00:00 - 01:00] STATION 1: THE HOOK & GIZA (ORIGIN)
        # =========================================================================

        # Line 0: हज़ारों साल पहले... बिना मशीनों के पिरामिड्स कैसे बनाई गईं?
        coords = Text("GPS: 29.9792° N, 31.1342° E", font="Courier New", color=GREEN, weight=BOLD).scale(0.55).to_corner(UL)
        title1 = Text("HOW WERE THEY BUILT?", font="sans-serif", weight=BOLD, color=WHITE).scale(0.95).to_edge(UP, buff=0.6)
        no_mach = Text("NO CRANES  |  NO MODERN MACHINES", font="sans-serif", color=RED, weight=BOLD).scale(0.6).next_to(pyramid_img, DOWN, buff=0.4)
        target_ring = Circle(radius=2.6, color=RED, stroke_width=4).move_to(ORIGIN)

        self.run_seq(D[0], [
            lambda rt: self.play(Write(coords), run_time=rt),
            lambda rt: self.play(FadeIn(pyramid_img, scale=0.8), run_time=rt),
            lambda rt: self.play(Write(title1), run_time=rt),
            lambda rt: self.play(Create(target_ring), FadeIn(no_mach, shift=UP), run_time=rt),
            lambda rt: self.play(target_ring.animate.scale(1.25).set_opacity(0), self.camera.frame.animate.scale(0.9), run_time=rt),
        ], focus_mob=no_mach)

        # Line 1: मिस्र के राजाओं (फ़राओ) की कब्रों के रूप में बनाए गए थे
        st1_sub = RIGHT * 6.5
        pharaoh_title = Text("ROYAL TOMBS OF THE PHARAOHS", font="sans-serif", color=GOLD, weight=BOLD).scale(0.65).move_to(st1_sub + UP * 2.8)
        p_trio = VGroup(
            Triangle(color=GOLD, fill_opacity=0.25, stroke_width=4).scale(1.4),
            Triangle(color=GOLD, fill_opacity=0.35, stroke_width=5).scale(1.8),
            Triangle(color=GOLD, fill_opacity=0.25, stroke_width=4).scale(1.1)
        ).arrange(RIGHT, buff=0.4, aligned_edge=DOWN).move_to(st1_sub + DOWN * 0.4)
        tomb_box = Rectangle(width=0.6, height=0.35, color=YELLOW, fill_opacity=0.9).move_to(p_trio[1].get_center() + DOWN * 0.3)

        self.run_seq(D[1], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st1_sub).scale(1.1), run_time=rt),
            lambda rt: self.play(Write(pharaoh_title), run_time=rt),
            lambda rt: self.play(Create(p_trio), run_time=rt),
            lambda rt: self.play(DrawBorderThenFill(tomb_box), Flash(tomb_box, color=YELLOW), run_time=rt),
            lambda rt: self.play(Indicate(p_trio[1], color=GOLD, scale_factor=1.1), run_time=rt),
        ], focus_mob=tomb_box)

        # Line 2: ग्रेट पिरामिड ऑफ़ गीज़ा, लगभग 4,500 साल पहले
        giza_lbl = Text("GREAT PYRAMID OF GIZA", font="sans-serif", color=WHITE, weight=BOLD).scale(0.8).move_to(st1_sub + UP * 2.0)
        yr_num = Text("4,500 YEARS OLD", font="sans-serif", color=YELLOW, weight=BOLD).scale(1.3).move_to(st1_sub + DOWN * 2.5)
        t_line = NumberLine(x_range=[-2600, 2026, 1000], length=7, color=BLUE_C).move_to(st1_sub + DOWN * 3.4)
        t_dot = Dot(color=RED, radius=0.14).move_to(t_line.n2p(2026))

        self.run_seq(D[2], [
            lambda rt: self.play(Transform(pharaoh_title, giza_lbl), run_time=rt),
            lambda rt: self.play(FadeIn(yr_num, scale=1.4), run_time=rt),
            lambda rt: self.play(Create(t_line), FadeIn(t_dot), run_time=rt),
            lambda rt: self.play(t_dot.animate.move_to(t_line.n2p(-2560)), Flash(yr_num, color=RED), run_time=rt),
        ], focus_mob=yr_num)

        # Line 3: इतने भारी पत्थरों को उठाकर, एक के ऊपर एक रखकर कैसे बनाई गई?
        st1_stack = st1_sub + UP * 8
        stack_blocks = VGroup(*[
            Rectangle(width=3.6 - i * 0.45, height=0.5, color=BLUE_D, fill_opacity=0.85, stroke_color=WHITE)
            for i in range(6)
        ]).arrange(UP, buff=0.05).move_to(st1_stack + DOWN * 0.5)
        blk_count = Text("2,300,000 STONE BLOCKS!", font="sans-serif", color=RED, weight=BOLD).scale(0.95).move_to(st1_stack + UP * 2.6)
        q_big = Text("HOW?!", font="sans-serif", color=YELLOW, weight=BOLD).scale(1.6).next_to(stack_blocks, RIGHT, buff=0.8)

        self.run_seq(D[3], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st1_stack), run_time=rt),
            lambda rt: self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.8) for b in stack_blocks], lag_ratio=0.2), run_time=rt),
            lambda rt: self.play(Write(blk_count), run_time=rt),
            lambda rt: self.play(FadeIn(q_big, scale=0.5), Indicate(stack_blocks, color=RED), run_time=rt),
        ], focus_mob=stack_blocks)

        # =========================================================================
        # [01:00 - 02:00] STATION 2: GROUND, QUARRY, NILE BOAT & WET SAND (RIGHT * 22)
        # =========================================================================

        # Line 4: सही जगह चुनी जाती थी। ज़मीन को बराबर किया जाता था
        st2 = RIGHT * 22
        lvl_title = Text("STEP 1: PRECISION GROUND LEVELING", font="sans-serif", color=GREEN, weight=BOLD).scale(0.75).move_to(st2 + UP * 2.8)
        rocky_ground = VMobject(color=ORANGE, stroke_width=6).set_points_as_corners([
            st2 + LEFT * 5 + DOWN * 1, st2 + LEFT * 3 + DOWN * 0.2, st2 + LEFT * 1 + DOWN * 1.4,
            st2 + RIGHT * 1.5 + DOWN * 0.3, st2 + RIGHT * 3.5 + DOWN * 1.2, st2 + RIGHT * 5 + DOWN * 0.6
        ])
        flat_ground = Line(st2 + LEFT * 5 + DOWN * 1, st2 + RIGHT * 5 + DOWN * 1, color=GREEN, stroke_width=8)
        lvl_badge = Text("ERROR < 2 CM ACROSS 230 METERS!", font="Courier New", color=YELLOW, weight=BOLD).scale(0.6).move_to(st2 + UP * 0.8)

        self.run_seq(D[4], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st2), Write(lvl_title), run_time=rt),
            lambda rt: self.play(Create(rocky_ground), run_time=rt),
            lambda rt: self.play(Transform(rocky_ground, flat_ground), run_time=rt),
            lambda rt: self.play(FadeIn(lvl_badge, shift=UP), Flash(flat_ground.get_center(), color=GREEN), run_time=rt),
        ], focus_mob=lvl_badge)

        # Line 5: हज़ारों बड़े पत्थरों को काटकर तैयार किया जाता था (लाइमस्टोन)
        st2_quarry = st2 + DOWN * 9
        q_title = Text("STEP 2: CUTTING LIMESTONE BLOCKS", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.75).move_to(st2_quarry + UP * 2.8)
        raw_rock = Rectangle(width=5, height=2.6, color=GOLD_E, fill_opacity=0.7).move_to(st2_quarry)
        cut_grid = VGroup(*[
            Square(side_length=0.85, color=GOLD_A, fill_opacity=0.85, stroke_color=RED, stroke_width=3)
            for _ in range(8)
        ]).arrange_in_grid(rows=2, cols=4, buff=0.05).move_to(st2_quarry)
        wt_lbl = Text("EACH BLOCK: 2.5 TO 15 TONS", font="sans-serif", color=RED, weight=BOLD).scale(0.7).move_to(st2_quarry + DOWN * 2.4)

        self.run_seq(D[5], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st2_quarry), Write(q_title), run_time=rt),
            lambda rt: self.play(DrawBorderThenFill(raw_rock), run_time=rt),
            lambda rt: self.play(ReplacementTransform(raw_rock, cut_grid), run_time=rt),
            lambda rt: self.play(cut_grid.animate.arrange_in_grid(rows=2, cols=4, buff=0.35).move_to(st2_quarry), Write(wt_lbl), run_time=rt),
        ], focus_mob=cut_grid)

        # Line 6: नावों के ज़रिए पहुँचाया जाता था (Nile River Boat Transport!)
        st2_nile = st2_quarry + DOWN * 9
        nile_title = Text("STEP 3: NILE RIVER TRANSPORT", font="sans-serif", color=BLUE_B, weight=BOLD).scale(0.8).move_to(st2_nile + UP * 2.8)
        river = FunctionGraph(lambda x: 0.55 * np.sin(x * 1.4), x_range=[-5.5, 5.5], color=BLUE, stroke_width=24).shift(st2_nile + DOWN * 0.3)
        boat_hull = Polygon(LEFT * 0.7 + UP * 0.2, RIGHT * 0.7 + UP * 0.2, RIGHT * 0.45 + DOWN * 0.2, LEFT * 0.45 + DOWN * 0.2, color=DARK_BROWN, fill_opacity=1)
        cargo = Square(side_length=0.5, color=GOLD, fill_opacity=1).next_to(boat_hull, UP, buff=0)
        boat_grp = VGroup(boat_hull, cargo).move_to(river.point_from_proportion(0))

        self.run_seq(D[6], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st2_nile), Write(nile_title), run_time=rt),
            lambda rt: self.play(Create(river), run_time=rt),
            lambda rt: self.play(FadeIn(boat_grp, scale=0.6), run_time=rt),
            lambda rt: self.play(MoveAlongPath(boat_grp, river), run_time=rt, rate_func=linear),
            lambda rt: self.play(Flash(boat_grp, color=YELLOW), run_time=rt),
        ], focus_mob=boat_grp)

        # Line 7: स्लेज जैसी लकड़ी की गाड़ियों का इस्तेमाल
        st2_sled = st2_nile + RIGHT * 16
        sled_title = Text("HEAVY WOODEN SLEDGES", font="sans-serif", color=ORANGE, weight=BOLD).scale(0.8).move_to(st2_sled + UP * 2.8)
        desert_floor = Line(st2_sled + LEFT * 5.5 + DOWN * 1.5, st2_sled + RIGHT * 5.5 + DOWN * 1.5, color=GOLD_E, stroke_width=10)
        sled_base = Rectangle(width=2.2, height=0.25, color=DARK_BROWN, fill_opacity=1)
        sled_stone = Rectangle(width=1.8, height=1.3, color=LIGHT_GREY, fill_opacity=0.95).next_to(sled_base, UP, buff=0)
        stone_txt = Text("2.5 TONS", font="sans-serif", color=RED, weight=BOLD).scale(0.45).move_to(sled_stone)
        rope_line = Line(sled_base.get_right(), sled_base.get_right() + RIGHT * 2.0, color=YELLOW_D, stroke_width=5)
        sled_unit = VGroup(sled_base, sled_stone, stone_txt, rope_line).move_to(st2_sled + LEFT * 3 + DOWN * 0.6)

        self.run_seq(D[7], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st2_sled), Write(sled_title), run_time=rt),
            lambda rt: self.play(Create(desert_floor), FadeIn(sled_unit, shift=RIGHT), run_time=rt),
            lambda rt: self.play(sled_unit.animate.shift(RIGHT * 1.5), run_time=rt),
            lambda rt: self.play(Indicate(sled_stone, color=RED, scale_factor=1.15), run_time=rt),
        ], focus_mob=sled_unit)

        # Line 8: रेत को गीला करने से पत्थरों को खींचना आसान (Wet Sand Physics!)
        wet_title = Text("WET SAND = 50% LESS FRICTION!", font="sans-serif", color=BLUE_A, weight=BOLD).scale(0.75).move_to(st2_sled + UP * 1.8)
        water_drops = VGroup(*[
            Dot(radius=0.09, color=BLUE_B).move_to(sled_unit.get_right() + UP * 0.8 + RIGHT * (i * 0.25))
            for i in range(6)
        ])
        wet_patch = Line(st2_sled + LEFT * 1 + DOWN * 1.5, st2_sled + RIGHT * 5 + DOWN * 1.5, color=BLUE_C, stroke_width=12)

        self.run_seq(D[8], [
            lambda rt: self.play(Write(wet_title), FadeIn(water_drops, shift=DOWN * 0.5), run_time=rt),
            lambda rt: self.play(water_drops.animate.shift(DOWN * 1.5).set_opacity(0), Create(wet_patch), run_time=rt),
            lambda rt: self.play(sled_unit.animate.shift(RIGHT * 3.8), run_time=rt, rate_func=rate_functions.ease_out_cubic),
            lambda rt: self.play(Flash(sled_unit, color=BLUE_A), run_time=rt),
        ], focus_mob=sled_unit)

        # =========================================================================
        # [02:00 - 03:00] STATION 3: RAMP THEORIES & ENGINEERING (UP * 18)
        # =========================================================================

        # Line 9: इतने भारी पत्थरों को ऊँचाई तक कैसे पहुँचाया गया?
        st3 = UP * 18
        h_title = Text("THE HEIGHT CHALLENGE: 146.6 METERS", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.75).move_to(st3 + UP * 2.8)
        tall_pyr = Triangle(color=GOLD, stroke_width=5, fill_opacity=0.15).scale(2.5).move_to(st3 + DOWN * 0.5)
        h_arrow = DoubleArrow(tall_pyr.get_bottom() + LEFT * 3.2, tall_pyr.get_top() + LEFT * 3.2, color=RED, stroke_width=5)
        h_lbl = Text("146.6m", font="sans-serif", color=RED, weight=BOLD).scale(0.6).next_to(h_arrow, LEFT)

        self.run_seq(D[9], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st3), Write(h_title), run_time=rt),
            lambda rt: self.play(Create(tall_pyr), run_time=rt),
            lambda rt: self.play(GrowFromCenter(h_arrow), Write(h_lbl), run_time=rt),
            lambda rt: self.play(Flash(tall_pyr.get_top(), color=RED, flash_radius=1.0), run_time=rt),
        ], focus_mob=tall_pyr)

        # Line 10: इसके लिए एक थ्योरी है — रैम्प्स का इस्तेमाल
        ramp_lbl = Text("THEORY #1: INCLINED RAMPS", font="sans-serif", color=ORANGE, weight=BOLD).scale(0.8).move_to(st3 + UP * 2.0)
        ramp_line = Line(tall_pyr.get_bottom() + LEFT * 4.5, tall_pyr.get_top() + DOWN * 0.4, color=ORANGE, stroke_width=10)

        self.run_seq(D[10], [
            lambda rt: self.play(FadeIn(ramp_lbl, shift=DOWN), run_time=rt),
            lambda rt: self.play(Create(ramp_line), run_time=rt),
            lambda rt: self.play(Indicate(ramp_line, color=YELLOW), run_time=rt),
        ], focus_mob=ramp_line)

        # Line 11: मिट्टी, रेत और पत्थरों से बने ढलान वाले रास्ते
        mat_txt = Text("BUILT FROM: MUD + SAND + LIMESTONE CHIP", font="Courier New", color=GOLD_A, weight=BOLD).scale(0.55).move_to(st3 + DOWN * 3.2)
        ramp_supports = VGroup(*[
            Line(ramp_line.point_from_proportion(p), [ramp_line.point_from_proportion(p)[0], tall_pyr.get_bottom()[1], 0], color=ORANGE, stroke_opacity=0.6)
            for p in np.linspace(0.15, 0.85, 7)
        ])

        self.run_seq(D[11], [
            lambda rt: self.play(Create(ramp_supports), run_time=rt),
            lambda rt: self.play(Write(mat_txt), run_time=rt),
            lambda rt: self.play(Indicate(ramp_supports, color=ORANGE), run_time=rt),
        ], focus_mob=ramp_supports)

        # Line 12: मज़दूर इन रास्तों पर पत्थरों को धीरे-धीरे ऊपर खींचते थे
        r_sled = VGroup(
            Rectangle(width=0.9, height=0.15, color=DARK_BROWN, fill_opacity=1),
            Square(side_length=0.6, color=YELLOW, fill_opacity=0.95).shift(UP * 0.35)
        ).move_to(ramp_line.get_start()).rotate(ramp_line.get_angle())

        self.run_seq(D[12], [
            lambda rt: self.play(FadeIn(r_sled, scale=0.7), run_time=rt),
            lambda rt: self.play(MoveAlongPath(r_sled, ramp_line), run_time=rt, rate_func=linear),
            lambda rt: self.play(Flash(r_sled.get_center(), color=YELLOW, flash_radius=1.0), run_time=rt),
        ], focus_mob=r_sled)

        # Line 13: आज भी यह पूरी तरह साफ़ नहीं है कि कौन-सा तरीका इस्तेमाल हुआ था
        st3_right = st3 + RIGHT * 16
        mys_title = Text("WHICH RAMP SYSTEM WAS USED?", font="sans-serif", color=RED, weight=BOLD).scale(0.75).move_to(st3_right + UP * 2.8)
        cards = VGroup(
            VGroup(RoundedRectangle(width=3.4, height=2.2, corner_radius=0.2, color=BLUE), Text("STRAIGHT\nRAMP?", font="sans-serif", color=WHITE).scale(0.55)),
            VGroup(RoundedRectangle(width=3.4, height=2.2, corner_radius=0.2, color=GREEN), Text("SPIRAL\nRAMP?", font="sans-serif", color=WHITE).scale(0.55)),
            VGroup(RoundedRectangle(width=3.4, height=2.2, corner_radius=0.2, color=PURPLE), Text("INTERNAL\nTUNNEL?", font="sans-serif", color=WHITE).scale(0.55)),
        ).arrange(RIGHT, buff=0.6).move_to(st3_right)

        self.run_seq(D[13], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st3_right), Write(mys_title), run_time=rt),
            lambda rt: self.play(FadeIn(cards[0], shift=UP), run_time=rt),
            lambda rt: self.play(FadeIn(cards[1], shift=UP), run_time=rt),
            lambda rt: self.play(FadeIn(cards[2], shift=UP), run_time=rt),
        ], focus_mob=cards)

        # Line 14: अलग-अलग हिस्सों में अलग-अलग तरीके (Spiral + Straight Hybrid)
        st3_spiral = st3_right + UP * 10
        sp_title = Text("COMBINED SPIRAL & EXTERNAL RAMPS", font="sans-serif", color=GOLD, weight=BOLD).scale(0.7).move_to(st3_spiral + UP * 2.8)
        sp_pyr = Triangle(color=GOLD, fill_opacity=0.2, stroke_width=4).scale(2.6).move_to(st3_spiral + DOWN * 0.6)
        spiral_lines = VGroup(*[
            Line(
                st3_spiral + LEFT * (2.6 - i * 0.45) + DOWN * (2.4 - i * 0.85),
                st3_spiral + RIGHT * (2.3 - i * 0.45) + DOWN * (1.9 - i * 0.85),
                color=RED_B, stroke_width=6
            ) for i in range(5)
        ])

        self.run_seq(D[14], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st3_spiral), Write(sp_title), run_time=rt),
            lambda rt: self.play(Create(sp_pyr), run_time=rt),
            lambda rt: self.play(Create(spiral_lines, lag_ratio=0.3), run_time=rt),
            lambda rt: self.play(Indicate(spiral_lines, color=YELLOW), run_time=rt),
        ], focus_mob=spiral_lines)

        # Line 15: शानदार प्लानिंग, इंजीनियरिंग और टीमवर्क
        pillars = VGroup(
            Text("1. MASTER PLANNING", font="sans-serif", color=BLUE_B, weight=BOLD).scale(0.6),
            Text("2. PRECISION ENGINEERING", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.6),
            Text("3. MASSIVE TEAMWORK", font="sans-serif", color=GREEN, weight=BOLD).scale(0.6),
        ).arrange(DOWN, buff=0.35).move_to(st3_spiral + RIGHT * 4.2)

        self.run_seq(D[15], [
            lambda rt: self.play(FadeIn(pillars[0], shift=LEFT), run_time=rt),
            lambda rt: self.play(FadeIn(pillars[1], shift=LEFT), run_time=rt),
            lambda rt: self.play(FadeIn(pillars[2], shift=LEFT), Flash(sp_pyr.get_top(), color=GOLD), run_time=rt),
        ], focus_mob=pillars)

        # =========================================================================
        # [03:00 - 04:00] STATION 4: MATH, GEOMETRY & WORKFORCE (LEFT * 22)
        # =========================================================================

        # Line 16: मैथ्स और ज्योमेट्री का भी इस्तेमाल (Wireframe & 51.5° Angle!)
        st4 = LEFT * 22
        math_title = Text("MATHEMATICS & SACRED GEOMETRY", font="sans-serif", color=TEAL_A, weight=BOLD).scale(0.75).move_to(st4 + UP * 2.8)
        wf_pyr = Triangle(color=GOLD, stroke_width=5).scale(2.5).move_to(st4 + DOWN * 0.6)
        v_axis = DashedLine(wf_pyr.get_top(), [wf_pyr.get_top()[0], wf_pyr.get_bottom()[1], 0], color=WHITE)
        angle_arc = Arc(radius=0.85, start_angle=0, angle=0.9, arc_center=wf_pyr.get_left() + DOWN * 0.02, color=RED, stroke_width=6)
        angle_txt = Text("51.5° SLOPE", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.65).next_to(angle_arc, UR, buff=0.1)

        self.run_seq(D[16], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st4), Write(math_title), run_time=rt),
            lambda rt: self.play(Create(wf_pyr), Create(v_axis), run_time=rt),
            lambda rt: self.play(Create(angle_arc), Write(angle_txt), run_time=rt),
            lambda rt: self.play(Flash(angle_txt, color=RED), Indicate(wf_pyr, color=BLUE_B), run_time=rt),
        ], focus_mob=angle_txt)

        # Line 17: पिरामिड का बेस बहुत ध्यान से बनाया जाता था (Weight Distribution)
        base_line = Line(wf_pyr.get_left(), wf_pyr.get_right(), color=GREEN, stroke_width=10)
        arrows_down = VGroup(*[
            Arrow(start=base_line.point_from_proportion(p), end=base_line.point_from_proportion(p) + DOWN * 1.1, color=RED, buff=0)
            for p in np.linspace(0.1, 0.9, 6)
        ])
        mass_txt = Text("TOTAL MASS: 6,000,000 TONS", font="Courier New", color=WHITE, weight=BOLD).scale(0.65).move_to(st4 + DOWN * 3.1)

        self.run_seq(D[17], [
            lambda rt: self.play(Create(base_line), run_time=rt),
            lambda rt: self.play(LaggedStart(*[GrowArrow(a) for a in arrows_down], lag_ratio=0.15), run_time=rt),
            lambda rt: self.play(Write(mass_txt), run_time=rt),
        ], focus_mob=mass_txt)

        # Line 18: हर पत्थर को सही जगह पर रखना ज़रूरी था (माप में गलती vs सटीकता)
        st4_prec = st4 + DOWN * 9
        prec_title = Text("LASER-LIKE STONE PRECISION", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.75).move_to(st4_prec + UP * 2.8)
        bad_pyr = Triangle(color=RED, stroke_width=4).scale(1.4).move_to(st4_prec + LEFT * 3.2)
        bad_lbl = Text("WRONG ANGLE = COLLAPSE", font="sans-serif", color=RED).scale(0.45).next_to(bad_pyr, DOWN)
        good_pyr = Triangle(color=GREEN, stroke_width=5, fill_opacity=0.25).scale(1.4).move_to(st4_prec + RIGHT * 3.2)
        good_lbl = Text("0.5mm GAP = STANDS FOREVER", font="sans-serif", color=GREEN, weight=BOLD).scale(0.45).next_to(good_pyr, DOWN)

        self.run_seq(D[18], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st4_prec), Write(prec_title), run_time=rt),
            lambda rt: self.play(Create(bad_pyr), Write(bad_lbl), run_time=rt),
            lambda rt: self.play(bad_pyr.animate.rotate(0.25).set_opacity(0.3), Create(good_pyr), Write(good_lbl), run_time=rt),
            lambda rt: self.play(Flash(good_pyr, color=GREEN, flash_radius=1.5), run_time=rt),
        ], focus_mob=good_pyr)

        # Line 19: बहुत सारे वर्कर्स, कारीगरों और सुपरवाइज़र्स की ज़रूरत
        st4_work = st4_prec + DOWN * 9
        wk_title = Text("20,000+ ORGANIZED BUILDERS", font="sans-serif", color=GOLD, weight=BOLD).scale(0.8).move_to(st4_work + UP * 2.8)
        roles = VGroup(
            VGroup(RoundedRectangle(width=3.5, height=1.2, color=YELLOW), Text("ENGINEERS", font="sans-serif", color=YELLOW).scale(0.55)),
            VGroup(RoundedRectangle(width=3.5, height=1.2, color=BLUE_B), Text("SKILLED ARTISANS", font="sans-serif", color=BLUE_B).scale(0.55)),
            VGroup(RoundedRectangle(width=3.5, height=1.2, color=GREEN), Text("SUPERVISORS", font="sans-serif", color=GREEN).scale(0.55)),
        ).arrange(RIGHT, buff=0.5).move_to(st4_work + UP * 0.6)
        worker_dots = VGroup(*[Dot(radius=0.08, color=GOLD_A) for _ in range(48)]).arrange_in_grid(rows=4, cols=12, buff=0.25).move_to(st4_work + DOWN * 1.8)

        self.run_seq(D[19], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st4_work), Write(wk_title), run_time=rt),
            lambda rt: self.play(FadeIn(roles, shift=UP), run_time=rt),
            lambda rt: self.play(FadeIn(worker_dots, lag_ratio=0.05), run_time=rt),
        ], focus_mob=roles)

        # Line 20: गुलामों ने बनाए थे (Myth Busted!) -> संगठित मज़दूर और कुशल कारीगर
        st4_myth = st4_work + LEFT * 16
        myth_txt = Text("OLD MYTH: BUILT BY SLAVES", font="sans-serif", color=GREY_B, weight=BOLD).scale(0.85).move_to(st4_myth + UP * 1.5)
        cross_x = VGroup(
            Line(myth_txt.get_corner(UL), myth_txt.get_corner(DR), color=RED, stroke_width=10),
            Line(myth_txt.get_corner(DL), myth_txt.get_corner(UR), color=RED, stroke_width=10),
        )
        truth_txt = Text("REAL EVIDENCE: PAID SKILLED WORKERS!", font="sans-serif", color=GREEN, weight=BOLD).scale(0.85).move_to(st4_myth + DOWN * 0.5)
        proof_sub = Text("ARCHAEOLOGICAL PROOF: WORKERS' CITIES & RESPECTED TOMBS", font="Courier New", color=YELLOW).scale(0.5).move_to(st4_myth + DOWN * 2.0)

        self.run_seq(D[20], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st4_myth), Write(myth_txt), run_time=rt),
            lambda rt: self.play(Create(cross_x), run_time=rt),
            lambda rt: self.play(FadeIn(truth_txt, scale=1.2), run_time=rt),
            lambda rt: self.play(Write(proof_sub), Flash(truth_txt, color=GREEN), run_time=rt),
        ], focus_mob=truth_txt)

        # Line 21: इंसानी मेहनत और समझ का शानदार उदाहरण (Orion Constellation Blink!)
        st4_stars = st4_myth + UP * 10
        orion_title = Text("A MONUMENT OF HUMAN BRILLIANCE", font="sans-serif", color=WHITE, weight=BOLD).scale(0.75).move_to(st4_stars + UP * 2.8)
        o_pyr = Triangle(color=GOLD, stroke_width=5, fill_opacity=0.25).scale(2.2).move_to(st4_stars + DOWN * 1.0)
        belt_stars = VGroup(
            Dot(radius=0.14, color=BLUE_A).move_to(st4_stars + LEFT * 2.2 + UP * 1.2),
            Dot(radius=0.14, color=BLUE_A).move_to(st4_stars + UP * 1.5),
            Dot(radius=0.14, color=BLUE_A).move_to(st4_stars + RIGHT * 2.2 + UP * 1.9),
        )
        star_lines = VGroup(
            Line(belt_stars[0], belt_stars[1], color=BLUE_C),
            Line(belt_stars[1], belt_stars[2], color=BLUE_C),
            DashedLine(belt_stars[1], o_pyr.get_top(), color=YELLOW)
        )

        self.run_seq(D[21], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st4_stars), Write(orion_title), run_time=rt),
            lambda rt: self.play(Create(o_pyr), FadeIn(belt_stars), run_time=rt),
            lambda rt: self.play(Create(star_lines), run_time=rt),
            lambda rt: self.play(Flash(belt_stars[0]), Flash(belt_stars[1]), Flash(belt_stars[2]), run_time=rt),
        ], focus_mob=o_pyr)

        # =========================================================================
        # [04:00 - 05:00] STATION 5: GRAND SUMMARY & SWARM FINALE (ORIGIN)
        # =========================================================================

        # Line 22: पत्थरों की कटाई, ट्रांसपोर्टेशन, रैम्प्स, सही माप और हज़ारों लोगों की मेहनत
        st5 = DOWN * 18
        sum_title = Text("HOW THE GREAT PYRAMID WAS BUILT", font="sans-serif", color=GOLD, weight=BOLD).scale(0.85).move_to(st5 + UP * 2.8)
        hub_pyr = Triangle(color=GOLD, fill_opacity=0.35, stroke_width=5).scale(1.6).move_to(st5 + DOWN * 0.3)
        badges = VGroup(
            Text("1. QUARRYING", font="sans-serif", color=YELLOW, weight=BOLD).scale(0.55).move_to(st5 + LEFT * 4.5 + UP * 1.2),
            Text("2. NILE BOATS & SLEDGES", font="sans-serif", color=BLUE_B, weight=BOLD).scale(0.55).move_to(st5 + RIGHT * 4.5 + UP * 1.2),
            Text("3. ENGINEERED RAMPS", font="sans-serif", color=ORANGE, weight=BOLD).scale(0.55).move_to(st5 + LEFT * 4.5 + DOWN * 1.8),
            Text("4. MATH & 20,000 WORKERS", font="sans-serif", color=GREEN, weight=BOLD).scale(0.55).move_to(st5 + RIGHT * 4.5 + DOWN * 1.8),
        )
        rays = VGroup(*[Arrow(b.get_center(), hub_pyr.get_center(), color=WHITE, buff=0.8) for b in badges])

        self.run_seq(D[22], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st5), Write(sum_title), Create(hub_pyr), run_time=rt),
            lambda rt: self.play(FadeIn(badges[0]), GrowArrow(rays[0]), run_time=rt),
            lambda rt: self.play(FadeIn(badges[1]), GrowArrow(rays[1]), run_time=rt),
            lambda rt: self.play(FadeIn(badges[2]), GrowArrow(rays[2]), FadeIn(badges[3]), GrowArrow(rays[3]), run_time=rt),
            lambda rt: self.play(Flash(hub_pyr, color=GOLD, flash_radius=1.6), run_time=rt),
        ], focus_mob=hub_pyr)

        # Line 23: आर्कियोलॉजी और साइंस... हज़ारों साल बाद भी खड़े हैं
        st5_scan = st5 + RIGHT * 16
        sc_title = Text("MODERN SCIENCE & ARCHAEOLOGY", font="sans-serif", color=TEAL_A, weight=BOLD).scale(0.8).move_to(st5_scan + UP * 2.8)
        xray_pyr = Triangle(color=WHITE, stroke_width=5).scale(2.4).move_to(st5_scan + DOWN * 0.5)
        chambers = VGroup(
            Rectangle(width=1.1, height=0.45, color=YELLOW, fill_opacity=0.9).move_to(st5_scan + DOWN * 0.3),
            Rectangle(width=0.8, height=0.35, color=BLUE_B, fill_opacity=0.9).move_to(st5_scan + DOWN * 1.2),
        )
        scan_laser = Line(st5_scan + LEFT * 4 + DOWN * 2.5, st5_scan + RIGHT * 4 + DOWN * 2.5, color=GREEN, stroke_width=6)
        stand_txt = Text("STANDING STRONG FOR 4,500+ YEARS!", font="sans-serif", color=GOLD, weight=BOLD).scale(0.7).move_to(st5_scan + DOWN * 3.1)

        self.run_seq(D[23], [
            lambda rt: self.play(self.camera.frame.animate.move_to(st5_scan), Write(sc_title), Create(xray_pyr), run_time=rt),
            lambda rt: self.play(scan_laser.animate.shift(UP * 4.2), FadeIn(chambers), run_time=rt),
            lambda rt: self.play(scan_laser.animate.shift(DOWN * 4.2), Write(stand_txt), run_time=rt),
            lambda rt: self.play(Indicate(chambers, color=RED, scale_factor=1.2), run_time=rt),
        ], focus_mob=chambers)

        # Line 24: FINALE — Flying Block Swarm, Glowing Capstone & CTA!
        swarm = VGroup(*[
            Square(side_length=0.22, color=GOLD, fill_opacity=0.85).move_to(
                ORIGIN + [random.uniform(-7, 7), random.uniform(-4, 4), 0]
            ) for _ in range(45)
        ])
        capstone_pos = pyramid_img.get_top() + DOWN * 0.35
        capstone = Triangle(color=YELLOW, fill_opacity=1).scale(0.55).move_to(capstone_pos)
        glow_ring = Circle(radius=1.8, color=YELLOW, fill_opacity=0.35).move_to(capstone_pos)
        final_msg = Text("TIMELESS HUMAN ENGINEERING", font="sans-serif", weight=BOLD, color=GOLD).scale(0.95).move_to(DOWN * 2.6)
        cta_msg = Text("LIKE & SUBSCRIBE FOR MORE MYSTERIES!", font="sans-serif", weight=BOLD, color=RED).scale(0.8).move_to(DOWN * 3.4)

        self.run_seq(D[24], [
            lambda rt: self.play(self.camera.frame.animate.move_to(ORIGIN), FadeIn(swarm), run_time=rt),
            lambda rt: self.play(*[s.animate.move_to(capstone_pos).set_opacity(0) for s in swarm], run_time=rt, rate_func=rate_functions.ease_in_expo),
            lambda rt: self.play(FadeIn(capstone, scale=1.5), FadeIn(glow_ring), run_time=rt),
            lambda rt: self.play(glow_ring.animate.scale(3.2).set_opacity(0), Write(final_msg), run_time=rt),
            lambda rt: self.play(FadeIn(cta_msg, shift=UP), Flash(capstone_pos, color=YELLOW, flash_radius=2.0), run_time=rt),
            lambda rt: self.play(Indicate(cta_msg, color=YELLOW, scale_factor=1.12), self.camera.frame.animate.scale(1.15), run_time=rt),
        ], focus_mob=cta_msg)
