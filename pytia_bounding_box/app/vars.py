"""
    The variables submodule of the main window.
"""

from dataclasses import dataclass
from tkinter import BooleanVar, IntVar, StringVar, Tk

from const import Axes
from pytia_bounding_box import resources
from resources import resource


@dataclass(slots=True, kw_only=True)
class Variables:
    """The Variables dataclass. Provides all variables for the main window."""

    x_measure: int | float
    y_measure: int | float
    z_measure: int | float

    scale_offset_value: IntVar
    scale_step_value: IntVar
    thickness_value: BooleanVar

    entry_measure_x_text: StringVar
    entry_measure_y_text: StringVar
    entry_measure_z_text: StringVar

    entry_value_x_text: StringVar
    entry_value_y_text: StringVar
    entry_value_z_text: StringVar

    entry_result_current_text: StringVar
    entry_result_new_text: StringVar

    selected_preset: resources.Preset
    selected_axis: Axes
    pre_selected_preset_reason: str

    def __init__(self, root: Tk) -> None:
        """Initialize the variables."""
        self.x_measure = 0.0
        self.y_measure = 0.0
        self.z_measure = 0.0

        self.scale_offset_value = IntVar(master=root, name="scale_offset_value")
        self.scale_step_value = IntVar(master=root, name="scale_step_value")
        self.thickness_value = BooleanVar(master=root, name="thickness_value")

        self.entry_measure_x_text = StringVar(master=root, name="entry_measure_x_text")
        self.entry_measure_y_text = StringVar(master=root, name="entry_measure_y_text")
        self.entry_measure_z_text = StringVar(master=root, name="entry_measure_z_text")

        self.entry_value_x_text = StringVar(master=root, name="entry_value_x_text")
        self.entry_value_y_text = StringVar(master=root, name="entry_value_y_text")
        self.entry_value_z_text = StringVar(master=root, name="entry_value_z_text")

        self.entry_result_current_text = StringVar(
            master=root, name="entry_result_current_text"
        )
        self.entry_result_new_text = StringVar(
            master=root, name="entry_result_new_text"
        )

        self.selected_preset = resource.presets[0]
        self.selected_axis = Axes.X
        self.pre_selected_preset_reason = ""
