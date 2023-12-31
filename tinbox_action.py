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
