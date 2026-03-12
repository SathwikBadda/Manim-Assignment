from manim import *
import sys
import os

# Ensure we can import from the Task directory
sys.path.append(os.path.join(os.getcwd(), "Manim-Assignment", "Task"))

from rabbit import Rabbit, Carrot
from egg import Egg, EggShells, Chicken
from evolution import (
    Human, Bicycle, Motorcycle, Car, 
    Boat, Ship, Submarine, 
    Bird, WrightPlane, Airplane, Jet
)

class TestTaskRefactoring(Scene):
    def construct(self):
        # 1. Rabbit & Carrot
        self.test_rabbit_carrot()
        self.clear()
        
        # 2. Egg, Shells, Chicken
        self.test_egg_cycle()
        self.clear()
        
        # 3. Evolution Vehicles
        self.test_evolution_vehicles()
        
    def test_rabbit_carrot(self):
        print("--- Testing Rabbit & Carrot ---")
        rabbit = Rabbit()
        rabbit.scale(0.5).shift(LEFT * 2)
        rabbit.set_color("left_ear_inner", RED) # Manipulation test
        
        carrot = Carrot()
        carrot.scale(0.5).shift(RIGHT * 2)
        carrot.set_color("carrot_body", YELLOW) # Manipulation test
        
        self.add(rabbit, carrot)
        self.wait(0.5)

    def test_egg_cycle(self):
        print("--- Testing Egg Cycle ---")
        egg = Egg()
        egg.scale(0.5).shift(LEFT * 3)
        
        shells = EggShells()
        shells.scale(0.5).shift(LEFT * 1)
        
        chicken = Chicken()
        chicken.scale(0.5).shift(RIGHT * 1)
        chicken.set_color("beak", RED) # Manipulation test
        
        self.add(egg, shells, chicken)
        self.wait(0.5)

    def test_evolution_vehicles(self):
        print("--- Testing Evolution Vehicles ---")
        
        # Group 1
        human = Human().scale(0.5).shift(LEFT*5)
        bike = Bicycle().scale(0.5).shift(LEFT*3)
        moto = Motorcycle().scale(0.5).shift(LEFT*1)
        car = Car().scale(0.5).shift(RIGHT*1)
        
        self.add(human, bike, moto, car)
        self.wait(0.5)
        self.clear()
        
        # Group 2
        boat = Boat().scale(0.5).shift(LEFT*3)
        ship = Ship().scale(0.5).shift(LEFT*1)
        sub = Submarine().scale(0.5).shift(RIGHT*1)
        
        self.add(boat, ship, sub)
        self.wait(0.5)
        self.clear()
        
        # Group 3
        bird = Bird().scale(0.5).shift(LEFT*3)
        wright = WrightPlane().scale(0.5).shift(LEFT*1)
        plane = Airplane().scale(0.5).shift(RIGHT*1)
        jet = Jet().scale(0.5).shift(RIGHT*3)
        
        self.add(bird, wright, plane, jet)
        self.wait(0.5)

if __name__ == "__main__":
    try:
        # Instantiation checks
        r = Rabbit()
        r.get_subcomponent("body")
        c = Carrot()
        c.get_subcomponent("leaves")
        
        e = Egg()
        es = EggShells()
        ch = Chicken()
        
        h = Human()
        b = Bicycle()
        m = Motorcycle()
        ca = Car()
        
        bo = Boat()
        sh = Ship()
        su = Submarine()
        
        bi = Bird()
        wp = WrightPlane()
        ap = Airplane()
        j = Jet()
        
        print("✔ All Task classes instantiated and getters checked.")
    except Exception as e:
        print(f"✘ Verification Failed: {e}")
