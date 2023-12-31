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
import wx
import pcbnew
from .tinbox_pcbgen import PcbGenerator
from .tinbox_mpgen import MountingPadGenerator


def _get_image_path():
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tinbox_measure.png")
    return image_path


def _get_default_units():
    # For KiCad Version 7 and later
    units = pcbnew.GetUserUnits()
    return "mm" if units == pcbnew.EDA_UNITS_MILLIMETRES else "in."


class TinboxDialog(wx.Dialog):
    def __init__(self, parent, title, icon_path, image_path):
        super(TinboxDialog, self).__init__(parent, title=title)

        self.SetIcon(wx.Icon(icon_path))
        self.panel = wx.Panel(self)

        # Using GridBagSizer for layout
        self.layout = wx.GridBagSizer(5, 5)

        # Load and display the image
        self.image = wx.Image(image_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.image_ctrl = wx.StaticBitmap(self.panel, wx.ID_ANY, self.image)
        self.layout.Add(self.image_ctrl, pos=(0, 0), span=(1, 3), flag=wx.ALL | wx.CENTER, border=5)

        # Get the default units
        self.unit_label = _get_default_units()
        # Create input fields
        self.width_txt = self.create_input_field("Width:", 1, self.unit_label)
        self.length_txt = self.create_input_field("Length:", 2, self.unit_label)
        self.diagonal_txt = self.create_input_field("Diagonal:", 3, self.unit_label)
        self.clearance_txt = self.create_input_field("Clearance:", 4,
                                                     "thou" if self.unit_label != "mm" else self.unit_label)
        self.wall_thickness_txt = self.create_input_field("Wall thickness:", 5,
                                                          "thou" if self.unit_label != "mm" else self.unit_label)
        self.mounting_hole_txt = self.create_input_field("Hole dia.:", 6,
                                                         "thou" if self.unit_label != "mm" else self.unit_label)

        # Static text label and checkbox for "Generate Mounting pad"
        self.generate_mounting_pad_label = wx.StaticText(self.panel, label="Generate mounting pad")
        self.generate_mounting_pad_chk = wx.CheckBox(self.panel)

        self.layout.Add(self.generate_mounting_pad_label, pos=(7, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.layout.Add(self.generate_mounting_pad_chk, pos=(7, 1), flag=wx.ALL, border=5)

        # Generate Button
        self.generate_btn = wx.Button(self.panel, label="Generate")
        self.layout.Add(self.generate_btn, pos=(8, 0), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=5)

        self.panel.SetSizer(self.layout)
        self.layout.Fit(self.panel)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.on_generate, self.generate_btn)

    def create_input_field(self, label, row, unit_label):
        lbl = wx.StaticText(self.panel, label=label)
        txt = wx.TextCtrl(self.panel)
        unit_lbl = wx.StaticText(self.panel, label=unit_label)

        self.layout.Add(lbl, pos=(row, 0), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=15)
        self.layout.Add(txt, pos=(row, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.layout.Add(unit_lbl, pos=(row, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        return txt  # Return the TextCtrl object

    def on_generate(self, event):
        try:
            width = float(self.width_txt.GetValue())
            length = float(self.length_txt.GetValue())
            diagonal = float(self.diagonal_txt.GetValue())
            mounting_hole = float(self.mounting_hole_txt.GetValue())
            clearance = float(self.clearance_txt.GetValue())
            thickness = float(self.wall_thickness_txt.GetValue())
            if self.unit_label != "mm":
                width = width * 25.4
                length = length * 25.4
                diagonal = diagonal * 25.4
                mounting_hole = mounting_hole * 0.0254
                clearance = clearance * 0.0254

            pcb_generator = PcbGenerator()

            # Process the valid values as needed
            result = pcb_generator.generate(width, length, diagonal, clearance, mounting_hole)

            if result == pcb_generator.GeneratorRetCodes.VALUE_LESS_OR_ZERO:
                wx.MessageBox('All values must be numbers greater than zero.', 'Invalid Input', wx.OK | wx.ICON_ERROR)
                return
            elif result == pcb_generator.GeneratorRetCodes.DIAGONAL_ERR_MAX:
                wx.MessageBox('Diagonal is larger than theoretical maximum', 'Invalid Input', wx.OK | wx.ICON_ERROR)
                return
            elif result == pcb_generator.GeneratorRetCodes.DIAGONAL_ERR_MIN:
                wx.MessageBox('Diagonal is smaller than theoretical minimum', 'Invalid Input', wx.OK | wx.ICON_ERROR)
                return
            elif result == pcb_generator.GeneratorRetCodes.MH_TOO_LARGE:
                wx.MessageBox('Mounting hole ' + str(mounting_hole) + 'mm is too large for default location',
                              'Invalid Input', wx.OK | wx.ICON_ERROR)
                return

            elif result == pcb_generator.GeneratorRetCodes.CLEARANCE_TOO_LARGE:
                wx.MessageBox('Clearance value ' + str(clearance) + 'mm is larger than box size.',
                              'Invalid Input', wx.OK | wx.ICON_ERROR)
                return

            # elif result == pcb_generator.GeneratorRetCodes.THICKNESS_TOO_LARGE:
            #     wx.MessageBox('Thickness value ' + str(clearance) + 'mm is larger than box size.',
            #                   'Invalid Input', wx.OK | wx.ICON_ERROR)
            #     return
            mh_dist = pcb_generator.get_mh_distance()
            if self.generate_mounting_pad_chk.IsChecked() and mounting_hole > 0 and mh_dist is not None:
                mounting_pad_generator = MountingPadGenerator()
                mp_config = mounting_pad_generator.generate(width, length, diagonal, thickness, mounting_hole, mh_dist)
                mounting_pad_generator.copy_openscad_model(mp_config)

            self.Close()
        except ValueError:
            wx.MessageBox('Please enter valid numeric values.', 'Invalid Input', wx.OK | wx.ICON_ERROR)


def run_tinbox(iconpath):
    app = wx.App(False)
    dialog = TinboxDialog(None, title="Tinbox", icon_path=iconpath, image_path=_get_image_path())
    dialog.ShowModal()
    dialog.Destroy()
    app.MainLoop()
