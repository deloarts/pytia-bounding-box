"""
    Helper functions and classes for the UI.
"""

import functools
import re
import time
import webbrowser
from tkinter import BooleanVar, IntVar
from tkinter import messagebox as tkmsg
from typing import Optional, Tuple

from const import Axes, Preference
from pytia.const import USERNAME
from pytia.exceptions import (
    PytiaDifferentDocumentError,
    PytiaPropertyNotFoundError,
    PytiaValueError,
)
from pytia.log import log
from resources import Preset, resource


def show_help() -> None:
    """Opens the help docs."""
    if url := resource.settings.urls.help:
        webbrowser.open_new(url)
    else:
        tkmsg.showinfo(
            title=resource.settings.title,
            message="Your administrator did not provide a help page for this app.",
        )


def get_offset(
    x: str | int | float,
    y: str | int | float,
    z: str | int | float,
    selected_preset: Preset,
    selected_axis: Axes,
    selected_offset: IntVar,
    selected_step: IntVar,
) -> Tuple[float, float, float]:
    """
    Returns the calculated offsets as tuple, representing the three axes X, Y & Z.
    Calculates the offset values accordingly to the presets.json files.

    Args:
        x (str | int | float): The exact x measurements.
        y (str | int | float): The exact y measurements.
        z (str | int | float): The exact z measurements.
        selected_preset (Preset): The selected preset from the UI.
        selected_axis (Axes): The selected axis from the UI as Axes enum.
        selected_offset (IntVar): The selected offset from the UI.
        selected_step (IntVar): The selected step from the UI.

    Raises:
        PytiaValueError: Raised when the values cannot be casted to float.

    Returns:
        Tuple[float, float, float]: The offset values of the three axes X, Y & Z.
    """

    def _calculate_offset(value: float) -> float:
        offset = float(selected_offset.get())
        step = float(selected_step.get())
        return (
            round((value + offset + ((step / 2) - 0.01)) / step, 0) * step
            if step > 0
            else value
        )

    try:
        values = [float(x), float(y), float(z)]
    except ValueError as e:
        raise PytiaValueError(f"Value error: {e}") from e

    enable = [False] * 3
    offsets = [0.0] * 3

    for i, axis in enumerate(Axes):
        if selected_preset.preference:
            enable[i] = (
                selected_preset.offset_preference
                if selected_axis.value == axis.value
                else selected_preset.offset_non_preference
            )
        else:
            enable[i] = bool(selected_preset.offset)
        offsets[i] = _calculate_offset(values[i]) if enable[i] else values[i]

    return offsets[0], offsets[1], offsets[2]


def get_preferred_axis(
    x: str | int | float,
    y: str | int | float,
    z: str | int | float,
    selected_preset: Preset,
) -> Axes:
    """
    Returns the preferred axis according to the settings files. If no match between the selected
    preset and the configuration can be found, the x axis will be returned.

    Args:
        x (str | int | float): The exact X measurements.
        y (str | int | float): The exact Y measurements.
        z (str | int | float): The exact Z measurements.
        selected_preset (Preset): The selected preset from the UI.

    Raises:
        PytiaValueError: Raised when the values cannot be casted to float.

    Returns:
        str: The preferred axis according to the preset.
    """
    try:
        values = {Axes.X: float(x), Axes.Y: float(y), Axes.Z: float(z)}
    except Exception as e:
        raise PytiaValueError(f"Cannot get preferred axis: {e}") from e

    match selected_preset.preference:
        case Preference.MIN.value:
            return min(values, key=values.get)  # type: ignore
        case Preference.MAX.value:
            return max(values, key=values.get)  # type: ignore
        case Preference.AXIS.value:
            # To get the turning axis we assume that at least two axes have the same value.
            # The turning axis is therefor the one axis that has a different value.
            # If all 3 axes have different values (imagine a hexagonal head screw), we assume
            # that the axis with the longest value is the turning axis.
            diff = {
                k: v for k, v in values.items() if list(values.values()).count(v) == 1
            }
            return (
                list(diff.keys())[0]
                if len(diff) == 1
                else max(values, key=values.get)  # type: ignore
            )

        case _:
            return Axes.X


