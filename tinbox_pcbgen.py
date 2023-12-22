import math
from enum import Enum, auto
import pcbnew


class PcbGenerator:
    def __init__(self):
        self.board = pcbnew.GetBoard()

    class GenerateRetCodes(Enum):
        OK = auto()
        NOT_OK = auto()
        DIAGONAL_ERR_MIN = auto()
        DIAGONAL_ERR_MAX = auto()
        VALUE_LESS_OR_ZERO = auto()
        MH_TOO_LARGE = auto()

    def generate_pcb(self, width, length, diagonal, mounting_hole):

        if width <= 0 or length <= 0 or diagonal <= 0:
            return self.GenerateRetCodes.VALUE_LESS_OR_ZERO

        if min(width, length) > diagonal:
            return self.GenerateRetCodes.DIAGONAL_ERR_MIN

        theoretical_diagonal = math.sqrt(width ** 2 + length ** 2)
        radius = (theoretical_diagonal - diagonal) / 2

        if radius < 0:
            return self.GenerateRetCodes.DIAGONAL_ERR_MAX

        # Convert width, length, and radius to KiCad's internal units (nanometers)
        width_nm = pcbnew.FromMM(width)
        length_nm = pcbnew.FromMM(length)

        # radius = diagonal
        radius_nm = pcbnew.FromMM(radius)
        rounded_shape = self.draw_rounded_square(width_nm, length_nm, radius_nm, pcbnew.Edge_Cuts)

        # Add/place shape to board
        self.board.Add(rounded_shape)

        # Add optional mounting holes
        if mounting_hole > 0:
            if mounting_hole > radius + 1:
                return self.GenerateRetCodes.MH_TOO_LARGE
            else:
                hole_offset = max(mounting_hole + 2, radius)
                holes = [[hole_offset, hole_offset], [width - hole_offset, hole_offset],
                         [hole_offset, length - hole_offset], [width - hole_offset, length - hole_offset]]

                for hole in holes:
                    hole_shape = self.draw_mounting_hole(mounting_hole, hole[0], hole[1])
                    self.board.Add(hole_shape)

        # Add/place silkscreen if it fits
        if length > 3 and width > 3 and radius > 1:
            clearance_nm = pcbnew.FromMM(1)
            silk_shape = self.draw_rounded_square(width_nm - 2 * clearance_nm, length_nm - 2 * clearance_nm,
                                                  radius_nm - clearance_nm, pcbnew.F_SilkS)
            silk_shape.Move(pcbnew.VECTOR2I(clearance_nm, clearance_nm))
            self.board.Add(silk_shape)

        # Refresh to update the display
        pcbnew.Refresh()
        return self.GenerateRetCodes.OK

    def draw_mounting_hole(self, mounting_hole, pos_x, pos_y):

        mounting_hole_nm = pcbnew.FromMM(mounting_hole)
        pos_x_nm = pcbnew.FromMM(pos_x)
        pos_y_nm = pcbnew.FromMM(pos_y)

        # Create a mounting hole at 0,0
        mh_via = pcbnew.PCB_VIA(self.board)
        mh_via.SetPosition(pcbnew.VECTOR2I(pos_x_nm, pos_y_nm))
        mh_via.SetDrill(mounting_hole_nm)

        return mh_via

    def draw_rounded_square(self, width_nm, length_nm, radius_nm, layer):
        error_max_nm = pcbnew.FromMM(0.01)
        # Create a polygon for the rectangle
        rect_poly = pcbnew.SHAPE_POLY_SET()

        # Define the rectangle corners
        rect_poly.NewOutline()
        rect_poly.Append(pcbnew.VECTOR2I(0, 0))
        rect_poly.Append(pcbnew.VECTOR2I(width_nm, 0))
        rect_poly.Append(pcbnew.VECTOR2I(width_nm, length_nm))
        rect_poly.Append(pcbnew.VECTOR2I(0, length_nm))
        rect_poly.Append(pcbnew.VECTOR2I(0, 0))  # Close the rectangle

        # Apply fillet to all corners
        rounded_poly = pcbnew.SHAPE_POLY_SET(rect_poly.Fillet(radius_nm, error_max_nm))

        # Create a PCB_SHAPE and set it to the polygon shape
        rounded_shape = pcbnew.PCB_SHAPE(self.board)
        rounded_shape.SetLayer(layer)
        rounded_shape.SetShape(pcbnew.SHAPE_T_POLY)
        rounded_shape.SetPolyShape(rounded_poly)

        return rounded_shape
