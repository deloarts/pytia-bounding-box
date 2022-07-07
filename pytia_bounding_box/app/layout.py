"""
    The layout submodule of the app. Holds the layout of the main window.
"""

from tkinter import DISABLED, SE, ttk

from const import Axes
from pytia_ui_tools.widgets.entries import NumberEntry
from pytia_ui_tools.widgets.scales import SnapScale
from resources import resource

from app.frames import Frames
from app.vars import Variables


class Layout:
    """The Layout class, holds the layout of the main window."""

    def __init__(self, frames: Frames, variables: Variables) -> None:
        """Initialize the Layout class."""
        # SELECTIONS
        lbl_selection_header = ttk.Label(
            frames.selection_header,
            text="Selection",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        lbl_selection_header.grid(
            row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w"
        )

        # PRESET SELECTION
        lbl_preset = ttk.Label(
            frames.selection, text="Preset", cursor="arrow", width=12
        )

        self._combo_preset = ttk.Combobox(
            frames.selection,
            values=[ts.name for ts in resource.presets],
            width=35,
            state=DISABLED,
        )
        self._combo_preset.current(0)

        lbl_preset.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self._combo_preset.grid(row=0, column=1, padx=(5, 5), pady=(3, 3), sticky="w")

        # AXIS SELECTION
        lbl_axis = ttk.Label(frames.selection, text="Axis", cursor="arrow", width=12)

        self._combo_axis = ttk.Combobox(
            frames.selection,
            values=[a.value for a in Axes],
            width=35,
            state=DISABLED,
        )
        self._combo_axis.current(0)

        lbl_axis.grid(row=1, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self._combo_axis.grid(row=1, column=1, padx=(5, 5), pady=(3, 3), sticky="w")

        # OFFSET SELECTION
        lbl_offset = ttk.Label(
            frames.selection, text="Offset", cursor="arrow", width=12
        )
        self._scale_offset = SnapScale(
            frames.selection,
            int_var=variables.scale_offset_value,
            from_=resource.settings.offset.min,
            to=resource.settings.offset.max,
            tick=resource.settings.offset.tick,
            length=180,
            orient="horizontal",
            state=DISABLED,
        )
        lbl_offset_value = ttk.Label(
            frames.selection,
            textvariable=variables.scale_offset_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        lbl_offset_unit = ttk.Label(frames.selection, text="mm", cursor="arrow")

        lbl_offset.grid(row=2, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self._scale_offset.grid(row=2, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        lbl_offset_value.place(x=300, y=55)
        lbl_offset_unit.place(x=318, y=55)

        # STEP SELECTION
        lbl_step = ttk.Label(frames.selection, text="Step", cursor="arrow", width=12)
        self._scale_step = SnapScale(
            frames.selection,
            int_var=variables.scale_step_value,
            from_=resource.settings.step.min,
            to=resource.settings.step.max,
            tick=resource.settings.step.tick,
            length=180,
            orient="horizontal",
            state=DISABLED,
        )
        lbl_step_value = ttk.Label(
            frames.selection,
            textvariable=variables.scale_step_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        lbl_step_unit = ttk.Label(frames.selection, text="mm", cursor="arrow")

        lbl_step.grid(row=3, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self._scale_step.grid(row=3, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        lbl_step_value.place(x=300, y=84)
        lbl_step_unit.place(x=318, y=84)

        # THICKNESS
        lbl_thickness = ttk.Label(
            frames.selection, text="Thickness", cursor="arrow", width=12
        )
        self._chkbox_thickness = ttk.Checkbutton(
            frames.selection,
            variable=variables.thickness_value,
            onvalue=1,
            offvalue=0,
            style="Grey.TCheckbutton",
            state=DISABLED,
        )
        lbl_thickness.grid(row=4, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self._chkbox_thickness.grid(
            row=4, column=1, padx=(3, 5), pady=(3, 3), sticky="w"
        )

        # MEASURE AND SELECTED VALUE
        lbl_values_header = ttk.Label(
            frames.values_header,
            text="Measured / Selected",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        lbl_values_header.grid(row=0, column=0, padx=(15, 5), pady=(15, 5), sticky="w")

        # X-AXIS
        lbl_values_unit = ttk.Label(frames.values, text="mm", cursor="arrow")
        lbl_values_slash = ttk.Label(frames.values, text="mm  / ", cursor="arrow")
        lbl_value_x = ttk.Label(
            frames.values,
            text=Axes.X.value,
            cursor="arrow",
            width=12,
        )
        self._entry_measure_x = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_measure_x_text,
        )
        self._entry_value_x = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_value_x_text,
        )

        lbl_value_x.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self._entry_measure_x.grid(
            row=0, column=1, padx=(5, 1), pady=(3, 3), sticky="w"
        )
        lbl_values_slash.grid(row=0, column=2, padx=(1, 1), pady=(3, 3), sticky="w")
        self._entry_value_x.grid(row=0, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        lbl_values_unit.grid(row=0, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # Y-AXIS
        lbl_values_unit = ttk.Label(frames.values, text="mm", cursor="arrow")
        lbl_values_slash = ttk.Label(frames.values, text="mm  / ", cursor="arrow")
        lbl_value_y = ttk.Label(
            frames.values,
            text=Axes.Y.value,
            cursor="arrow",
            width=12,
        )
        self._entry_measure_y = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_measure_y_text,
        )
        self._entry_value_y = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_value_y_text,
        )

        lbl_value_y.grid(row=1, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self._entry_measure_y.grid(
            row=1, column=1, padx=(5, 1), pady=(3, 3), sticky="w"
        )
        lbl_values_slash.grid(row=1, column=2, padx=(1, 1), pady=(3, 3), sticky="w")
        self._entry_value_y.grid(row=1, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        lbl_values_unit.grid(row=1, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # Z-AXIS
        lbl_values_unit = ttk.Label(frames.values, text="mm", cursor="arrow")
        lbl_values_slash = ttk.Label(frames.values, text="mm  / ", cursor="arrow")
        lbl_value_z = ttk.Label(
            frames.values,
            text=Axes.Z.value,
            cursor="arrow",
            width=12,
        )
        self._entry_measure_z = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_measure_z_text,
        )
        self._entry_value_z = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_value_z_text,
        )

        lbl_value_z.grid(row=2, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self._entry_measure_z.grid(
            row=2, column=1, padx=(5, 1), pady=(3, 3), sticky="w"
        )
        lbl_values_slash.grid(row=2, column=2, padx=(1, 1), pady=(3, 3), sticky="w")
        self._entry_value_z.grid(row=2, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        lbl_values_unit.grid(row=2, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # RESULTS
        lbl_result_header = ttk.Label(
            frames.result_header,
            text="Result",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        lbl_result_header.grid(row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w")

        lbl_result_current = ttk.Label(
            frames.result, text="Current value", cursor="arrow", width=12
        )
        self._entry_result_current = ttk.Entry(
            frames.result,
            width=38,
            style="Global.TEntry",
            state=DISABLED,
            textvariable=variables.entry_result_current_text,
        )
        lbl_result_new = ttk.Label(
            frames.result, text="New value", cursor="arrow", width=12
        )
        self._entry_result_new = ttk.Entry(
            frames.result,
            width=38,
            style="Global.TEntry",
            state=DISABLED,
            textvariable=variables.entry_result_new_text,
        )

        lbl_result_current.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self._entry_result_current.grid(
            row=0, column=1, padx=(5, 5), pady=(3, 3), sticky="w"
        )

        lbl_result_new.grid(row=1, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self._entry_result_new.grid(
            row=1, column=1, padx=(5, 5), pady=(3, 3), sticky="w"
        )

        # FOOTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._btn_save = ttk.Button(
            frames.footer,
            text="Save",
            state=DISABLED,
            style="Footer.TButton",
        )
        self._btn_abort = ttk.Button(
            frames.footer,
            text="Abort",
            state=DISABLED,
            style="Footer.TButton",
        )

        self._btn_save.place(rely=1.0, relx=1.0, x=-115, y=-15, anchor=SE)
        self._btn_abort.place(rely=1.0, relx=1.0, x=-15, y=-15, anchor=SE)

    @property
    def input_preset(self) -> ttk.Combobox:
        """Returns the preset combobox widget."""
        return self._combo_preset

    @property
    def input_axis(self) -> ttk.Combobox:
        """Returns the axis combobox widget."""
        return self._combo_axis

    @property
    def input_offset(self) -> SnapScale:
        """Returns the offset scale widget."""
        return self._scale_offset

    @property
    def input_step(self) -> SnapScale:
        """Returns the step scale widget."""
        return self._scale_step

    @property
    def input_thickness(self) -> ttk.Checkbutton:
        """Returns the thickness checkbox widget."""
        return self._chkbox_thickness

    @property
    def measure_x(self) -> NumberEntry:
        """Returns the measure entry for the x axis."""
        return self._entry_measure_x

    @property
    def input_x(self) -> NumberEntry:
        """Returns the input entry for the x axis."""
        return self._entry_value_x

    @property
    def measure_y(self) -> NumberEntry:
        """Returns the measure entry for the y axis."""
        return self._entry_measure_y

    @property
    def input_y(self) -> NumberEntry:
        """Returns the input entry for the y axis."""
        return self._entry_value_y

    @property
    def measure_z(self) -> NumberEntry:
        """Returns the measure entry for the z axis."""
        return self._entry_measure_z

    @property
    def input_z(self) -> NumberEntry:
        """Returns the input entry for the z axis."""
        return self._entry_value_z

    @property
    def stored_result(self) -> ttk.Entry:
        """Returns the entry for the previous result."""
        return self._entry_result_current

    @property
    def input_result(self) -> ttk.Entry:
        """Returns the input entry for the result."""
        return self._entry_result_new

    @property
    def button_save(self) -> ttk.Button:
        """Returns the save button."""
        return self._btn_save

    @property
    def button_abort(self) -> ttk.Button:
        """Returns the abort button."""
        return self._btn_abort
