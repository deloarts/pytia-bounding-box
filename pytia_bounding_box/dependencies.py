"""
    Installs/updates required dependencies.
    Some deps may not be available on PyPi or GitHub (or are private),
    therefor it's necessary to provide the web-link to the wheel file.

    All required dependencies are specified in the dependencies.json
    resource file.

    .. warning::
        Do not import third party modules here.
        This module must work on its own without any other dependencies!
"""

import importlib.resources
import json
import subprocess
import sys
import tkinter as tk
import tkinter.messagebox as tkmsg
from dataclasses import dataclass
from distutils.version import (
    LooseVersion,
)  # FIXME: Module will be removed in Python 3.12
from http.client import HTTPSConnection
from importlib import metadata
from socket import gaierror
from tkinter import ttk
from typing import Dict, List
from urllib.parse import urlparse

from const import CNEXT, CONFIG_DEPS, VENV_PYTHON, VENV_PYTHONW, WEB_PIP
from resources import resource


@dataclass(slots=True, kw_only=True, frozen=True)
class PackageInfo:
    """
    Dataclass for package infos from the dependencies.json.

    .. warning::
        The content of the dependencies.json must match the list of dependencies specified in the
        pyproject.toml file at the key **tool.poetry.dependencies**
    """

    name: str
    version: str
    wheel: str | None


class Environment:
    def __init__(self) -> None:
        ...

    @staticmethod
    def is_virtual() -> bool:
        return VENV_PYTHON in sys.executable or VENV_PYTHONW in sys.executable

    @classmethod
    def warn_if_not_virtual(cls) -> None:
        if not cls.is_virtual():
            result = tkmsg.askyesno(
                title=resource.settings.title,
                message=(
                    "The app is not running in its virtualenv environment. "
                    "This will install all dependencies global, which can lead to unexpected "
                    "behaviour.\n\nProceed with installing dependencies global?\n\n"
                    "Hint: To run the app in its environment use the launcher."
                ),
                icon="warning",
            )
            if not result:
                sys.exit()


class Dependencies:
    """Class for managing dependencies."""

    __slots__ = ("_required_packages", "_missing_packages", "_runs_in_venv")

    def __init__(self) -> None:
        self._runs_in_venv = (
            VENV_PYTHON in sys.executable or VENV_PYTHONW in sys.executable
        )

    @staticmethod
    def read_dependencies_file() -> List[PackageInfo]:
        """
        Reads the deps json from the resources folder.

        Returns:
            List[PackageInfo]: The dependencies as a list.
        """
        with importlib.resources.open_binary("resources", CONFIG_DEPS) as f:
            return [PackageInfo(**i) for i in json.load(f)]

    def _remove_venv(self) -> None:
        pass

    @staticmethod
    def web_resource_available(address: str) -> bool:
        """Returns wether a web resource is available or not."""
        domain = urlparse(address).netloc
        path = urlparse(address).path or "/"
        conn = HTTPSConnection(domain, timeout=5)

        print(path)

        try:
            conn.request("HEAD", path)
            response = conn.getresponse()
            return True if response.status in [200, 301, 302, 307, 308] else False
        except gaierror:
            print("not available")
            return False
        finally:
            conn.close()

    @classmethod
    def get_missing_packages(cls) -> List[PackageInfo]:
        """Returns a list of missing packages."""
        missing_packages = []
        for package in cls.read_dependencies_file():
            try:
                dist_version = metadata.version(package.name)
                if LooseVersion(dist_version) < LooseVersion(package.version):
                    missing_packages.append(package)
            except metadata.PackageNotFoundError:
                missing_packages.append(package)
        return missing_packages

    @classmethod
    def get_pip_commands(cls) -> dict:
        pip_commands = {}
        for missing_package in cls.get_missing_packages():
            if missing_package.wheel is not None:
                if cls.web_resource_available(missing_package.wheel):
                    pip_commands[missing_package.name] = missing_package.wheel
                else:
                    tkmsg.showerror(
                        title=resource.settings.title,
                        message=(
                            f"Cannot install dependency {missing_package.name!r}.\n\n"
                            "Python wheel is not available under the specified link. "
                            "Please notify your system administrator immediately."
                        ),
                    )
                    sys.exit()
            else:
                pip_commands[
                    missing_package.name
                ] = f'"{missing_package.name}=={missing_package.version}"'
        return pip_commands

    def install_dependencies(self) -> None:
        """Installs missing dependencies."""

        # If nothing's missing, return and start the app.
        if self.get_missing_packages() == []:
            return

        Environment.warn_if_not_virtual()

        installer = VisualInstaller()
        installer.install()

        # Check if all missing packages have been installed.
        if missing_packages := self.get_missing_packages():
            tkmsg.showerror(
                title=resource.settings.title,
                message=(
                    f"Installation of "
                    f"{', '.join(package.name for package in missing_packages)} failed.\n\n"
                    f"Please notify your system administrator immediately."
                ),
            )
        else:
            tkmsg.showinfo(
                title=resource.settings.title,
                message=(
                    "Successfully updated the app.\n\n"
                    "The app will start automatically, once all changes have been applied. "
                    "This may take a while.\n\nClick OK to continue."
                ),
            )
            subprocess.Popen(  # pylint: disable=R1732
                [
                    f"{resource.settings.paths.catia}\\{CNEXT}",
                    "-batch",
                    "-macro",
                    f"{resource.settings.paths.release}\\"
                    f"{resource.settings.files.launcher}",
                ]
            )
        sys.exit()


class VisualInstaller(tk.Tk):
    """UI class for dependency installation."""

    def __init__(self):
        super().__init__()

        self.message = tk.StringVar(name="message", value="Connecting to remote ...")
        self.progress = tk.IntVar(value=0, name="progress")

        self.title = f"{resource.settings.title} | Installer"
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.config(cursor="wait")
        self.geometry("300x90")
        self.eval(f"tk::PlaceWindow {self.winfo_toplevel()} center")

        self.lbl = ttk.Label(
            self,
            textvariable=self.message,
        )
        self.progress_bar = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL,
            length=270,
            variable=self.progress,
        )
        self.lbl.grid(row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w")
        self.progress_bar.grid(row=1, column=0, padx=(15, 3), pady=(15, 3))
        self.progress_bar.focus()

    def _install_pip(self) -> None:
        """Installs python packages using pip."""
        if not Dependencies.web_resource_available(WEB_PIP):
            tkmsg.showerror(
                title=resource.settings.title,
                message="Cannot install required dependencies: No internet connection.",
            )
            sys.exit()

        pip_commands = Dependencies.get_pip_commands()

        self.progress.set(1)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        for index, key in enumerate(pip_commands.keys()):
            python_exe = sys.executable
            if VENV_PYTHONW in python_exe:
                python_exe = python_exe.replace(VENV_PYTHONW, VENV_PYTHON)
            command = f"start /wait {python_exe} -m pip install {pip_commands[key]} --no-cache-dir"
            self.message.set(
                f"Installing package {index+1} of {len(pip_commands)}: {key}"
            )
            self.update_idletasks()
            with subprocess.Popen(command, shell=True) as process:
                while process.poll() is None:
                    self.update()
        self.progress_bar.stop()
        self.destroy()

    def install(self) -> None:
        """Installs all dependencies"""
        self.after(100, self._install_pip)
        self.after(250, self.focus_force)
        self.mainloop()


deps = Dependencies()
