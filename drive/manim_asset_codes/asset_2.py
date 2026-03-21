from manim import *

class Asset2(VGroup):
    def __init__(
        self,
        building_width=1.2,
        building_height=1.5,
        num_columns=4,
        column_gap=0.15,
        base_color=ManimColor("#084993"),
        roof_color=ManimColor("#ed8c32"),
        car_body_color=ManimColor("#084993"),
        car_cabin_color=ManimColor("#4e88bc"),
        car_wheel_hub_color=ManimColor("#85c2e0"),
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.building_width = building_width
        self.building_height = building_height
        self.num_columns = num_columns
        self.column_gap = column_gap
        self.base_color = base_color
        self.roof_color = roof_color
        self.car_body_color = car_body_color
        self.car_cabin_color = car_cabin_color
        self.car_wheel_hub_color = car_wheel_hub_color
        
        self.base_group = VGroup()
        self.columns_group = VGroup()
        self.roof_assembly_group = VGroup()
        self.building_group = VGroup()
        self.car_group = VGroup()
        self.left_factory_unit = VGroup()
        self.right_factory_unit = VGroup()
        self.factories_composition_group = VGroup()
        
        self.col_1 = None
        self.col_2 = None
        self.col_3 = None
        self.col_4 = None
        
        self._build_building()
        self._build_car()
        self._assemble_composition()
    
    def _build_building(self):
        """Construct the factory building from base, columns, cap, and roof."""
        
        # Primary base: wide, shallow rectangle
        base_1 = RoundedRectangle(
            width=self.building_width,
            height=self.building_height * 0.08,
            corner_radius=0.02,
            fill_color=self.base_color,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Secondary base: narrower rectangle above primary
        base_2 = RoundedRectangle(
            width=self.building_width * 0.85,
            height=self.building_height * 0.07,
            corner_radius=0.02,
            fill_color=self.base_color,
            fill_opacity=1,
            stroke_width=0
        )
        base_2.next_to(base_1, UP, buff=0)
        
        self.base_group.add(base_1, base_2)
        
        # Vertical columns arranged horizontally
        col_height = self.building_height * 0.45
        col_width = (self.building_width * 0.85 - self.column_gap * (self.num_columns - 1)) / self.num_columns
        
        columns = []
        for i in range(self.num_columns):
            col = RoundedRectangle(
                width=col_width,
                height=col_height,
                corner_radius=0.01,
                fill_color=self.base_color,
                fill_opacity=1,
                stroke_width=0
            )
            columns.append(col)
            setattr(self, f'col_{i+1}', col)
        
        self.columns_group = VGroup(*columns).arrange(RIGHT, buff=self.column_gap)
        self.columns_group.next_to(base_2, UP, buff=0)
        
        # Horizontal cap unifying top
        cap = RoundedRectangle(
            width=self.building_width * 0.85,
            height=self.building_height * 0.06,
            corner_radius=0.01,
            fill_color=self.base_color,
            fill_opacity=1,
            stroke_width=0
        )
        cap.next_to(self.columns_group, UP, buff=0)
        
        # Triangular roof
        cap_left = cap.get_left()
        cap_right = cap.get_right()
        cap_center = cap.get_top()
        roof_apex = cap_center + UP * (self.building_height * 0.25)
        
        roof = Polygon(
            cap_left + LEFT * 0.05,
            roof_apex,
            cap_right + RIGHT * 0.05,
            fill_color=self.roof_color,
            fill_opacity=1,
            stroke_width=0
        )
        
        self.roof_assembly_group.add(cap, roof)
        
        # Master building group
        self.building_group.add(self.base_group, self.columns_group, self.roof_assembly_group)
    
    def _build_car(self):
        """Construct electric car icon with body, cabin, and wheels."""
        
        car_body_width = self.building_width * 0.6
        car_body_height = self.building_height * 0.12
        
        # Main car body
        body = RoundedRectangle(
            width=car_body_width,
            height=car_body_height,
            corner_radius=0.05,
            fill_color=self.car_body_color,
            fill_opacity=1,
            stroke_width=0
        )
        
        # Cabin/windshield area
        cabin = RoundedRectangle(
            width=car_body_width * 0.5,
            height=car_body_height * 0.7,
            corner_radius=0.03,
            fill_color=self.car_cabin_color,
            fill_opacity=1,
            stroke_width=0
        )
        cabin.next_to(body, UP, buff=0.02)
        cabin.shift(RIGHT * car_body_width * 0.1)
        
        # Left wheel
        left_wheel = Circle(
            radius=car_body_height * 0.25,
            fill_color=self.car_body_color,
            fill_opacity=1,
            stroke_width=0
        )
        left_wheel.next_to(body, DOWN, buff=0)
        left_wheel.shift(LEFT * car_body_width * 0.25)
        
        # Left wheel hub
        left_hub = Circle(
            radius=car_body_height * 0.12,
            fill_color=self.car_wheel_hub_color,
            fill_opacity=1,
            stroke_width=0
        )
        left_hub.move_to(left_wheel.get_center())
        
        # Right wheel
        right_wheel = Circle(
            radius=car_body_height * 0.25,
            fill_color=self.car_body_color,
            fill_opacity=1,
            stroke_width=0
        )
        right_wheel.next_to(body, DOWN, buff=0)
        right_wheel.shift(RIGHT * car_body_width * 0.25)
        
        # Right wheel hub
        right_hub = Circle(
            radius=car_body_height * 0.12,
            fill_color=self.car_wheel_hub_color,
            fill_opacity=1,
            stroke_width=0
        )
        right_hub.move_to(right_wheel.get_center())
        
        self.car_group.add(body, cabin, left_wheel, left_hub, right_wheel, right_hub)
    
    def _assemble_composition(self):
        """Assemble left and right factory units and compose them horizontally."""
        
        # Create left factory unit
        left_building = self.building_group.copy()
        left_car = self.car_group.copy()
        left_car.next_to(left_building, DOWN, buff=0.3)
        
        self.left_factory_unit.add(left_building, left_car)
        
        # Create right factory unit
        right_building = self.building_group.copy()
        right_car = self.car_group.copy()
        right_car.next_to(right_building, DOWN, buff=0.3)
        
        self.right_factory_unit.add(right_building, right_car)
        
        # Compose horizontally with spacing
        self.factories_composition_group.add(self.left_factory_unit, self.right_factory_unit)
        self.factories_composition_group.arrange(RIGHT, buff=1.5)
        
        # Add to self
        self.add(self.factories_composition_group)
    
    def get_building(self, side: str):
        """
        Retrieve building group by side.
        side: 'left' or 'right'
        """
        if side.lower() == 'left':
            return self.left_factory_unit[0]
        elif side.lower() == 'right':
            return self.right_factory_unit[0]
        raise ValueError(f"Side must be 'left' or 'right', got {side}")
    
    def get_car(self, side: str):
        """
        Retrieve car group by side.
        side: 'left' or 'right'
        """
        if side.lower() == 'left':
            return self.left_factory_unit[1]
        elif side.lower() == 'right':
            return self.right_factory_unit[1]
        raise ValueError(f"Side must be 'left' or 'right', got {side}")
    
    def set_building_color(self, side: str, base_accent_color, roof_accent_color):
        """
        Update building colors by side.
        side: 'left' or 'right'
        """
        building = self.get_building(side)
        
        # Update base and columns
        for submob in building.get_submobjects():
            if isinstance(submob, VGroup):
                for elem in submob.get_submobjects():
                    if isinstance(elem, VMobject) and elem != building[-1]:
                        elem.set_fill(base_accent_color, opacity=1)
        
        # Update roof separately
        roof = building[-1]
        if isinstance(roof, VGroup):
            roof_polygon = roof[-1]
            if isinstance(roof_polygon, VMobject):
                roof_polygon.set_fill(roof_accent_color, opacity=1)