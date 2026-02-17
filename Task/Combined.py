from manim import *
import numpy as np

class EducationMasterAnimation(Scene):
    def construct(self):

        
        title = Text("Visualizing Science with Manim", font_size=48)
        self.play(Write(title))
        self.play(Indicate(title))
        self.wait()
        self.play(Unwrite(title))

        
        math_title = Text("Mathematics", color=BLUE).to_edge(UP)
        self.play(AddTextLetterByLetter(math_title))

        square = Square()
        circle = Circle()

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(ClockwiseTransform(circle, Square()))
        self.play(CounterclockwiseTransform(square, Circle()))
        self.play(Circumscribe(circle))
        self.play(Uncreate(circle))
        self.play(RemoveTextLetterByLetter(math_title))

        physics_title = Text("Physics", color=GREEN).to_edge(UP)
        self.play(FadeIn(physics_title))

        arrow = Arrow(LEFT, RIGHT)
        self.play(GrowArrow(arrow))

        dot = Dot(color=YELLOW)
        path = TracedPath(dot.get_center, stroke_width=3)
        self.add(path, dot)

        angle = 0
        def spiral(m, dt):
            nonlocal angle
            angle += 3 * dt
            r = 0.05 * angle
            m.move_to([r*np.cos(angle), r*np.sin(angle), 0])

        dot.add_updater(spiral)
        self.wait(4)
        dot.remove_updater(spiral)

        self.play(Flash(dot))
        self.play(FadeOut(physics_title))
        self.remove(arrow, dot, path)

    
        chem_title = Text("Chemistry", color=RED).to_edge(UP)
        self.play(SpinInFromNothing(chem_title))

        molecule = VGroup(
            Circle(radius=0.3),
            Circle(radius=0.3).shift(RIGHT),
            Line(ORIGIN, RIGHT)
        )

        self.play(DrawBorderThenFill(molecule))
        self.play(ApplyWave(molecule))
        self.play(FocusOn(molecule))

        
        boundary = AnimatedBoundary(molecule)
        self.add(boundary)
        self.wait(3)
        self.remove(boundary)

        self.play(FadeOut(chem_title))
        self.remove(molecule)

       
        cs_title = Text("Computer Science", color=YELLOW).to_edge(UP)
        self.play(GrowFromCenter(cs_title))

        boxes = Group(
            Square().shift(LEFT * 3),
            Square(),
            Square().shift(RIGHT * 3)
        )

        self.play(ShowIncreasingSubsets(boxes))
        self.play(ShowSubmobjectsOneByOne(boxes))
        self.play(CyclicReplace(*boxes))
        self.play(ShowPassingFlash(boxes[0].copy()))

        self.play(FadeOut(cs_title))
        self.remove(*boxes)

        
        outro = Text("One Engine. Many Subjects.", font_size=42)
        self.play(GrowFromEdge(outro, DOWN))
        self.play(Wiggle(outro))
        self.wait(2)
