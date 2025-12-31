from manim import *

class BusinessAssetsAnimation(Scene):
    def construct(self):
        # Set modern dark background
        self.camera.background_color = "#0E1117"
        
        # ========================================
        # SCENE TITLE
        # ========================================
        
        title = Text(
            "Business Assets Overview",
            font_size=48,
            color="#FFFFFF",
            weight=BOLD
        )
        title.to_edge(UP, buff=0.8)
        
        # ========================================
        # BUILDING ASSET (LEFT) - BLUE/GRAY
        # ========================================
        
        # Main building structure
        building_base = Rectangle(
            width=2.0,
            height=3.0,
            fill_color="#2C3E50",
            fill_opacity=1,
            stroke_color="#34495E",
            stroke_width=3
        )
        
        # Roof
        roof = Polygon(
            [-1.2, 1.5, 0],
            [1.2, 1.5, 0],
            [0, 2.2, 0],
            fill_color="#34495E",
            fill_opacity=1,
            stroke_color="#4A5F7F",
            stroke_width=3
        )
        
        # Windows (3x3 grid)
        windows = VGroup()
        for row in range(3):
            for col in range(3):
                window = Rectangle(
                    width=0.35,
                    height=0.45,
                    fill_color="#5DADE2",
                    fill_opacity=0.8,
                    stroke_color="#3498DB",
                    stroke_width=2
                )
                x_pos = -0.6 + col * 0.6
                y_pos = 0.8 - row * 0.8
                window.move_to([x_pos, y_pos, 0])
                windows.add(window)
        
        # Door
        door = Rectangle(
            width=0.5,
            height=0.8,
            fill_color="#8B4513",
            fill_opacity=1,
            stroke_color="#654321",
            stroke_width=2
        )
        door.move_to([0, -1.1, 0])
        
        # Building shadow for depth
        building_shadow = Rectangle(
            width=2.1,
            height=3.1,
            fill_color="#000000",
            fill_opacity=0,
            stroke_color="#2C3E50",
            stroke_width=10,
            stroke_opacity=0.3
        )
        
        # Group building components
        building = VGroup(
            building_shadow,
            building_base,
            roof,
            windows,
            door
        )
        building.scale(0.8)
        building.shift(LEFT * 4)
        
        # Building label
        building_label = Text(
            "Building",
            font_size=28,
            color="#5DADE2",
            weight=BOLD
        )
        building_label.next_to(building, DOWN, buff=0.5)
        
        # ========================================
        # INVENTORY ASSET (CENTER) - ORANGE/YELLOW
        # ========================================
        
        # Create stacked boxes
        boxes = VGroup()
        box_colors = ["#FF6B35", "#FF8C42", "#FFA559"]
        
        # Bottom box (largest)
        box1 = VGroup()
        box1_main = Rectangle(
            width=2.2,
            height=0.9,
            fill_color=box_colors[0],
            fill_opacity=1,
            stroke_color="#E55934",
            stroke_width=3
        )
        # Box details (tape/lines)
        box1_line = Line(LEFT * 1.1, RIGHT * 1.1, color="#D64933", stroke_width=2)
        box1_line.move_to(box1_main.get_center())
        box1.add(box1_main, box1_line)
        box1.shift(DOWN * 1.2)
        
        # Middle box
        box2 = VGroup()
        box2_main = Rectangle(
            width=1.8,
            height=0.8,
            fill_color=box_colors[1],
            fill_opacity=1,
            stroke_color="#E67A3C",
            stroke_width=3
        )
        box2_line = Line(LEFT * 0.9, RIGHT * 0.9, color="#D66A2C", stroke_width=2)
        box2_line.move_to(box2_main.get_center())
        box2.add(box2_main, box2_line)
        box2.shift(DOWN * 0.35)
        
        # Top box (smallest)
        box3 = VGroup()
        box3_main = Rectangle(
            width=1.4,
            height=0.7,
            fill_color=box_colors[2],
            fill_opacity=1,
            stroke_color="#E89050",
            stroke_width=3
        )
        box3_line = Line(LEFT * 0.7, RIGHT * 0.7, color="#D68040", stroke_width=2)
        box3_line.move_to(box3_main.get_center())
        box3.add(box3_main, box3_line)
        box3.shift(UP * 0.4)
        
        # Pallet base
        pallet = Rectangle(
            width=2.5,
            height=0.2,
            fill_color="#8B4513",
            fill_opacity=1,
            stroke_color="#654321",
            stroke_width=2
        )
        pallet.shift(DOWN * 1.7)
        
        # Group inventory components
        inventory = VGroup(pallet, box1, box2, box3)
        inventory.scale(0.9)
        inventory.shift(UP * 0.3)
        
        # Inventory shadow
        inventory_shadow = Rectangle(
            width=2.6,
            height=3.5,
            fill_color="#000000",
            fill_opacity=0,
            stroke_color="#FF6B35",
            stroke_width=10,
            stroke_opacity=0.3
        )
        inventory_shadow.move_to(inventory.get_center())
        
        # Inventory label
        inventory_label = Text(
            "Inventory",
            font_size=28,
            color="#FF8C42",
            weight=BOLD
        )
        inventory_label.next_to(inventory, DOWN, buff=0.5)
        
        # ========================================
        # CASH ASSET (RIGHT) - GREEN/GOLD
        # ========================================
        
        # Money stack base
        money_stack = VGroup()
        
        # Create stacked bills
        for i in range(5):
            bill = Rectangle(
                width=2.0,
                height=0.25,
                fill_color="#27AE60",
                fill_opacity=1,
                stroke_color="#229954",
                stroke_width=2
            )
            bill.shift(UP * (i * 0.15 - 0.3))
            
            # Dollar sign on bill
            dollar = Text(
                "$",
                font_size=20,
                color="#F4D03F",
                weight=BOLD
            )
            dollar.move_to(bill.get_center())
            
            money_stack.add(bill, dollar)
        
        # Coins (circular shapes)
        coins = VGroup()
        coin_positions = [
            [0.8, 0.5, 0],
            [0.5, 0.8, 0],
            [-0.6, 0.6, 0],
            [-0.8, 0.3, 0]
        ]
        
        for pos in coin_positions:
            coin = Circle(
                radius=0.25,
                fill_color="#F4D03F",
                fill_opacity=1,
                stroke_color="#F39C12",
                stroke_width=3
            )
            coin.move_to(pos)
            
            # Coin inner circle
            coin_inner = Circle(
                radius=0.18,
                fill_color="#000000",
                fill_opacity=0,
                stroke_color="#F39C12",
                stroke_width=2
            )
            coin_inner.move_to(pos)
            
            coins.add(coin, coin_inner)
        
        # Currency symbol
        currency_symbol = Text(
            "$",
            font_size=60,
            color="#F4D03F",
            weight=BOLD
        )
        currency_symbol.move_to([0, -1.2, 0])
        
        # Group cash components
        cash = VGroup(money_stack, coins, currency_symbol)
        cash.scale(0.8)
        cash.shift(RIGHT * 4)
        
        # Cash glow effect
        cash_glow = Circle(
            radius=2.0,
            fill_color="#000000",
            fill_opacity=0,
            stroke_color="#27AE60",
            stroke_width=15,
            stroke_opacity=0.3
        )
        cash_glow.move_to(cash.get_center())
        
        # Cash label
        cash_label = Text(
            "Cash",
            font_size=28,
            color="#27AE60",
            weight=BOLD
        )
        cash_label.next_to(cash, DOWN, buff=0.5)
        
        # ========================================
        # SEPARATOR ARROWS (OPTIONAL VISUAL GUIDES)
        # ========================================
        
        arrow1 = Arrow(
            start=building.get_right() + RIGHT * 0.3,
            end=inventory.get_left() + LEFT * 0.3,
            color="#7F8C8D",
            stroke_width=3,
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        arrow2 = Arrow(
            start=inventory.get_right() + RIGHT * 0.3,
            end=cash.get_left() + LEFT * 0.3,
            color="#7F8C8D",
            stroke_width=3,
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        arrows = VGroup(arrow1, arrow2)
        
        # ========================================
        # ANIMATION SEQUENCE
        # ========================================
        
        # 1. Title fade in
        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            run_time=1.2
        )
        self.wait(0.5)
        
        # 2. Building appears with grow effect
        self.play(
            FadeIn(building_shadow),
            GrowFromCenter(building_base),
            FadeIn(roof, shift=DOWN * 0.3),
            run_time=1.0
        )
        self.play(
            LaggedStart(*[FadeIn(window, scale=0.5) for window in windows], lag_ratio=0.1),
            FadeIn(door, shift=UP * 0.2),
            run_time=0.8
        )
        self.play(
            Write(building_label),
            run_time=0.6
        )
        self.wait(0.3)
        
        # 3. Inventory appears with stacking animation
        self.play(
            FadeIn(inventory_shadow),
            FadeIn(pallet, shift=UP * 0.2),
            run_time=0.5
        )
        self.play(
            box1.animate.shift(DOWN * 0.5).scale(1.1).scale(1/1.1),
            run_time=0.4
        )
        self.play(
            box2.animate.shift(DOWN * 0.5).scale(1.1).scale(1/1.1),
            run_time=0.4
        )
        self.play(
            box3.animate.shift(DOWN * 0.5).scale(1.1).scale(1/1.1),
            run_time=0.4
        )
        self.play(
            Write(inventory_label),
            run_time=0.6
        )
        self.wait(0.3)
        
        # 4. Cash appears with bounce and glow
        self.play(
            FadeIn(cash_glow),
            run_time=0.3
        )
        self.play(
            FadeIn(money_stack, shift=UP * 0.3, scale=0.8),
            run_time=0.6
        )
        self.play(
            LaggedStart(*[GrowFromCenter(coin) for coin in [coins[i] for i in range(0, len(coins), 2)]], lag_ratio=0.15),
            run_time=0.8
        )
        self.play(
            DrawBorderThenFill(currency_symbol),
            run_time=0.7
        )
        self.play(
            Write(cash_label),
            run_time=0.6
        )
        
        # 5. Add connecting arrows
        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            run_time=1.0
        )
        
        # 6. Subtle pulsing effect on cash to show liquidity
        self.play(
            cash_glow.animate.scale(1.2).set_stroke(opacity=0.5),
            rate_func=there_and_back,
            run_time=1.0
        )
        
        # Final pause
        self.wait(1.5)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in [
                title, building, building_label, building_shadow,
                inventory, inventory_label, inventory_shadow,
                cash, cash_label, cash_glow, arrows
            ]],
            run_time=1.0
        )
        
        self.wait(0.5)