"""
    Loads the content from config files.

    Important: Do not import third party modules here. This module
    must work on its own without any other dependencies!
"""

import atexit
import importlib.resources
import json
import os
import tkinter.messagebox as tkmsg
from dataclasses import asdict, dataclass, field, fields
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Callable, List, Optional

from const import (
    APP_VERSION,
    APPDATA,
    CONFIG_APPDATA,
    CONFIG_INFOS,
    CONFIG_INFOS_DEFAULT,
    CONFIG_PRESETS,
    CONFIG_PRESETS_DEFAULT,
    CONFIG_PROCESSES,
    CONFIG_PROCESSES_DEFAULT,
    CONFIG_PROPS,
    CONFIG_PROPS_DEFAULT,
    CONFIG_SETTINGS,
    CONFIG_USERS,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsScale:
    """Dataclass for scale ui-elements settings (settings.json)."""

    min: int
    max: int
    tick: int


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsParameters:
    """Dataclass for scale ui-elements settings (settings.json)."""

    thickness: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsPaths:
    """Dataclass for paths (settings.json)."""

    local_dependencies: Path
    release: Path


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsFiles:
    """Dataclass for files (settings.json)."""

    app: str
    launcher: str


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsUrls:
    """Dataclass for urls (settings.json)."""

    help: str | None


@dataclass(slots=True, kw_only=True, frozen=True)
class SettingsMails:
    """Dataclass for mails (settings.json)."""

    admin: str


@dataclass(slots=True, kw_only=True)
class Settings:  # pylint: disable=R0902
    """Dataclass for settings (settings.json)."""

    title: str
    debug: bool
    precision: int
    offset: SettingsScale
    step: SettingsScale
    parameters: SettingsParameters
    enable_information: bool
    allow_all_users: bool
    allow_property_creation: bool
    save_modifier_by: str
    files: SettingsFiles
    paths: SettingsPaths
    urls: SettingsUrls
    mails: SettingsMails

    def __post_init__(self) -> None:
        self.offset = SettingsScale(**dict(self.offset))  # type: ignore
        self.step = SettingsScale(**dict(self.step))  # type: ignore
        self.parameters = SettingsParameters(**dict(self.parameters))  # type: ignore
        self.files = SettingsFiles(**dict(self.files))  # type: ignore
        self.paths = SettingsPaths(**dict(self.paths))  # type: ignore
        self.urls = SettingsUrls(**dict(self.urls))  # type: ignore
        self.mails = SettingsMails(**dict(self.mails))  # type: ignore


@dataclass(slots=True, kw_only=True, frozen=True)
class Props:
    """Dataclass for properties on the part (properties.json)."""

    base_size: str
    base_size_preset: str
    creator: str
    modifier: str
    process: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the Props dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the Props dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class Preset:  # pylint: disable=R0902
    """Dataclass for a preset for the bounding box (presets.json)."""

    name: str
    coord: int
    preference: Optional[str]
    preference_postfix: Optional[str]
    offset: Optional[int]
    step: int
    offset_preference: bool
    offset_non_preference: bool
    sort_max_to_min: bool
    result_filter: str
    tooltip: str
    filter_examples: List[str]


@dataclass(slots=True, kw_only=True, frozen=True)
class Process:
    """Dataclass for the process to preset conversion (processes.json)."""

    name: str
    preset: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the Process dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the Process dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class User:
    """Dataclass a user (users.json)."""

    logon: str
    id: str
    name: str
    mail: str

    @property
    def keys(self) -> List[str]:
        """Returns a list of all keys from the User dataclass."""
        return [f.name for f in fields(self)]

    @property
    def values(self) -> List[str]:
        """Returns a list of all values from the User dataclass."""
        return [getattr(self, f.name) for f in fields(self)]


@dataclass(slots=True, kw_only=True, frozen=True)
class Info:
    """Dataclass for an info messages (information.json)."""

    counter: int
    msg: str


@dataclass(slots=True, kw_only=True)
class AppData:
    """Dataclass for appdata settings."""

    version: str = field(default=APP_VERSION)
    counter: int = 0
    disable_volume_warning: bool = False

    def __post_init__(self) -> None:
        self.version = (
            APP_VERSION  # Always store the latest version in the appdata json
        )
        self.counter += 1


class Resources:  # pylint: disable=R0902
    """Class for handling resource files."""

    __slots__ = (
        "_settings",
        "_props",
        "_processes",
        "_presets",
        "_users",
        "_infos",
        "_appdata",
    )

    def __init__(self) -> None:
        self._read_settings()
        self._read_props()
        self._read_presets()
        self._read_users()
        self._read_processes()
        self._read_infos()
        self._read_appdata()

        atexit.register(self._write_appdata)

    @property
    def settings(self) -> Settings:
        """settings.json"""
        return self._settings

    @property
    def props(self) -> Props:
        """properties.json"""
        return self._props

    @property
    def presets(self) -> List[Preset]:
        """presets.json"""
        return self._presets

    @property
    def processes(self) -> List[Process]:
        """processes.json"""
        return self._processes

    @property
    def users(self) -> List[User]:
        """users.json"""
        return self._users

    @property
    def infos(self) -> List[Info]:
        """infos.json"""
        return self._infos

    @property
    def appdata(self) -> AppData:
        """Property for the appdata config file."""
        return self._appdata

    def _read_settings(self) -> None:
        """Reads the settings json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_SETTINGS) as f:
            self._settings = Settings(**json.load(f))

    def _read_presets(self) -> None:
        """Reads the presets json from the resources folder."""
        presets_resource = (
            CONFIG_PRESETS
            if importlib.resources.is_resource("resources", CONFIG_PRESETS)
            else CONFIG_PRESETS_DEFAULT
        )
        with importlib.resources.open_binary("resources", presets_resource) as f:
            self._presets = [Preset(**i) for i in json.load(f)]

    def _read_users(self) -> None:
        """Reads the users json from the resources folder."""
        with importlib.resources.open_binary("resources", CONFIG_USERS) as f:
            self._users = [User(**i) for i in json.load(f)]

    def _read_props(self) -> None:
        """Reads the props json from the resources folder."""
        props_resource = (
            CONFIG_PROPS
            if importlib.resources.is_resource("resources", CONFIG_PROPS)
            else CONFIG_PROPS_DEFAULT
        )
        with importlib.resources.open_binary("resources", props_resource) as f:
            self._props = Props(**json.load(f))

    def _read_processes(self) -> None:
        """Reads the processes json from the resources folder."""
        processes_resource = (
            CONFIG_PROCESSES
            if importlib.resources.is_resource("resources", CONFIG_PROCESSES)
            else CONFIG_PROCESSES_DEFAULT
        )
        with importlib.resources.open_binary("resources", processes_resource) as f:
            self._processes = [Process(**i) for i in json.load(f)]

    def _read_infos(self) -> None:
        """Reads the information json from the resources folder."""
        infos_resource = (
            CONFIG_INFOS
            if importlib.resources.is_resource("resources", CONFIG_INFOS)
            else CONFIG_INFOS_DEFAULT
        )
        with importlib.resources.open_binary("resources", infos_resource) as f:
            self._infos = [Info(**i) for i in json.load(f)]

    def _read_appdata(self) -> None:
        """Reads the json config file from the appdata folder."""
        if os.path.exists(appdata_file := f"{APPDATA}\\{CONFIG_APPDATA}"):
            with open(appdata_file, "r", encoding="utf8") as f:
                try:
                    value = AppData(**json.load(f))
                except JSONDecodeError:
                    value = AppData()
                    tkmsg.showwarning(
                        title="Configuration warning",
                        message="The AppData config file has been corrupted. \
                            You may need to apply your preferences again.",
                    )
                self._appdata = value
        else:
            self._appdata = AppData()

    def _write_appdata(self) -> None:
        """Saves appdata config to file."""
        os.makedirs(APPDATA, exist_ok=True)
        with open(f"{APPDATA}\\{CONFIG_APPDATA}", "w", encoding="utf8") as f:
            json.dump(asdict(self._appdata), f)

    @staticmethod
    def get_keys(c: Callable) -> List[str]:
        """
        Returns the keys of a provided dataclass.

        Args:
            c (Callable): The dataclass from which to get its keys.

        Returns:
            List[str]: The list of keys.
        """
        return [f.name for f in fields(c)]

    @staticmethod
    def get_values(c: Callable) -> List[str]:
        """
        Returns the values of the given dataclass.

        Args:
            c (Callable): The dataclass from which to get its values.

        Returns:
            List[str]: The list of values.
        """
        return [getattr(c, f.name) for f in fields(c)]

    def process_exists(self, name: str) -> bool:
        """
        Returns wether a process exists in the processes settings file.

        Args:
            name (str): The name of the process to search for.

        Returns:
            bool: True if the process exists, False otherwise.
        """
        for process in self._processes:
            if process.name == name:
                return True
        return False

    def get_process_by_name(self, name: str) -> Process:
        """
        Returns a process dataclass by its name.

        Args:
            name (str): The name of the process to fetch.

        Raises:
            ValueError: Raised when the process doesn't exist.'

        Returns:
            Processes: The process object.
        """
        for index, value in enumerate(self._processes):
            if value.name == name:
                return self._processes[index]
        raise ValueError

    def get_preset_by_name(self, name: str) -> Preset:
        """
        Returns the preset dataclass by its name.

        Args:
            name (str): The name of the preset to fetch.

        Raises:
            ValueError: Raised when the preset doesn't exist.'

        Returns:
            Preset: The preset object.
        """
        for index, value in enumerate(self._presets):
            if value.name == name:
                return self._presets[index]
        raise ValueError

    def preset_exists(self, name: str) -> bool:
        """
        Returns wether the a preset by the provided name exists, or not.

        Args:
            name (str): The name of the preset to fetch.

        Returns:
            bool: True if the preset exists, False otherwise.
        """
        for preset in self._presets:
            if preset.name == name:
                return True
        return False

    def get_user_by_logon(self, logon: str) -> User:
        """
        Returns the user dataclass that matches the logon value.

        Args:
            user (str): The user to fetch from the dataclass list.

        Raises:
            ValueError: Raised when the user doesn't exist.

        Returns:
            User: The user from the dataclass list that matches the provided logon name.
        """
        for index, value in enumerate(self._users):
            if value.logon == logon:
                return self._users[index]
        raise ValueError

    def user_exists(self, logon: str) -> bool:
        """
        Returns wether the user exists in the dataclass list, or not.

        Args:
            logon (str): The logon name to search for.

        Returns:
            bool: The user from the dataclass list that matches the provided logon name.
        """
        for user in self._users:
            if user.logon == logon:
                return True
        return False

    def get_info_msg_by_counter(self) -> List[str]:
        """
        Returns the info message by the app usage counter.

        Returns:
            List[str]: A list of all messages that should be shown at the counter value.
        """
        values = []
        for index, value in enumerate(self._infos):
            if value.counter == self._appdata.counter:
                values.append(self._infos[index].msg)
        return values


resource = Resources()
