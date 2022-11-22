################################################################################
# Copyright (c) 2021 - 2022 Advanced Micro Devices, Inc. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

import os
import sys
import io
from pathlib import Path
import subprocess
import shutil

# OMNIPERF_HOME = Path(__file__).resolve().parent

# OMNIPERF INFO
# PROG = "omniperf"
# SOC_LIST = ["mi50", "mi100", "mi200"]
# DISTRO_MAP = {"platform:el8": "rhel8", "15.3": "sle15sp3", "20.04": "ubuntu20_04"}


class OmniperfCommon():
    def __init__(self):
        self.NAME = "omniperf"
        self.HOME = Path(__file__).resolve().parent
        self.SOC_LIST = ["mi50", "mi100", "mi200"]
        self.DISTRO_MAP = {
            "platform:el8": "rhel8",
            "15.3": "sle15sp3",
            "20.04": "ubuntu20_04",
        }
        self.VERSION = None
        self.SHA = "unknown"
        self.MODE = "unknown"

        self.getVersion()
        return

    def getVersionDisplay(self):
        buf = io.StringIO()
        print("-" * 40, file=buf)
        print("Omniperf version: %s (%s)" % (self.VERSION, self.MODE), file=buf)
        print("Git revision:     %s" % self.SHA, file=buf)
        print("-" * 40, file=buf)
        return buf.getvalue()

    def getVersion(self):
        # symantic version info
        version = os.path.join(OMNIPERF_HOME.parent, "VERSION")
        try:
            with open(version, "r") as file:
                self.VERSION = file.read().replace("\n", "")
        except EnvironmentError:
            print("ERROR: Cannot find VERSION file at {}".format(version))
            sys.exit(1)

        # git version info
        gitDir = os.path.join(OMNIPERF_HOME.parent, ".git")
        if (shutil.which("git") is not None) and os.path.exists(gitDir):
            gitQuery = subprocess.run(
                ["git", "log", "--pretty=format:%h", "-n", "1"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            if gitQuery.returncode == 0:
                self.SHA = gitQuery.stdout.decode("utf-8")
                self.MODE = "dev"
        else:
            shaFile = os.path.join(OMNIPERF_HOME.parent, "VERSION.sha")
            try:
                with open(shaFile, "r") as file:
                    self.SHA = file.read().replace("\n", "")
            except EnvironmentError:
                print("ERROR: Cannot find VERSION.sha file at {}".format(shaFile))
                sys.exit(1)

            self.MODE = "release"
        return