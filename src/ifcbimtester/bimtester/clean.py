# BIMTester - OpenBIM Auditing Tool
# Copyright (C) 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BIMTester.
#
# BIMTester is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BIMTester is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with BIMTester.  If not, see <http://www.gnu.org/licenses/>.

import ifcopenshell
import os
from pathlib import Path


class TestPurger:
    def __init__(self):
        self.file = None

    def purge(self):
        filenames = []
        if os.path.exists("features"):
            for filename in Path("features/").glob("*.feature"):
                filenames.append(filename)
        for f in os.listdir("."):
            if f.endswith(".feature"):
                filenames.append(f)

        for filename in filenames:
            with open(filename, "r") as feature_file:
                old_file = feature_file.readlines()
            with open(filename, "w") as new_file:
                for line in old_file:
                    is_purged = False
                    if 'The IFC file "' in line and '" must be provided' in line:
                        filename = line.split('"')[1]
                        print("Loading file {} ...".format(filename))
                        self.file = ifcopenshell.open(filename)
                    if line.strip()[0:2] == "* ":
                        words = line.strip().split()
                        for word in words:
                            if self.is_a_global_id(word):
                                if not self.does_global_id_exist(word):
                                    print("Test for {} purged ...".format(word))
                                    is_purged = True
                    if not is_purged:
                        new_file.write(line)

    def is_a_global_id(self, word):
        return word[0] in ["0", "1", "2", "3"] and len(word) == 22

    def does_global_id_exist(self, global_id):
        try:
            self.file.by_guid(global_id)
            return True
        except Exception:
            return False
