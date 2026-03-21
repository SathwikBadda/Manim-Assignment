from manim import *

class Asset1(VGroup):
    def __init__(
        self,
        sheet_width=1.2,
        sheet_height=1.6,
        sheet_color=ManimColor("#F5F5F5"),
        line_color=ManimColor("#ed8c32"),
        currency_color=ManimColor("#084993"),
        corner_radius=0.15,
        **kwargs
    ):
        """
        Construct a financial document icon with modular structure.

        Parameters:
            sheet_width (float): Width of document sheet in Manim units (default: 1.2)
            sheet_height (float): Height of document sheet in Manim units (default: 1.6)
            sheet_color (ManimColor): Fill color of sheet (default: light gray #F5F5F5)
            line_color (ManimColor): Color of internal lines (default: Tiger Orange #ed8c32)
            currency_color (ManimColor): Color of currency symbol (default: Steel Azure #084993)
            corner_radius (float): Rounded corner radius for sheet (default: 0.15)
        """
        super().__init__(**kwargs)

        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.sheet_color = sheet_color
        self.line_color = line_color
        self.currency_color = currency_color
        self.corner_radius = corner_radius

        # Initialize exposed structural groups
        self.sheet_base = None
        self.lines_group = None
        self.currency_symbol = None
        self.document_group = None

        self._build_sheet()
        self._build_lines()
        self._build_currency_symbol()
        self._assemble()

    def _build_sheet(self):
        """Build the primary document sheet with a dog-ear fold at top right."""
        w = self.sheet_width
        h = self.sheet_height
        f = 0.25 * w # Fold size
        
        # Base polygon with clipped corner
        self.sheet_base = Polygon(
            [-w/2, -h/2, 0],  # Bottom Left
            [w/2, -h/2, 0],   # Bottom Right
            [w/2, h/2 - f, 0],# Mid Right (before fold)
            [w/2 - f, h/2, 0],# Top Mid (after fold)
            [-w/2, h/2, 0],   # Top Left
            fill_color=self.sheet_color,
            fill_opacity=1,
            stroke_width=2,
            stroke_color=self.line_color
        )
        
        # Triangular fold flap
        self.fold_flap = Polygon(
            [w/2, h/2 - f, 0],
            [w/2 - f, h/2, 0],
            [w/2 - f, h/2 - f, 0],
            fill_color=interpolate_color(self.sheet_color, BLACK, 0.15),
            fill_opacity=1,
            stroke_color=self.line_color,
            stroke_width=2
        )

    def _build_lines(self):
        """Build internal horizontal lines representing text/report rows."""
        self.lines_group = VGroup()

        interior_height = self.sheet_height * 0.8
        interior_width = self.sheet_width * 0.8
        line_spacing = interior_height / 7
        
        start_y = self.sheet_height / 2 - line_spacing * 2.2

        # Lines below the symbol and fold
        for i in range(5):
            line_y = start_y - i * line_spacing
            # Top lines are shorter to leave room for symbol
            l_width = interior_width if i > 1 else interior_width * 0.6
            l_x = 0 if i > 1 else interior_width * 0.2
            
            line = RoundedRectangle(
                width=l_width,
                height=0.04,
                corner_radius=0.02,
                fill_color=self.line_color,
                fill_opacity=0.8,
                stroke_width=0
            ).move_to([l_x, line_y, 0])
            self.lines_group.add(line)

    def _build_currency_symbol(self):
        """Build the currency symbol ($) positioned to avoid the fold."""
        symbol_height = self.sheet_height * 0.25
        symbol_y = self.sheet_height / 2 - symbol_height * 1.0

        self.currency_symbol = Text(
            "$",
            font_size=int(symbol_height * 60),
            color=self.currency_color,
            font="Avenir",
            weight=BOLD
        ).move_to([-self.sheet_width * 0.25, symbol_y, 0])

    def _assemble(self):
        """Assemble all components into the document_group."""
        self.document_group = VGroup(
            self.sheet_base,
            self.lines_group,
            self.currency_symbol,
            self.fold_flap
        )
        self.add(self.document_group)

    def get_sheet(self):
        """Return the sheet base component."""
        return self.sheet_base

    def get_lines_group(self):
        """Return the entire lines group."""
        return self.lines_group

    def get_line(self, index):
        """Return a specific line by index."""
        if 0 <= index < len(self.lines_group):
            return self.lines_group[index]
        raise IndexError(f"Line index {index} out of range")

    def get_currency_symbol(self):
        """Return the currency symbol component."""
        return self.currency_symbol

    def get_document_group(self):
        """Return the master document group."""
        return self.document_group

    def set_line_color(self, color):
        """Set color of all lines."""
        c = ManimColor(color) if isinstance(color, str) else color
        for line in self.lines_group:
            line.set_fill(c, opacity=1)

    def set_currency_symbol_color(self, color):
        """Set color of currency symbol."""
        c = ManimColor(color) if isinstance(color, str) else color
        self.currency_symbol.set_color(c)

    def set_line_widths(self, widths_list):
        """Set widths of individual lines."""
        for i, width in enumerate(widths_list):
            if i < len(self.lines_group):
                self.lines_group[i].width = width