def sort_base_size(
    x: str | int | float,
    y: str | int | float,
    z: str | int | float,
    selected_preset: Preset,
    selected_axis: Axes,
    thickness: BooleanVar,
) -> str:
    """
    Sorts and formats the base size according to the settings files.

    Args:
        x (str | int | float): The evaluated bounding value for the X axis.
        y (str | int | float): The evaluated bounding value for the Y axis.
        z (str | int | float): The evaluated bounding value for the Z axis.
        selected_preset (Preset): The selected preset from the UI.
        selected_axis (Axes): The selected axis from the UI as Axes enum.
        thickness (BooleanVar): The selection from the thickness checkbox.

    Returns:
        str: The sorted and formatted base size. Returns an empty string if the \
            numbers can't be sorted.
    """

    try:
        x = float(x)
        y = float(y)
        z = float(z)
    except ValueError:
        return ""

    # The next three lines are to remove all positions after a comma if
    # the number only has zeros after the floating point.
    x = int(x) if x.is_integer() else x
    y = int(y) if y.is_integer() else y
    z = int(z) if z.is_integer() else z

    axis_values = {Axes.X.value: x, Axes.Y.value: y, Axes.Z.value: z}

    if selected_preset.coord in [3, 4]:
        # Sort values based on config file settings (selections.json).
        sorted_axes = {
            k: str(v)
            for k, v in sorted(
                axis_values.items(),
                key=lambda item: item[1],
                reverse=selected_preset.sort_max_to_min,
            )
        }

        # Add postfix.
        if selected_preset.preference_postfix:
            sorted_axes[selected_axis.value] = (
                sorted_axes[selected_axis.value] + selected_preset.preference_postfix
            )

        # Write the preferred axis at last.
        if selected_preset.preference:
            preferred_value = sorted_axes[selected_axis.value]
            del sorted_axes[selected_axis.value]
            sorted_list = list(sorted_axes.values())

            # Retrieve the thickness (if available) and write it at third position.
            if thickness.get() and selected_preset.coord == 4:
                part_helper = LazyPartHelper()
                thickness_value = part_helper.get_parameter(
                    resource.settings.parameters.thickness
                )
                if thickness_value:
                    try:
                        thickness_value = float(thickness_value)
                        thickness_value = (
                            int(thickness_value)
                            if thickness_value.is_integer()
                            else thickness_value
                        )
                        sorted_list.append(str(thickness_value))
                    except ValueError:
                        log.warning("Parameter 'thickness' cannot be casted to float.")

            # Add the length at last.
            sorted_list.append(preferred_value)
        else:
            sorted_list = list(sorted_axes.values())
        return " x ".join(sorted_list)
    else:
        length = axis_values[selected_axis.value]
        del axis_values[selected_axis.value]
        diameter = max(axis_values.values())
        return f"Ø{diameter} x {length}"


