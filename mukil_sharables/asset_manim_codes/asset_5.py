from manim import *
import numpy as np


class Asset5(VGroup):
    """
    4C Heatmaps asset: A semantically-layered grid structure with cells,
    headers, row labels, and color intensity mapping.
    
    Exposes internal structure for animation:
    - cells_group: all cell mobjects in row-major order
    - row_groups: list of VGroups, one per row
    - header_group: column labels
    - row_labels_group: row identifiers
    - grid_container: unified cell matrix + headers + row labels
    - heatmap_master_group: frame + grid_container
    - frame: outer boundary rectangle
    """
    
    def __init__(
        self,
        rows=4,
        cols=4,
        cell_width=0.6,
        cell_height=0.6,
        header_labels=None,
        row_labels=None,
        color_data=None,
        header_font_size=14,
        row_label_font_size=14,
        cell_text_font_size=12,
        frame_stroke_width=1.5,
        **kwargs
    ):
        """
        Initialize the 4C Heatmaps asset.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            cell_width: Width of each cell
            cell_height: Height of each cell
            header_labels: List of column header labels (default: None)
            row_labels: List of row labels (default: None)
            color_data: Dict mapping (row, col) to intensity [0, 1] (default: None)
            header_font_size: Font size for headers
            row_label_font_size: Font size for row labels
            cell_text_font_size: Font size for cell text
            frame_stroke_width: Stroke width of outer frame
        """
        super().__init__(**kwargs)
        
        self.rows = rows
        self.cols = cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.header_font_size = header_font_size
        self.row_label_font_size = row_label_font_size
        self.cell_text_font_size = cell_text_font_size
        
        # Color scheme
        self.color_low = ManimColor("#C6C7DC")      # Primary Text (low intensity)
        self.color_high = ManimColor("#F97316")     # Primary Shape Accent (high intensity)
        self.color_label = ManimColor("#A5B4FC")    # Secondary Text
        self.color_frame = ManimColor("#F97316")    # Primary Shape Accent
        
        # Pre-computed color intensity mapping
        self.color_data = color_data if color_data else {}
        
        # Initialize header and row labels
        self.header_labels = header_labels if header_labels else [f"Col {i}" for i in range(cols)]
        self.row_labels = row_labels if row_labels else [f"Row {i}" for i in range(rows)]
        
        # Build cell matrix
        self.cells_group = VGroup()
        self.row_groups = []
        self._build_cells()
        
        # Build headers and row labels
        self.header_group = VGroup()
        self.row_labels_group = VGroup()
        self._build_labels()
        
        # Container for grid + labels
        self.grid_container = VGroup(
            self.cells_group,
            self.header_group,
            self.row_labels_group
        )
        
        # Outer frame
        grid_width = self.cols * self.cell_width
        grid_height = self.rows * self.cell_height
        self.frame = Rectangle(
            width=grid_width,
            height=grid_height,
            stroke_color=self.color_frame,
            stroke_width=frame_stroke_width,
            fill_opacity=0
        )
        self.frame.move_to(self.cells_group.get_center())
        
        # Master group
        self.heatmap_master_group = VGroup(self.frame, self.grid_container)
        
        # Add all to self
        self.add(self.heatmap_master_group)
    
    def _build_cells(self):
        """Build the cell grid in row-major order."""
        for row in range(self.rows):
            row_group = VGroup()
            for col in range(self.cols):
                # Determine cell color based on intensity mapping
                intensity = self.color_data.get((row, col), 0.5)
                cell_color = self._interpolate_color(intensity)
                
                # Cell body (filled rectangle)
                cell_rect = Rectangle(
                    width=self.cell_width,
                    height=self.cell_height,
                    fill_color=cell_color,
                    fill_opacity=1,
                    stroke_width=0
                )
                
                # Cell text (optional annotation)
                cell_text = Text(
                    "",
                    font_size=self.cell_text_font_size,
                    color=self.color_label,
                    font="Times New Roman"
                )
                cell_text.move_to(cell_rect.get_center())
                
                # Cell as VGroup
                cell = VGroup(cell_rect, cell_text)
                cell.rect = cell_rect
                cell.text = cell_text
                
                # Position cell
                x_pos = col * self.cell_width - (self.cols - 1) * self.cell_width / 2
                y_pos = (self.rows - 1) * self.cell_height / 2 - row * self.cell_height
                cell.move_to(np.array([x_pos, y_pos, 0]))
                
                row_group.add(cell)
                self.cells_group.add(cell)
            
            self.row_groups.append(row_group)
        
        # Align columns by enforcing x-coordinates
        for col in range(self.cols):
            col_x = self.row_groups[0][col].get_center()[0]
            for row in range(self.rows):
                cell_center = self.row_groups[row][col].get_center()
                self.row_groups[row][col].move_to(np.array([col_x, cell_center[1], 0]))
    
    def _interpolate_color(self, intensity):
        """
        Interpolate color between low and high based on intensity [0, 1].
        
        Args:
            intensity: Float between 0 and 1
            
        Returns:
            ManimColor interpolated between color_low and color_high
        """
        return interpolate_color(self.color_low, self.color_high, intensity)
    
    def _build_labels(self):
        """Build header and row label groups."""
        # Header labels (above columns)
        for col in range(self.cols):
            col_center_x = self.row_groups[0][col].get_center()[0]
            header_text = Text(
                self.header_labels[col],
                font_size=self.header_font_size,
                color=self.color_label,
                font="Times New Roman"
            )
            header_text.move_to(np.array([
                col_center_x,
                self.cells_group.get_top()[1] + 0.3,
                0
            ]))
            self.header_group.add(header_text)
        
        # Row labels (left of rows)
        for row in range(self.rows):
            row_center_y = self.row_groups[row][0].get_center()[1]
            row_label_text = Text(
                self.row_labels[row],
                font_size=self.row_label_font_size,
                color=self.color_label,
                font="Times New Roman"
            )
            row_label_text.move_to(np.array([
                self.cells_group.get_left()[0] - 0.5,
                row_center_y,
                0
            ]))
            self.row_labels_group.add(row_label_text)
    
    def get_cell(self, row, col):
        """
        Access a specific cell by row and column indices.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            VGroup representing the cell
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.row_groups[row][col]
        return None
    
    def get_row(self, row_index):
        """
        Access all cells in a specific row.
        
        Args:
            row_index: Row index
            
        Returns:
            VGroup containing all cells in the row
        """
        if 0 <= row_index < self.rows:
            return self.row_groups[row_index]
        return None
    
    def get_column(self, col_index):
        """
        Access all cells in a specific column.
        
        Args:
            col_index: Column index
            
        Returns:
            VGroup containing all cells in the column
        """
        if 0 <= col_index < self.cols:
            col_cells = VGroup(*[self.row_groups[row][col_index] for row in range(self.rows)])
            return col_cells
        return None
    
    def set_cell_color(self, row, col, intensity):
        """
        Update the color of a specific cell based on intensity.
        
        Args:
            row: Row index
            col: Column index
            intensity: Float between 0 and 1
        """
        cell = self.get_cell(row, col)
        if cell:
            new_color = self._interpolate_color(intensity)
            cell.rect.set_fill(new_color, opacity=1)
            self.color_data[(row, col)] = intensity
    
    def set_cell_text(self, row, col, text):
        """
        Update the text annotation in a specific cell.
        
        Args:
            row: Row index
            col: Column index
            text: Text string to display
        """
        cell = self.get_cell(row, col)
        if cell:
            new_text = Text(
                text,
                font_size=self.cell_text_font_size,
                color=self.color_label,
                font="Times New Roman"
            )
            new_text.move_to(cell.rect.get_center())
            cell.remove(cell.text)
            cell.add(new_text)
            cell.text = new_text
    
    def highlight_cell(self, row, col, highlight_color=None):
        """
        Highlight a specific cell with a color.
        
        Args:
            row: Row index
            col: Column index
            highlight_color: Color to highlight with (default: bright accent)
            
        Returns:
            Animation object for highlighting
        """
        cell = self.get_cell(row, col)
        if cell:
            color = highlight_color if highlight_color else ManimColor("#FFD700")
            return Indicate(cell, color=color)
        return Wait(0)
    
    def animate_cell_color_change(self, row, col, target_intensity, run_time=0.5):
        """
        Animation helper: smoothly transition cell color to target intensity.
        
        Args:
            row: Row index
            col: Column index
            target_intensity: Target intensity [0, 1]
            run_time: Animation duration
            
        Returns:
            Animation object
        """
        cell = self.get_cell(row, col)
        if not cell:
            return Wait(0)
        
        start_intensity = self.color_data.get((row, col), 0.5)
        
        def update_func(m, alpha):
            intensity = interpolate(start_intensity, target_intensity, alpha)
            self.set_cell_color(row, col, intensity)
        
        return UpdateFromAlphaFunc(self, update_func, run_time=run_time)
    
    def animate_row_color_wave(self, row_index, target_intensity, stagger_time=0.1, run_time=0.5):
        """
        Animation helper: animate all cells in a row with staggered color changes.
        
        Args:
            row_index: Row index
            target_intensity: Target intensity [0, 1]
            stagger_time: Delay between column animations
            run_time: Duration per column animation
            
        Returns:
            Animation sequence
        """
        anims = []
        for col in range(self.cols):
            anim = self.animate_cell_color_change(row_index, col, target_intensity, run_time=run_time)
            anims.append(anim)
        
        return stagger(*anims, lag_ratio=stagger_time / run_time)