import os

import pcbnew
from pcbnew import ActionPlugin
from .tinbox_ui import run_tinbox
import sys


def _get_icon_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")


class TinboxPlugin(ActionPlugin):
    def defaults(self):
        self.name = "Tinbox PCB generator"
        self.category = "Tinbox PCB"
        self.description = "PCB generator for tin boxes"
        self.icon_file_name = _get_icon_path()

    def Run(self):
        run_tinbox(self.icon_file_name)
