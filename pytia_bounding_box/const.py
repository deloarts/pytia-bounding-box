"""
    Constants for the pytia bounding box app.
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path

__version__ = "0.5.0"

PYTIA = "pytia"
PYTIA_BOUNDING_BOX = "pytia_bounding_box"

APP_NAME = "PYTIA Bounding Box"
APP_VERSION = __version__

LOGON = str(os.environ.get("USERNAME")).lower()
CNEXT = "win_b64\\code\\bin\\CNEXT.exe"
TEMP = str(os.environ.get("TEMP"))
APPDATA = f"{str(os.environ.get('APPDATA'))}\\{PYTIA}\\{PYTIA_BOUNDING_BOX}"
LOGS = f"{APPDATA}\\logs"
LOG = "app.log"
PID = os.getpid()
PID_FILE = f"{TEMP}\\{PYTIA_BOUNDING_BOX}.pid"
VENV = f"\\.env\\{APP_VERSION}"
VENV_PYTHON = Path(VENV, "Scripts\\python.exe")
VENV_PYTHONW = Path(VENV, "Scripts\\pythonw.exe")
PY_VERSION = APPDATA + "\\pyversion.txt"

CONFIG_APPDATA = "config.json"
CONFIG_SETTINGS = "settings.json"
CONFIG_DEPS = "dependencies.json"
CONFIG_PROPS = "properties.json"
CONFIG_PROPS_DEFAULT = "properties.default.json"
CONFIG_PRESETS = "presets.json"
CONFIG_PRESETS_DEFAULT = "presets.default.json"
CONFIG_PROCESSES = "processes.json"
CONFIG_PROCESSES_DEFAULT = "processes.default.json"
CONFIG_INFOS = "information.json"
CONFIG_INFOS_DEFAULT = "information.default.json"
CONFIG_USERS = "users.json"

WEB_PIP = "https://www.pypi.org"

STYLES = [
    "cosmo",
    "litera",
    "flatly",
    "journal",
    "lumen",
    "minty",
    "pulse",
    "sandstone",
    "united",
    "yeti",
    "morph",
    "simplex",
    "cerculean",
    "solar",
    "superhero",
    "darkly",
    "cyborg",
    "vapor",
]


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
