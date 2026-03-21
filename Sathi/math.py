from manim import *
import numpy as np

class FinalScene(MovingCameraScene):
    def construct(self):

        self.camera.background_color = "#2C3336"

        w = config.frame_width
        h = config.frame_height
        title_font = "Comic Sans MS"

        def wrap_text_dynamic(text, font_name, font_size, max_width, color="#FFFFFF", **kwargs):
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                current_line.append(word)
                test_text = Text(" ".join(current_line), font=font_name, font_size=font_size, **kwargs)
                if test_text.width > max_width and len(current_line) > 1:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(" ".join(current_line))
            vg = VGroup(*[Text(line, font=font_name, font_size=font_size, color=color, **kwargs) for line in lines])
            vg.arrange(DOWN, buff=0.15)
            return vg

        # ------------------------------------------------
        ## Section 1
        # ------------------------------------------------

        title_string = "Subtracting Money: Riya's Leftover"

        title = Text(
            title_string,
            font=title_font,
            weight=BOLD,
            font_size=32,
            color="#61D262"
        )

        title.to_edge(UP, buff=0.5)
        title.set_z_index(4)

        self.play(FadeIn(title, shift=UP), run_time=2.0)

        title_bottom = title.get_bottom()[1]
        screen_bottom = -h/2

        available_height = title_bottom - screen_bottom
        grid_offset = 0.5

        center_y_of_grid = screen_bottom + available_height/2 - grid_offset

        v_line_grid = Line([0,title_bottom,0],[0,-h/2,0],stroke_width=1,color=GRAY,stroke_opacity=0.3)
        #h_line_grid = Line([-w/2,center_y_of_grid,0],[0,center_y_of_grid,0],stroke_width=1,color=GRAY,stroke_opacity=0.3)

        grid_lines = VGroup(v_line_grid)
        grid_lines.set_z_index(3)

        self.play(Create(grid_lines), run_time=1.5)

        top_right_anchor = np.array([w/4,(title_bottom+center_y_of_grid)/2,0])

        # ------------------------------------------------
        # LEFT MASK
        # ------------------------------------------------

        left_mask = Rectangle(width=w/2+0.5,height=h,fill_color="#2C3336",fill_opacity=1,stroke_width=0)
        left_mask.move_to([-w/4,0,0])
        left_mask.set_z_index(2)

        self.add(left_mask)

        # ------------------------------------------------
        # IMAGES (DYNAMIC TEMPLATE POSITIONS)
        # ------------------------------------------------

        # User can dynamically add more items to this list, and they will arrange without overlapping.
        image_data_list = [
            {"path": "../images/image_1.png", "scale": 0.5, "label": None},
            {"path": "../images/image_2.png", "scale": 0.35, "label": "₹85.75"},
            {"path": "../images/image_3.png", "scale": 0.25, "label": "₹80.20"},
        ]
        
        gallery_elements = Group()
        
        for i, item in enumerate(image_data_list):
            img = ImageMobject(item["path"]).scale(item["scale"])
            if item.get("label"):
                lbl = Text(item["label"], font=title_font, font_size=18, color="#FFFFFF")
                container = Group(img, lbl).arrange(DOWN, buff=0.2)
            else:
                container = Group(img)
            container.set_z_index(3)
            gallery_elements.add(container)
            
        # Dynamically arrange based on number of items (wrap to next row if more than 2)
        cols = 2 if len(gallery_elements) >= 2 else 1
        gallery_elements.arrange_in_grid(cols=cols, buff=0.5)
        
        # Position in the designated left area
        gallery_elements.move_to([-w/4, (title_bottom+center_y_of_grid)/2, 0])
        
        # Auto-scale to ensure it doesn't overlap or go out of bounds
        max_left_width = w/2 - 1.0
        max_left_height = available_height - 1.0
        
        if gallery_elements.height > max_left_height:
            gallery_elements.scale_to_fit_height(max_left_height)
        if gallery_elements.width > max_left_width:
            gallery_elements.scale_to_fit_width(max_left_width)
            
        # Dynamic rendering
        for el in gallery_elements:
            self.play(FadeIn(el, shift=UP), run_time=0.5)

        self.wait(3.07)

        # ------------------------------------------------
        ## Section 2
        # ------------------------------------------------

        column_heading = Text(
            "Column Subtraction Method",
            font=title_font,
            weight=BOLD,
            font_size=20,
            color="#61D262"
        )

        column_heading.move_to(top_right_anchor + UP*0.8)

        self.play(Write(column_heading), run_time=1.2)

        addend1 = Text("₹85. 75", font=title_font, font_size=20, color="#FFFFFF")
        addend1.move_to(top_right_anchor + RIGHT*0.5 + DOWN*0.2)

        addend2 = Text("₹80. 20", font=title_font, font_size=20, color="#FFFFFF")
        addend2.move_to(top_right_anchor + RIGHT*0.5 + DOWN*0.7)

        self.play(FadeIn(addend1), run_time=1.0)
        self.play(FadeIn(addend2), run_time=1.0)

        horiz_line = Line(
            top_right_anchor + LEFT*0.3 + DOWN*1.0,
            top_right_anchor + RIGHT*1.3 + DOWN*1.0,
        )

        self.play(Create(horiz_line), run_time=1.0)

        self.wait(1.8)

        # ------------------------------------------------
        ## Section 3
        # ------------------------------------------------

        step1_title = wrap_text_dynamic("Step 1: Subtract the Paise!", title_font, 24, w/2 - 1.0)
        step1_desc = wrap_text_dynamic("75 paise - 20 paise = 55 paise", title_font, 18, w/2 - 1.0)
        
        panel1_text = VGroup(step1_title, step1_desc).arrange(DOWN, buff=0.3)

        panel1_text.move_to([w/4,-1.6,0])

        self.play(Write(panel1_text), run_time=1.725)

        paise_rect = SurroundingRectangle(
            VGroup(
                Text("75", font=title_font, font_size=16).move_to(top_right_anchor+RIGHT*0.9+DOWN*0.2),
                Text("20", font=title_font, font_size=16).move_to(top_right_anchor+RIGHT*0.9+DOWN*0.7)
            ),
            buff=0.15,
            color="#EF9515"
        )

        self.play(Indicate(paise_rect), run_time=1.425)

        paise_result = Text("55", font=title_font, font_size=20, color="#FFFFFF")
        paise_result.move_to(top_right_anchor + RIGHT*0.8 + DOWN*1.2)

        self.play(FadeIn(paise_result), run_time=0.725)

        self.wait(2.6)

        self.play(panel1_text.animate.shift(LEFT*w/1.5), run_time=1.025)
        self.remove(panel1_text)

        # ------------------------------------------------
        ## Section 4
        # ------------------------------------------------

        step2_title = wrap_text_dynamic("Step 2: Subtract the Rupees!", title_font, 24, w/2 - 1.0)
        step2_desc = wrap_text_dynamic("85 rupees - 80 rupees = 5 rupees", title_font, 18, w/2 - 1.0)
        
        panel2_text = VGroup(step2_title, step2_desc).arrange(DOWN, buff=0.3)

        panel2_text.move_to([w/4,-1.6,0])

        self.play(Write(panel2_text), run_time=1.758)

        rupee_rect = SurroundingRectangle(
            VGroup(
                Text("85", font=title_font, font_size=16).move_to(top_right_anchor+RIGHT*0.3+DOWN*0.2),
                Text("80", font=title_font, font_size=16).move_to(top_right_anchor+RIGHT*0.3+DOWN*0.7)
            ),
            buff=0.15,
            color="#EF9515"
        )

        self.play(Indicate(rupee_rect), run_time=1.458)

        rupee_result = Text("5.", font=title_font, font_size=20, color="#FFFFFF")
        rupee_result.move_to(top_right_anchor + RIGHT*0.3 + DOWN*1.2)

        self.play(FadeIn(rupee_result), run_time=0.758)

        self.wait(1.462)

        self.play(panel2_text.animate.shift(LEFT*w/1.5), run_time=1.058)
        self.remove(panel2_text)

        # ------------------------------------------------
        ## Section 5
        # ------------------------------------------------

        panel3_text = wrap_text_dynamic(
            "Money Left: ₹5.55",
            title_font,
            32,
            w/2 - 1.0,
            weight=BOLD
        )

        panel3_text.move_to([w/4,-1,0])

        self.play(Write(panel3_text), run_time=1.25)

        total_result = Text("₹5.55", font=title_font, font_size=24, color="#FFFFFF")
        total_result.move_to([w/4,-2.5,0])
        total_result.set_z_index(5)


        self.play(FadeIn(total_result), run_time=1.0)

        total_highlight = SurroundingRectangle(total_result, buff=0.15)
        total_highlight.set_z_index(5)


        self.play(Create(total_highlight), run_time=0.5)
        self.play(total_result.animate.scale(1.2), run_time=0.55)

        self.wait(4.0)

        self.play(panel3_text.animate.shift(LEFT*w/1.5), run_time=0.85)
        self.remove(panel3_text)

        # ------------------------------------------------
        ## Section 6
        # ------------------------------------------------

        fade_out_group = VGroup(
            grid_lines,
            column_heading,
            addend1,
            addend2,
            horiz_line,
            paise_rect,
            rupee_rect,
            paise_result,
            rupee_result
        )

        fade_out_group_2 = gallery_elements

        self.play(fade_out_group.animate.shift(RIGHT*8), run_time=0.5)
        self.play(fade_out_group_2.animate.shift(LEFT*8), run_time=0.5)

        self.play(
            total_result.animate.move_to([0,2.5,0]),
            total_highlight.animate.move_to([0,2.5,0]),
            run_time=1.0
        )

        # ------------------------------------------------
        # FINAL MESSAGE
        # ------------------------------------------------

        confirmation = VGroup(
            Text("Riya has ", font=title_font, font_size=22),
            Text("₹5.55", font=title_font, font_size=22, color="#EF9515"),
            Text(" left!", font=title_font, font_size=22)
        ).arrange(RIGHT, buff=0.05)

        confirmation.move_to([0,1.2,0])
        confirmation.set_z_index(5)


        self.play(FadeIn(confirmation, shift=UP), run_time=1.0)

        self.wait(2.0)

        self.play(
            FadeOut(title),
            FadeOut(total_result),
            FadeOut(total_highlight),
            FadeOut(confirmation),
            run_time=1.0
        )