class LazyPartHelper:
    """
    Helper class for late imports of any kind of methods related to handle part operations.

    Important: This class loads the current part document only once (on instantiation). If the
    document changes all operations will be made on the original document.

    Use the ensure_part_not_changed method if you're not sure if the part hasn't changed.
    """

    def __init__(self) -> None:
        # Import the PyPartDocument after the GUI exception handler is initialized.
        # Otherwise the CATIA-not-running-exception will not be caught.
        # Also: The UI will load a little bit faster.

        # pylint: disable=C0415
        # pylint: disable=C0103
        t0 = time.perf_counter()
        from pytia.wrapper.documents.part_documents import PyPartDocument

        t1 = time.perf_counter()
        log.debug(f"Loaded PyPartDocument in {(t1-t0):.4f}s")
        # pylint: enable=C0415
        # pylint: enable=C0103

        self.part_document = PyPartDocument()
        self.part_document.current()
        self.part_name = self.part_document.document.name

    def _part_changed(self) -> bool:
        """Returns True if the current part document has changed, False if not."""
        part_document = self.part_document
        part_document.current()
        return part_document.document.name != self.part_name

    @staticmethod
    def _ensure_part_not_changed(func):
        """
        Ensures that the part hasn't changed.
        Raises the PytiaDifferentDocumentError if the part has changed.
        """

        # pylint: disable=W0212
        @functools.wraps(func)
        def _ensure_part_not_changed_wrapper(self, *args, **kwargs):
            if self._part_changed():
                part_document = self.part_document
                part_document.current()
                raise PytiaDifferentDocumentError(
                    f"The name of the current document has changed:\n"
                    f" - Original was {self.part_name}\n"
                    f" - Current is {part_document.document.name}"
                )
            return func(self, *args, **kwargs)

        # pylint: enable=W0212

        return _ensure_part_not_changed_wrapper

    @_ensure_part_not_changed
    def get_parameter(self, name: str) -> Optional[str]:
        """
        Retrieves a parameters value from the part.

        Args:
            name (str): The name of the parameter to retrieve the value from.

        Returns:
            Optional[str]: The value of the parameter as string.
        """
        if self.part_document.parameters.exists(name):
            param = str(self.part_document.parameters.get(name).value)
            log.info(f"Retrieved parameter {name} ({param}) from part.")
            return param
        else:
            log.info(f"Couldn't retrieve parameter {name} from part: Doesn't exists.")
            return None

    @_ensure_part_not_changed
    def get_property(self, name: str) -> Optional[str]:
        """
        Retrieves a properties value from the part properties.

        Args:
            name (str): The name of the property to retrieve the value from.

        Returns:
            Optional[str]: The value of the property as string.
        """
        if self.part_document.parameters.exists(name):
            param = str(self.part_document.parameters.get(name).value)
            log.info(f"Retrieved property {name} ({param}) from part.")
            return param
        else:
            log.info(f"Couldn't retrieve property {name} from part: Doesn't exists.")
            return None

    @_ensure_part_not_changed
    def write_property(self, name: str, value: str) -> None:
        """
        Writes the property to the part properties.

        Args:
            name (str): The name of the property.
            value (str): The value of the property.
        """
        if not self.part_document.properties.exists(name):
            if not resource.settings.allow_property_creation:
                raise PytiaPropertyNotFoundError(
                    f"The app doesn't have the permission to create properties at runtime. "
                    f"All required properties must be created before running this app."
                )
            self.part_document.properties.create(name, value)
        self.part_document.properties.set_value(name, value)
        log.info(f"Wrote property {name!r} to part with value {value!r}.")

    @_ensure_part_not_changed
    def write_modifier(self, write_creator: bool = True) -> None:
        """
        Saves the modifier to the part properties.

        Args:
            write_creator (bool, optional): Also write the creator. Defaults to True.
        """
        if resource.user_exists(USERNAME):
            user = resource.get_user_by_logon(USERNAME)
            filter_result = re.findall(r"\%(.*?)\%", resource.settings.save_modifier_by)
            modifier = resource.settings.save_modifier_by

            if all(elem in user.keys for elem in filter_result):
                for key in filter_result:
                    modifier = modifier.replace(f"%{key}%", getattr(user, key))
            else:
                log.warning(
                    f"Cannot save user by {resource.settings.save_modifier_by!r}. "
                    f"Saving logon name {USERNAME!r} to {resource.props.modifier!r}."
                )
                modifier = USERNAME
        else:
            modifier = USERNAME
            log.warning(
                f"Current user doesn't exist in config file. Saving logon name {USERNAME!r} to "
                f"{resource.props.modifier!r}."
            )

        self.write_property(resource.props.modifier, modifier)
        if not self.get_property(resource.props.creator) and write_creator:
            self.write_property(resource.props.creator, modifier)
