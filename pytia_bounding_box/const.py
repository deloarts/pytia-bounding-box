"""
    Constants for the pytia bounding box app.
"""

from __future__ import annotations

import os
from enum import Enum

__version__ = "0.1.0"

PYTIA = "pytia"
PYTIA_BOUNDING_BOX = "pytia_bounding_box"

APP_NAME = "PYTIA Bounding Box"
APP_VERSION = __version__

CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
APPDATA = f"{str(os.environ.get('APPDATA'))}\\{PYTIA}\\{PYTIA_BOUNDING_BOX}"
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = VENV + "\\Scripts\\python.exe"
VENV_PYTHONW = VENV + "\\Scripts\\pythonw.exe"
PY_VERSION = APPDATA + "\\pyversion.txt"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_DEPS_DEFAULT = "dependencies.default.json"
CONFIG_PROPS = "properties.json"
CONFIG_PROPS_DEFAULT = "properties.default.json"
CONFIG_PRESETS = "presets.json"
CONFIG_PRESETS_DEFAULT = "presets.default.json"
CONFIG_PROCESSES = "processes.json"
CONFIG_PROCESSES_DEFAULT = "processes.default.json"
CONFIG_INFOS = "information.json"
CONFIG_INFOS_DEFAULT = "information.default.json"
CONFIG_USERS = "users.json"

WEB_PIP = "www.pypi.org"


class Preference(Enum):
    """Enum class for preference settings."""

    MIN = "min"
    MAX = "max"
    AXIS = "axis"


class Axes(Enum):
    """Enum class for axes."""

    X = "X-Axis"
    Y = "Y-Axis"
    Z = "Z-Axis"
