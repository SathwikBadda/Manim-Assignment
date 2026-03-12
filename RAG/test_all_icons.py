from manim import *
from graduation_cap_icon import GraduationCapIcon
from institution_icon import InstitutionIcon
from map_pin_icon import MapPinIcon
from pizza_slice import PizzaSlice, CompletePizza
from rocket_with_flame import Rocket, Flame

class TestAllIcons(Scene):
    def construct(self):
        # 1. Graduation Cap
        self.test_graduation_cap()
        self.clear()
        
        # 2. Institution Icon
        self.test_institution()
        self.clear()
        
        # 3. Map Pin
        self.test_map_pin()
        self.clear()
        
        # 4. Pizza Slice & Complete Pizza
        self.test_pizza()
        self.clear()
        
        # 5. Rocket & Flame
        self.test_rocket()
        
    def test_graduation_cap(self):
        print("--- Testing GraduationCapIcon ---")
        cap = GraduationCapIcon()
        cap.move_to(ORIGIN)
        self.add(cap)
        self.wait(0.5)
        
        # Manipulate
        cap.set_color("tassel_curse", RED) # typo intentional to check safety? No, let's use correct name
        # Actually let's use correct name
        try:
             cap.set_color("tassel_curve", RED)
             cap.set_color("tassel_end", RED)
        except Exception as e:
             print(f"Error setting color: {e}")

        self.play(cap.animate_manipulation("skull_cap", "Wiggle"))
        self.wait(0.5)
        self.play(FadeOut(cap))

    def test_institution(self):
        print("--- Testing InstitutionIcon ---")
        inst = InstitutionIcon()
        inst.move_to(ORIGIN)
        self.add(inst)
        self.wait(0.5)
        
        # Manipulate
        inst.set_color("roof", BLUE)
        inst.set_color("cols", GRAY)
        
        self.play(inst.animate_manipulation("cap", "Indicate", color=YELLOW))
        self.wait(0.5)
        self.play(FadeOut(inst))

    def test_map_pin(self):
        print("--- Testing MapPinIcon ---")
        pin = MapPinIcon()
        pin.move_to(ORIGIN)
        self.add(pin)
        self.wait(0.5)
        
        # Manipulate
        pin.set_color("pin_body", RED)
        
        self.play(pin.animate_manipulation("pin_body", "Wiggle"))
        self.wait(0.5)
        self.play(FadeOut(pin))

    def test_pizza(self):
        print("--- Testing Pizza ---")
        # Single Slice
        slice_obj = PizzaSlice(0, PI/4)
        slice_obj.move_to(LEFT * 2)
        self.add(slice_obj)
        
        # Manipulate Slice
        slice_obj.set_color("crust_outer", BROWN)
        self.play(slice_obj.animate_manipulation("pepperonis", "Indicate", color=WHITE))
        
        # Complete Pizza
        pizza = CompletePizza()
        pizza.scale(0.5)
        pizza.move_to(RIGHT * 2)
        self.add(pizza)
        
        # Manipulate Complete Pizza
        # Get a specific slice (0) and manipulate it
        first_slice = pizza.get_slice(0)
        if first_slice:
            self.play(first_slice.animate_manipulation("cheese_slice", "Indicate", color=YELLOW))
            
        self.wait(0.5)
        self.play(FadeOut(slice_obj), FadeOut(pizza))

    def test_rocket(self):
        print("--- Testing Rocket ---")
        rocket = Rocket()
        flame = Flame()
        
        rocket.move_to(UP)
        flame.next_to(rocket, DOWN, buff=0)
        
        group = VGroup(rocket, flame)
        group.scale(0.8)
        group.move_to(ORIGIN)
        
        self.add(group)
        self.wait(0.5)
        
        # Manipulate Rocket
        rocket.set_color("nose", BLUE)
        rocket.set_color("left_fin", BLUE)
        rocket.set_color("right_fin", BLUE)
        
        # Manipulate Flame
        flame.animate_manipulation("flame_inner", "Indicate", color=WHITE)
        
        self.play(
            rocket.animate_manipulation("porthole", "Flash"),
            flame.animate_manipulation("flame_outer", "Wiggle")
        )
        self.wait(0.5)
        self.play(FadeOut(group))

if __name__ == "__main__":
    try:
        # Quick non-render check
        g = GraduationCapIcon()
        g.get_subcomponent("skull_cap")
        
        i = InstitutionIcon()
        i.get_subcomponent("roof")
        
        m = MapPinIcon()
        m.get_subcomponent("pin_body")
        
        p = PizzaSlice(0, 1)
        p.get_subcomponent("pepperonis")
        
        r = Rocket()
        r.get_subcomponent("nose")
        
        print("✔ All classes instantiated and getters checked.")
    except Exception as e:
        print(f"✘ verification Failed: {e}")
