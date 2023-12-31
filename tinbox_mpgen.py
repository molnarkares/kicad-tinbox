# Copyright (c) 2023 Karoly Molnar
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import math
from enum import Enum, auto
import pcbnew
import shutil
from collections import namedtuple


def _get_model_path():
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mounting_pad.scad")
    return model_path


class MountingPadGenerator:
    def __init__(self):
        self.board = pcbnew.GetBoard()

    class GeneratorRetCodes(Enum):
        OK = auto()
        NOT_OK = auto()
        DIAGONAL_ERR_MIN = auto()
        DIAGONAL_ERR_MAX = auto()
        VALUE_LESS_OR_ZERO = auto()
        MH_TOO_LARGE = auto()
        CLEARANCE_TOO_LARGE = auto()

    def generate(self, p_width, p_length, diagonal, p_thickness, mounting_hole, mh_dist):
        mh_drill = mounting_hole * 0.9
        width = p_width - 2 * (p_thickness + 0.3)
        length = p_length - 2 * (p_thickness + 0.3)
        mh_distance = mh_dist - (p_thickness + 0.3)

        diagonal = diagonal - 2 * (p_thickness + 0.3)
        theoretical_diagonal = math.sqrt(width ** 2 + length ** 2)
        radius = (theoretical_diagonal - diagonal) / 2

        thickness = max(3, mounting_hole)

        c_height = thickness * 2

        MountingPad = namedtuple("MountingPad",
                                 "width depth radius thickness c_height mh_distance mh_drill")
        mounting_pad = MountingPad(width, length, radius, thickness, c_height, mh_distance, mh_drill)
        return mounting_pad

    def copy_openscad_model(self, mount_pad_config):
        # Get the full path of the current board file
        board_file_path = self.board.GetFileName()
        # Extract the directory from the full path
        project_directory = os.path.dirname(board_file_path)

        pcb_file_name = os.path.basename(board_file_path)

        # Change the file extension to .scad
        scad_model_name = os.path.splitext(pcb_file_name)[0] + "_mount.scad"
        scad_config_name = "mounting_pad_cfg.scad"

        # Define the full path for the new .scad file
        scad_model_path = os.path.join(project_directory, scad_model_name)
        scad_config_path = os.path.join(project_directory, scad_config_name)

        lines = []
        for field in mount_pad_config._fields:
            value = getattr(mount_pad_config, field)
            # Format the value if it's a float
            if isinstance(value, float):
                formatted_value = "{:.2f}".format(value)
            else:
                formatted_value = value
            line = f"{field} = {formatted_value};"
            lines.append(line)

        serialized_data = "\n".join(lines)

        try:
            shutil.copyfile(_get_model_path(), scad_model_path)
            with open(scad_config_path, 'w') as file:
                file.write(serialized_data)
                return True
        except IOError:
            return False
