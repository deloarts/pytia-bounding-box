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
        self.lbl_selection_header = ttk.Label(
            frames.selection_header,
            text="Selection",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_selection_header.grid(
            row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w"
        )

        # PRESET SELECTION
        self.lbl_preset = ttk.Label(
            frames.selection, text="Preset", cursor="arrow", width=12
        )

        self.combo_preset = ttk.Combobox(
            frames.selection,
            values=[ts.name for ts in resource.presets],
            width=35,
            state="readonly",
        )
        self.combo_preset.current(0)

        self.lbl_preset.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.combo_preset.grid(row=0, column=1, padx=(5, 5), pady=(3, 3), sticky="w")

        # AXIS SELECTION
        self.lbl_axis = ttk.Label(
            frames.selection, text="Axis", cursor="arrow", width=12
        )

        self.combo_axis = ttk.Combobox(
            frames.selection,
            values=[a.value for a in Axes],
            width=35,
            state="readonly",
        )
        self.combo_axis.current(0)

        self.lbl_axis.grid(row=1, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.combo_axis.grid(row=1, column=1, padx=(5, 5), pady=(3, 3), sticky="w")

        # OFFSET SELECTION
        self.lbl_offset = ttk.Label(
            frames.selection, text="Offset", cursor="arrow", width=12
        )
        self.scale_offset = SnapScale(
            frames.selection,
            int_var=variables.scale_offset_value,
            from_=resource.settings.offset.min,
            to=resource.settings.offset.max,
            tick=resource.settings.offset.tick,
            length=180,
            orient="horizontal",
            # command=self.callback_scale_offset,
        )
        self.lbl_offset_value = ttk.Label(
            frames.selection,
            textvariable=variables.scale_offset_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        self.lbl_offset_unit = ttk.Label(frames.selection, text="mm", cursor="arrow")

        self.lbl_offset.grid(row=2, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.scale_offset.grid(row=2, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        self.lbl_offset_value.place(x=300, y=55)
        self.lbl_offset_unit.place(x=318, y=55)

        # STEP SELECTION
        self.lbl_step = ttk.Label(
            frames.selection, text="Step", cursor="arrow", width=12
        )
        self.scale_step = SnapScale(
            frames.selection,
            int_var=variables.scale_step_value,
            from_=resource.settings.step.min,
            to=resource.settings.step.max,
            tick=resource.settings.step.tick,
            length=180,
            orient="horizontal",
            # command=self.callback_scale_step,
        )
        self.lbl_step_value = ttk.Label(
            frames.selection,
            textvariable=variables.scale_step_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        self.lbl_step_unit = ttk.Label(frames.selection, text="mm", cursor="arrow")

        self.lbl_step.grid(row=3, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.scale_step.grid(row=3, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        self.lbl_step_value.place(x=300, y=84)
        self.lbl_step_unit.place(x=318, y=84)

        # THICKNESS
        self.lbl_thickness = ttk.Label(
            frames.selection, text="Thickness", cursor="arrow", width=12
        )
        self.chkbox_thickness = ttk.Checkbutton(
            frames.selection,
            variable=variables.thickness_value,
            onvalue=1,
            offvalue=0,
            style="Grey.TCheckbutton",
            # command=self.callback_thickness,
        )
        self.lbl_thickness.grid(row=4, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.chkbox_thickness.grid(
            row=4, column=1, padx=(3, 5), pady=(3, 3), sticky="w"
        )

        # MEASURE AND SELECTED VALUE
        self.lbl_values_header = ttk.Label(
            frames.values_header,
            text="Measured / Selected",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_values_header.grid(
            row=0, column=0, padx=(15, 5), pady=(15, 5), sticky="w"
        )

        # X-AXIS
        self.lbl_values_unit = ttk.Label(frames.values, text="mm", cursor="arrow")
        self.lbl_values_slash = ttk.Label(frames.values, text="mm  / ", cursor="arrow")
        self.lbl_value_x = ttk.Label(
            frames.values,
            text=Axes.X.value,
            cursor="arrow",
            width=12,
        )
        self.entry_measure_x = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_measure_x_text,
        )
        self.entry_value_x = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            string_var=variables.entry_value_x_text,
        )

        self.lbl_value_x.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.entry_measure_x.grid(row=0, column=1, padx=(5, 1), pady=(3, 3), sticky="w")
        self.lbl_values_slash.grid(
            row=0, column=2, padx=(1, 1), pady=(3, 3), sticky="w"
        )
        self.entry_value_x.grid(row=0, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        self.lbl_values_unit.grid(row=0, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # Y-AXIS
        self.lbl_values_unit = ttk.Label(frames.values, text="mm", cursor="arrow")
        self.lbl_values_slash = ttk.Label(frames.values, text="mm  / ", cursor="arrow")
        self.lbl_value_y = ttk.Label(
            frames.values,
            text=Axes.Y.value,
            cursor="arrow",
            width=12,
        )
        self.entry_measure_y = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_measure_y_text,
        )
        self.entry_value_y = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            string_var=variables.entry_value_y_text,
        )

        self.lbl_value_y.grid(row=1, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.entry_measure_y.grid(row=1, column=1, padx=(5, 1), pady=(3, 3), sticky="w")
        self.lbl_values_slash.grid(
            row=1, column=2, padx=(1, 1), pady=(3, 3), sticky="w"
        )
        self.entry_value_y.grid(row=1, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        self.lbl_values_unit.grid(row=1, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # Z-AXIS
        self.lbl_values_unit = ttk.Label(frames.values, text="mm", cursor="arrow")
        self.lbl_values_slash = ttk.Label(frames.values, text="mm  / ", cursor="arrow")
        self.lbl_value_z = ttk.Label(
            frames.values,
            text=Axes.Z.value,
            cursor="arrow",
            width=12,
        )
        self.entry_measure_z = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            state=DISABLED,
            string_var=variables.entry_measure_z_text,
        )
        self.entry_value_z = NumberEntry(
            frames.values,
            width=12,
            style="Global.TEntry",
            string_var=variables.entry_value_z_text,
        )

        self.lbl_value_z.grid(row=2, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.entry_measure_z.grid(row=2, column=1, padx=(5, 1), pady=(3, 3), sticky="w")
        self.lbl_values_slash.grid(
            row=2, column=2, padx=(1, 1), pady=(3, 3), sticky="w"
        )
        self.entry_value_z.grid(row=2, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        self.lbl_values_unit.grid(row=2, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # RESULTS
        self.lbl_result_header = ttk.Label(
            frames.result_header,
            text="Result",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_result_header.grid(
            row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w"
        )

        self.lbl_result_current = ttk.Label(
            frames.result, text="Current value", cursor="arrow", width=12
        )
        self.entry_result_current = ttk.Entry(
            frames.result,
            width=38,
            style="Global.TEntry",
            state=DISABLED,
            textvariable=variables.entry_result_current_text,
        )
        self.lbl_result_new = ttk.Label(
            frames.result, text="New value", cursor="arrow", width=12
        )
        self.entry_result_new = ttk.Entry(
            frames.result,
            width=38,
            style="Global.TEntry",
            textvariable=variables.entry_result_new_text,
        )

        self.lbl_result_current.grid(
            row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w"
        )
        self.entry_result_current.grid(
            row=0, column=1, padx=(5, 5), pady=(3, 3), sticky="w"
        )

        self.lbl_result_new.grid(row=1, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.entry_result_new.grid(
            row=1, column=1, padx=(5, 5), pady=(3, 3), sticky="w"
        )

        # FOOTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.btn_save = ttk.Button(
            frames.footer,
            text="Save",
            # command=self.on_btn_save,
            style="Footer.TButton",
        )
        self.btn_abort = ttk.Button(
            frames.footer,
            text="Abort",
            # command=self.on_btn_abort,
            style="Footer.TButton",
        )

        self.btn_save.place(rely=1.0, relx=1.0, x=-115, y=-15, anchor=SE)
        self.btn_abort.place(rely=1.0, relx=1.0, x=-15, y=-15, anchor=SE)
