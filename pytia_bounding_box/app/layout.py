"""
    The layout submodule of the app. Holds the layout of the main window.
"""

from tkinter import DISABLED, Tk

from app.frames import Frames
from app.helper import set_appearance_menu, show_help
from app.vars import Variables
from const import STYLES, Axes
from pytia_ui_tools.widgets.entries import NumberEntry
from pytia_ui_tools.widgets.scales import SnapScale
from resources import resource
from ttkbootstrap import Button, Checkbutton, Combobox, Entry, Label, Menu


class Layout:
    """The Layout class, holds the layout of the main window.

    Args:
        root (Tk): The main window.
        frames (Frames): The frames of the main window.
        variables (Variables): The variables of the main window.
    """

    def __init__(self, root: Tk, frames: Frames, variables: Variables) -> None:
        """Initialize the Layout class."""
        # region MENU
        menubar = Menu(root)

        self._appearance_menu = Menu(menubar, tearoff=False)
        for style in STYLES:
            self._appearance_menu.add_command(label=style)

        menubar.add_cascade(label="Help", command=show_help)
        menubar.add_cascade(label="Appearance", menu=self._appearance_menu)

        set_appearance_menu(self._appearance_menu)
        root.configure(menu=menubar)
        # endregion

        # SELECTIONS
        # PRESET SELECTION
        lbl_preset = Label(frames.selection, text="Preset", cursor="arrow", width=12)

        self._combo_preset = Combobox(
            frames.selection,
            values=[ts.name for ts in resource.presets],
            state=DISABLED,
        )
        self._combo_preset.current(0)

        lbl_preset.grid(row=0, column=0, padx=(15, 5), pady=(2, 2), sticky="w")
        self._combo_preset.grid(row=0, column=1, padx=(5, 10), pady=(2, 2), sticky="ew")

        # AXIS SELECTION
        lbl_axis = Label(frames.selection, text="Axis", cursor="arrow", width=12)

        self._combo_axis = Combobox(
            frames.selection,
            values=[a.value for a in Axes],
            state=DISABLED,
        )
        self._combo_axis.current(0)

        lbl_axis.grid(row=1, column=0, padx=(15, 3), pady=(2, 2), sticky="w")
        self._combo_axis.grid(row=1, column=1, padx=(5, 10), pady=(2, 2), sticky="ew")

        # OFFSET SELECTION
        lbl_offset = Label(frames.selection, text="Offset", cursor="arrow", width=12)
        self._scale_offset = SnapScale(
            frames.selection,  # type: ignore
            int_var=variables.scale_offset_value,
            from_=resource.settings.offset.min,
            to=resource.settings.offset.max,
            tick=resource.settings.offset.tick,
            length=180,
            orient="horizontal",
            state=DISABLED,
        )
        lbl_offset_value = Label(
            frames.selection,
            textvariable=variables.scale_offset_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        lbl_offset_unit = Label(frames.selection, text="mm", cursor="arrow")

        lbl_offset.grid(row=2, column=0, padx=(15, 3), pady=(5, 2), sticky="w")
        self._scale_offset.grid(row=2, column=1, padx=(5, 5), pady=(4, 1), sticky="w")
        lbl_offset_value.place(x=300, y=68)
        lbl_offset_unit.place(x=318, y=68)

        # STEP SELECTION
        lbl_step = Label(frames.selection, text="Step", cursor="arrow", width=12)
        self._scale_step = SnapScale(
            frames.selection,  # type: ignore
            int_var=variables.scale_step_value,
            from_=resource.settings.step.min,
            to=resource.settings.step.max,
            tick=resource.settings.step.tick,
            length=180,
            orient="horizontal",
            state=DISABLED,
        )
        lbl_step_value = Label(
            frames.selection,
            textvariable=variables.scale_step_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        lbl_step_unit = Label(frames.selection, text="mm", cursor="arrow")

        lbl_step.grid(row=3, column=0, padx=(15, 3), pady=(2, 2), sticky="w")
        self._scale_step.grid(row=3, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        lbl_step_value.place(x=300, y=95)
        lbl_step_unit.place(x=318, y=95)

        # THICKNESS
        lbl_thickness = Label(
            frames.selection, text="Thickness", cursor="arrow", width=12
        )
        self._chkbox_thickness = Checkbutton(
            frames.selection,
            bootstyle="round-toggle",  # type:ignore
            variable=variables.thickness_value,
            onvalue=1,
            offvalue=0,
            state=DISABLED,
        )
        lbl_thickness.grid(row=4, column=0, padx=(15, 3), pady=(3, 10), sticky="w")
        self._chkbox_thickness.grid(
            row=4, column=1, padx=(3, 5), pady=(3, 10), sticky="w"
        )

        # MEASURE AND SELECTED VALUE
        # X-AXIS
        lbl_values_unit = Label(frames.values, text="mm", cursor="arrow")
        lbl_values_slash = Label(frames.values, text="mm  / ", cursor="arrow")
        lbl_value_x = Label(
            frames.values,
            text=Axes.X.value,
            cursor="arrow",
            width=12,
        )
        self._entry_measure_x = NumberEntry(
            frames.values,
            width=12,
            state=DISABLED,
            string_var=variables.entry_measure_x_text,
        )
        self._entry_value_x = NumberEntry(
            frames.values,
            width=12,
            state=DISABLED,
            string_var=variables.entry_value_x_text,
        )

        lbl_value_x.grid(row=0, column=0, padx=(15, 5), pady=(2, 2), sticky="w")
        self._entry_measure_x.grid(
            row=0, column=1, padx=(5, 1), pady=(2, 2), sticky="w"
        )
        lbl_values_slash.grid(row=0, column=2, padx=(0, 0), pady=(2, 2), sticky="w")
        self._entry_value_x.grid(row=0, column=4, padx=(1, 1), pady=(2, 2), sticky="w")
        lbl_values_unit.grid(row=0, column=5, padx=(1, 10), pady=(2, 2), sticky="w")

        # Y-AXIS
        lbl_values_unit = Label(frames.values, text="mm", cursor="arrow")
        lbl_values_slash = Label(frames.values, text="mm  / ", cursor="arrow")
        lbl_value_y = Label(
            frames.values,
            text=Axes.Y.value,
            cursor="arrow",
            width=12,
        )
        self._entry_measure_y = NumberEntry(
            frames.values,
            width=12,
            state=DISABLED,
            string_var=variables.entry_measure_y_text,
        )
        self._entry_value_y = NumberEntry(
            frames.values,
            width=12,
            state=DISABLED,
            string_var=variables.entry_value_y_text,
        )

        lbl_value_y.grid(row=1, column=0, padx=(15, 5), pady=(2, 2), sticky="w")
        self._entry_measure_y.grid(
            row=1, column=1, padx=(5, 1), pady=(2, 2), sticky="w"
        )
        lbl_values_slash.grid(row=1, column=2, padx=(1, 1), pady=(2, 2), sticky="w")
        self._entry_value_y.grid(row=1, column=4, padx=(1, 1), pady=(2, 2), sticky="w")
        lbl_values_unit.grid(row=1, column=5, padx=(1, 1), pady=(2, 2), sticky="w")

        # Z-AXIS
        lbl_values_unit = Label(frames.values, text="mm", cursor="arrow")
        lbl_values_slash = Label(frames.values, text="mm  / ", cursor="arrow")
        lbl_value_z = Label(
            frames.values,
            text=Axes.Z.value,
            cursor="arrow",
            width=12,
        )
        self._entry_measure_z = NumberEntry(
            frames.values,
            width=12,
            state=DISABLED,
            string_var=variables.entry_measure_z_text,
        )
        self._entry_value_z = NumberEntry(
            frames.values,
            width=12,
            state=DISABLED,
            string_var=variables.entry_value_z_text,
        )

        lbl_value_z.grid(row=2, column=0, padx=(15, 5), pady=(3, 10), sticky="w")
        self._entry_measure_z.grid(
            row=2, column=1, padx=(5, 1), pady=(3, 10), sticky="w"
        )
        lbl_values_slash.grid(row=2, column=2, padx=(1, 1), pady=(3, 10), sticky="w")
        self._entry_value_z.grid(row=2, column=4, padx=(1, 1), pady=(3, 10), sticky="w")
        lbl_values_unit.grid(row=2, column=5, padx=(1, 1), pady=(3, 10), sticky="w")

        # RESULTS
        lbl_result_current = Label(
            frames.result, text="Current value", cursor="arrow", width=12
        )
        self._entry_result_current = Entry(
            frames.result,
            width=39,
            state=DISABLED,
            textvariable=variables.entry_result_current_text,
        )
        lbl_result_new = Label(
            frames.result, text="New value", cursor="arrow", width=12
        )
        self._entry_result_new = Entry(
            frames.result,
            width=39,
            state=DISABLED,
            textvariable=variables.entry_result_new_text,
        )

        lbl_result_current.grid(row=0, column=0, padx=(15, 5), pady=(2, 2), sticky="w")
        self._entry_result_current.grid(
            row=0, column=1, padx=(5, 2), pady=(2, 2), sticky="w"
        )

        lbl_result_new.grid(row=1, column=0, padx=(15, 5), pady=(2, 10), sticky="w")
        self._entry_result_new.grid(
            row=1, column=1, padx=(5, 2), pady=(2, 10), sticky="w"
        )

        # FOOTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self._btn_save = Button(
            frames.footer,
            text="Save",
            style="outline",
            width=10,
            state=DISABLED,
        )
        self._btn_save.grid(row=0, column=1, padx=(5, 2), pady=0, sticky="e")

        self._btn_abort = Button(
            frames.footer,
            text="Abort",
            style="outline",
            width=10,
            state=DISABLED,
        )
        self._btn_abort.grid(row=0, column=2, padx=(2, 0), pady=0, sticky="e")

    @property
    def input_preset(self) -> Combobox:
        """Returns the preset combobox widget."""
        return self._combo_preset

    @property
    def input_axis(self) -> Combobox:
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
    def input_thickness(self) -> Checkbutton:
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
    def stored_result(self) -> Entry:
        """Returns the entry for the previous result."""
        return self._entry_result_current

    @property
    def input_result(self) -> Entry:
        """Returns the input entry for the result."""
        return self._entry_result_new

    @property
    def button_save(self) -> Button:
        """Returns the save button."""
        return self._btn_save

    @property
    def button_abort(self) -> Button:
        """Returns the abort button."""
        return self._btn_abort
