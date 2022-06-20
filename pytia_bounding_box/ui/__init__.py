"""
    The toplevel frame for the application.
"""

import re
import time
import tkinter as tk
from tkinter import font
from tkinter import messagebox as tkmsg
from tkinter import ttk

from const import APP_VERSION, LOG, LOGS, Axes
from pytia.const import USERNAME
from pytia.exceptions import (
    PytiaBodyEmptyError,
    PytiaDifferentDocumentError,
    PytiaNoDocumentOpenError,
    PytiaPropertyNotFoundError,
    PytiaWrongDocumentTypeError,
)
from pytia.log import log
from pytia_ui_tools.handlers.error_handler import ErrorHandler
from pytia_ui_tools.handlers.mail_handler import MailHandler
from pytia_ui_tools.widgets.entries import NumberEntry
from pytia_ui_tools.widgets.scales import SnapScale
from pytia_ui_tools.widgets.tooltips import ToolTip
from pytia_ui_tools.window_manager import WindowManager
from resources import resource

from ui.decorators import busy
from ui.helper import (
    LazyPartHelper,
    get_offset,
    get_preferred_axis,
    show_help,
    sort_base_size,
)

t0 = time.perf_counter()


class GUI(tk.Tk):
    """The user interface of the app."""

    HEIGHT = 470
    WIDTH = 365

    def __init__(self) -> None:
        tk.Tk.__init__(self)

        # CLASS VARS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.x_measure = 0.0
        self.y_measure = 0.0
        self.z_measure = 0.0

        self.scale_offset_value = tk.IntVar()
        self.scale_step_value = tk.IntVar()
        self.thickness_value = tk.BooleanVar()

        self.entry_measure_x_text = tk.StringVar()
        self.entry_measure_y_text = tk.StringVar()
        self.entry_measure_z_text = tk.StringVar()

        self.entry_value_x_text = tk.StringVar()
        self.entry_value_y_text = tk.StringVar()
        self.entry_value_z_text = tk.StringVar()

        self.entry_result_current_text = tk.StringVar()
        self.entry_result_new_text = tk.StringVar()

        self.part_helper: LazyPartHelper  # Instantiate later for performance improvement
        self.selected_preset = resource.presets[0]
        self.selected_axis: Axes = Axes.X
        self.pre_selected_preset_reason = ""

        self.readonly = bool(
            not resource.user_exists(USERNAME) and not resource.settings.allow_all_users
        )

        # UI TOOLS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.window_manager = WindowManager(self)
        self.mail_handler = MailHandler(
            standard_receiver=resource.settings.mails.admin,
            app_title=resource.settings.title,
            app_version=APP_VERSION,
            logfile=f"{LOGS}\\{LOG}",
        )
        self.error_handler = ErrorHandler(
            mail_handler=self.mail_handler,
            warning_exceptions=[
                PytiaNoDocumentOpenError,
                PytiaWrongDocumentTypeError,
                PytiaBodyEmptyError,
                PytiaPropertyNotFoundError,
                PytiaDifferentDocumentError,
            ],
        )

        # UI INIT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.title(
            f"{resource.settings.title} "
            f"{'(DEBUG MODE)' if resource.settings.debug else APP_VERSION}"
            f"{' (READ ONLY)' if self.readonly else ''}"
        )
        # self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.config(cursor="wait")
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Segoe UI", size=10)
        self.report_callback_exception = self.error_handler.exceptions_callback

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (GUI.WIDTH / 2))
        y_coordinate = int((screen_height / 2) - (GUI.HEIGHT / 2))
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}+{x_coordinate}+{y_coordinate}")

        # STYLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        style = ttk.Style(self)
        style.configure("Grey.TCheckbutton", foreground="grey")

        # LAYOUT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        fr_main = ttk.Frame(self, style="Main.TFrame")
        fr_main_selection_header = ttk.Frame(fr_main, style="Main.TFrame")
        fr_main_selection = ttk.Frame(fr_main, style="Main.TFrame")
        fr_main_values_header = ttk.Frame(fr_main, style="Main.TFrame")
        fr_main_values = ttk.Frame(fr_main, style="Main.TFrame")
        fr_main_result_header = ttk.Frame(fr_main, style="Main.TFrame")
        fr_main_result = ttk.Frame(fr_main, style="Main.TFrame")
        fr_footer = ttk.Frame(self, height=50, style="Footer.TFrame")

        fr_main.pack(fill="both", expand=True)
        fr_main_selection_header.pack(fill=tk.X)
        fr_main_selection.pack(fill=tk.X)
        fr_main_values_header.pack(fill=tk.X)
        fr_main_values.pack(fill=tk.X)
        fr_main_result_header.pack(fill=tk.X)
        fr_main_result.pack(fill=tk.X)
        fr_footer.pack(fill=tk.X)

        # HEADER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # SELECTIONS
        self.lbl_selection_header = ttk.Label(
            fr_main_selection_header,
            text="Selection",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_selection_header.grid(
            row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w"
        )

        # PRESET SELECTION
        self.lbl_preset = ttk.Label(
            fr_main_selection, text="Preset", cursor="arrow", width=12
        )

        self.combo_preset = ttk.Combobox(
            fr_main_selection,
            values=[ts.name for ts in resource.presets],
            width=35,
            state="readonly",
        )
        self.combo_preset.current(0)
        self.combo_preset.bind("<<ComboboxSelected>>", self.callback_combobox_preset)

        self.lbl_preset.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.combo_preset.grid(row=0, column=1, padx=(5, 5), pady=(3, 3), sticky="w")

        # AXIS SELECTION
        self.lbl_axis = ttk.Label(
            fr_main_selection, text="Axis", cursor="arrow", width=12
        )

        self.combo_axis = ttk.Combobox(
            fr_main_selection,
            values=[a.value for a in Axes],
            width=35,
            state="readonly",
        )
        self.combo_axis.current(0)
        self.combo_axis.bind("<<ComboboxSelected>>", self.callback_combobox_axis)

        self.lbl_axis.grid(row=1, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.combo_axis.grid(row=1, column=1, padx=(5, 5), pady=(3, 3), sticky="w")

        # OFFSET SELECTION
        self.lbl_offset = ttk.Label(
            fr_main_selection, text="Offset", cursor="arrow", width=12
        )
        self.scale_offset = SnapScale(
            fr_main_selection,
            int_var=self.scale_offset_value,
            from_=resource.settings.offset.min,
            to=resource.settings.offset.max,
            tick=resource.settings.offset.tick,
            length=180,
            orient="horizontal",
            command=self.callback_scale_offset,
        )
        self.lbl_offset_value = ttk.Label(
            fr_main_selection,
            textvariable=self.scale_offset_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        self.lbl_offset_unit = ttk.Label(fr_main_selection, text="mm", cursor="arrow")

        self.lbl_offset.grid(row=2, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.scale_offset.grid(row=2, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        self.lbl_offset_value.place(x=300, y=55)
        self.lbl_offset_unit.place(x=318, y=55)

        # STEP SELECTION
        self.lbl_step = ttk.Label(
            fr_main_selection, text="Step", cursor="arrow", width=12
        )
        self.scale_step = SnapScale(
            fr_main_selection,
            int_var=self.scale_step_value,
            from_=resource.settings.step.min,
            to=resource.settings.step.max,
            tick=resource.settings.step.tick,
            length=180,
            orient="horizontal",
            command=self.callback_scale_step,
        )
        self.lbl_step_value = ttk.Label(
            fr_main_selection,
            textvariable=self.scale_step_value,
            cursor="arrow",
            width=2,
            anchor="e",
        )
        self.lbl_step_unit = ttk.Label(fr_main_selection, text="mm", cursor="arrow")

        self.lbl_step.grid(row=3, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.scale_step.grid(row=3, column=1, padx=(5, 5), pady=(1, 1), sticky="w")
        self.lbl_step_value.place(x=300, y=84)
        self.lbl_step_unit.place(x=318, y=84)

        # THICKNESS
        self.lbl_thickness = ttk.Label(
            fr_main_selection, text="Thickness", cursor="arrow", width=12
        )
        self.chkbox_thickness = ttk.Checkbutton(
            fr_main_selection,
            variable=self.thickness_value,
            onvalue=1,
            offvalue=0,
            style="Grey.TCheckbutton",
            command=self.callback_thickness,
        )
        self.lbl_thickness.grid(row=4, column=0, padx=(15, 3), pady=(3, 3), sticky="w")
        self.chkbox_thickness.grid(
            row=4, column=1, padx=(3, 5), pady=(3, 3), sticky="w"
        )

        # MEASURE AND SELECTED VALUE
        self.lbl_values_header = ttk.Label(
            fr_main_values_header,
            text="Measured / Selected",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_values_header.grid(
            row=0, column=0, padx=(15, 5), pady=(15, 5), sticky="w"
        )

        # X-AXIS
        self.lbl_values_unit = ttk.Label(fr_main_values, text="mm", cursor="arrow")
        self.lbl_values_slash = ttk.Label(fr_main_values, text="mm  / ", cursor="arrow")
        self.lbl_value_x = ttk.Label(
            fr_main_values,
            text=Axes.X.value,
            cursor="arrow",
            width=12,
        )
        self.entry_measure_x = NumberEntry(
            fr_main_values,
            width=12,
            style="Global.TEntry",
            state=tk.DISABLED,
            string_var=self.entry_measure_x_text,
        )
        self.entry_value_x = NumberEntry(
            fr_main_values,
            width=12,
            style="Global.TEntry",
            string_var=self.entry_value_x_text,
        )

        self.lbl_value_x.grid(row=0, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.entry_measure_x.grid(row=0, column=1, padx=(5, 1), pady=(3, 3), sticky="w")
        self.lbl_values_slash.grid(
            row=0, column=2, padx=(1, 1), pady=(3, 3), sticky="w"
        )
        self.entry_value_x.grid(row=0, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        self.lbl_values_unit.grid(row=0, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # Y-AXIS
        self.lbl_values_unit = ttk.Label(fr_main_values, text="mm", cursor="arrow")
        self.lbl_values_slash = ttk.Label(fr_main_values, text="mm  / ", cursor="arrow")
        self.lbl_value_y = ttk.Label(
            fr_main_values,
            text=Axes.Y.value,
            cursor="arrow",
            width=12,
        )
        self.entry_measure_y = NumberEntry(
            fr_main_values,
            width=12,
            style="Global.TEntry",
            state=tk.DISABLED,
            string_var=self.entry_measure_y_text,
        )
        self.entry_value_y = NumberEntry(
            fr_main_values,
            width=12,
            style="Global.TEntry",
            string_var=self.entry_value_y_text,
        )

        self.lbl_value_y.grid(row=1, column=0, padx=(15, 5), pady=(3, 3), sticky="w")
        self.entry_measure_y.grid(row=1, column=1, padx=(5, 1), pady=(3, 3), sticky="w")
        self.lbl_values_slash.grid(
            row=1, column=2, padx=(1, 1), pady=(3, 3), sticky="w"
        )
        self.entry_value_y.grid(row=1, column=4, padx=(1, 1), pady=(3, 3), sticky="w")
        self.lbl_values_unit.grid(row=1, column=5, padx=(1, 1), pady=(3, 3), sticky="w")

        # Z-AXIS
        self.lbl_values_unit = ttk.Label(fr_main_values, text="mm", cursor="arrow")
        self.lbl_values_slash = ttk.Label(fr_main_values, text="mm  / ", cursor="arrow")
        self.lbl_value_z = ttk.Label(
            fr_main_values,
            text=Axes.Z.value,
            cursor="arrow",
            width=12,
        )
        self.entry_measure_z = NumberEntry(
            fr_main_values,
            width=12,
            style="Global.TEntry",
            state=tk.DISABLED,
            string_var=self.entry_measure_z_text,
        )
        self.entry_value_z = NumberEntry(
            fr_main_values,
            width=12,
            style="Global.TEntry",
            string_var=self.entry_value_z_text,
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
            fr_main_result_header,
            text="Result",
            cursor="arrow",
            font=("Segoe UI", 10, "bold"),
        )
        self.lbl_result_header.grid(
            row=0, column=0, padx=(15, 3), pady=(15, 3), sticky="w"
        )

        self.lbl_result_current = ttk.Label(
            fr_main_result, text="Current value", cursor="arrow", width=12
        )
        self.entry_result_current = ttk.Entry(
            fr_main_result,
            width=38,
            style="Global.TEntry",
            state=tk.DISABLED,
            textvariable=self.entry_result_current_text,
        )
        self.lbl_result_new = ttk.Label(
            fr_main_result, text="New value", cursor="arrow", width=12
        )
        self.entry_result_new = ttk.Entry(
            fr_main_result,
            width=38,
            style="Global.TEntry",
            textvariable=self.entry_result_new_text,
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
            fr_footer,
            text="Save",
            command=self.on_btn_save,
            style="Footer.TButton",
        )
        self.btn_abort = ttk.Button(
            fr_footer,
            text="Abort",
            command=self.on_btn_abort,
            style="Footer.TButton",
        )

        self.btn_save.place(rely=1.0, relx=1.0, x=-115, y=-15, anchor=tk.SE)
        self.btn_abort.place(rely=1.0, relx=1.0, x=-15, y=-15, anchor=tk.SE)

        self.bindings()
        self.update()
        self.window_manager.remove_window_buttons()

    def run(self) -> None:
        """Run the app."""
        t1 = time.perf_counter()  # pylint: disable=C0103
        log.info(f"Loaded UI in {(t1-t0):.4f}s")

        self.after(100, self.run_controller)
        self.mainloop()

    def run_controller(self) -> None:
        """Runs all controllers. Initializes all lazy loaders."""
        self.part_helper = LazyPartHelper()
        self.main_controller()

    def main_controller(self) -> None:
        """The main controller: Loads and calculates the bounding box."""
        self.load_process()
        self.load_measurements()
        self.load_combobox_preset()
        self.load_combobox_axis()
        self.load_chkbox_thickness()
        self.load_scale_offset()
        self.load_scale_step()
        self.load_existing_base_size()
        self.load_calculated()
        self.load_result()

    def bindings(self) -> None:
        """Key bindings."""
        self.bind("<Escape>", lambda _: self.destroy())
        self.bind("<F1>", lambda _: show_help())
        self.bind("<F5>", lambda _: self.main_controller())
        self.bind("<Button-2>", lambda _: self.on_btn_save())

        self.entry_value_x.bind("<KeyRelease>", lambda _: self.load_result())
        self.entry_value_y.bind("<KeyRelease>", lambda _: self.load_result())
        self.entry_value_z.bind("<KeyRelease>", lambda _: self.load_result())
        self.entry_result_new.bind("<KeyRelease>", lambda _: self.validate_result())

    def on_btn_save(self) -> None:
        """Event handler for the OK button."""
        log.info("User pressed OK button.")

        if not self.readonly:
            self.part_helper.write_property(
                resource.props.base_size, self.entry_result_new.get()
            )
            self.part_helper.write_property(
                resource.props.base_size_preset, self.selected_preset.name
            )
            self.part_helper.write_modifier()

            if resource.settings.enable_information:
                for msg in resource.get_info_msg_by_counter():
                    tkmsg.showinfo(
                        title=resource.settings.title, message=f"Did you know:\n\n{msg}"
                    )

            self.withdraw()
            self.destroy()

        else:
            log.warning(
                f"Did not save values to the part properties: {USERNAME} is not available in the "
                f"user configuration."
            )
            tkmsg.showwarning(
                title=resource.settings.title,
                message=(
                    f"You are not allowed to save to the part properties: {USERNAME} is not "
                    f"available in the user configuration."
                ),
            )

    def on_btn_abort(self) -> None:
        """Event handler for the abort button."""
        log.info("User pressed Abort button.")
        self.withdraw()
        self.destroy()

    def callback_combobox_preset(self, _: tk.Event) -> None:
        """Callback for the presets combo box widget."""
        log.info(f"Callback Combobox Preset: User selected {self.combo_preset.get()!r}")
        self.pre_selected_preset_reason = ""

        self.load_combobox_preset()
        self.load_combobox_axis()
        self.load_scale_offset()
        self.load_scale_step()
        self.load_chkbox_thickness()
        self.load_calculated()
        self.load_result()

    def callback_combobox_axis(self, _: tk.Event) -> None:
        """Callback for the axis combo box widget."""
        log.info(f"Callback Combobox Axis: User selected {self.combo_axis.get()!r}")
        self.load_combobox_axis()
        self.load_calculated()
        self.load_result()

    def callback_scale_offset(self) -> None:
        """Callback for the offset scale widget."""
        log.info(f"Callback Scale Offset: User selected {self.scale_offset.get()!r}")
        self.load_calculated()
        self.load_result()

    def callback_scale_step(self) -> None:
        """Callback for the step scale widget."""
        log.info(f"Callback Scale Step: User selected: {self.scale_step.get()}")
        self.load_calculated()
        self.load_result()

    def callback_thickness(self) -> None:
        """Callback for the thickness checkbox widget."""
        log.info(
            f"Callback Checkbox Thickness: User selected: {self.thickness_value.get()}"
        )
        self.load_result()

    def load_existing_base_size(self) -> None:
        """Loads the pre-existing base size from the part document to the UI."""
        if prop := self.part_helper.get_property(resource.props.base_size):
            self.entry_result_current_text.set(prop)
        else:
            self.entry_result_current_text.set("")

    @busy
    def load_measurements(self) -> None:
        """Retrieves the base size from the body and writes the values to the UI."""
        # Late importing improves the GUI loading time.
        # pylint: disable=C0415
        from pytia.utilities.bounding_box import get_bounding_box

        # pylint: enable=C0415

        self.x_measure, self.y_measure, self.z_measure = get_bounding_box(
            n_digits=resource.settings.precision
        )

        self.entry_measure_x_text.set(str(self.x_measure))
        self.entry_measure_y_text.set(str(self.y_measure))
        self.entry_measure_z_text.set(str(self.z_measure))

    @busy
    def load_process(self) -> None:
        """
        Loads the process property from the part document.
        Pre-selects the preset-combobox by this process or
        on an the existing preset from the parts properties.

        Always favors the existing preset from the parts properties.
        """

        preset_property = self.part_helper.get_property(resource.props.base_size_preset)
        if preset_property and resource.preset_exists(preset_property):
            self.combo_preset.set(preset_property)
            self.pre_selected_preset_reason = (
                "This preset has been pre-selected because it "
                "already existed in the part properties.\n\n"
            )
            return

        process_property = self.part_helper.get_property(resource.props.process)
        if process_property and resource.process_exists(process_property):
            process = resource.get_process_by_name(process_property)
            if resource.preset_exists(process.preset):
                self.combo_preset.set(process.preset)
                self.pre_selected_preset_reason = (
                    f"This preset has been pre-selected because of the process "
                    f"property {process_property!r}.\n\n"
                )
                return

    def load_combobox_preset(self) -> None:
        """
        Loads the selected preset from the preset-combobox to the UI.
        Pre-selects the axis based on the preference from the presets config file.

        Requires valid measurements.
        """
        self.selected_preset = resource.get_preset_by_name(self.combo_preset.get())
        self.combo_axis.set(
            get_preferred_axis(
                self.x_measure,
                self.y_measure,
                self.z_measure,
                self.selected_preset,
            ).value
        )
        ToolTip(
            self.combo_preset,
            text=self.pre_selected_preset_reason + self.selected_preset.tooltip,
        )

    def load_combobox_axis(self) -> None:
        """
        Loads the selected axis based on the preference from the
        presets config file to the UI.

        Disables the axis-combobox when no preference is specified.
        """
        if self.selected_preset.preference:
            self.combo_axis["state"] = "readonly"
            self.selected_axis = Axes(self.combo_axis.get())
        else:
            self.combo_axis["state"] = tk.DISABLED
            self.selected_axis = Axes.X

    def load_scale_offset(self) -> None:
        """
        Loads the offset value according to the presets config file to the UI.
        Disables the offset-scale when no offset is specified.
        """
        if self.selected_preset.offset:
            self.scale_offset["state"] = tk.NORMAL
            self.scale_offset_value.set(self.selected_preset.offset)
        else:
            self.scale_offset["state"] = tk.DISABLED
            self.scale_offset_value.set(0)

    def load_scale_step(self) -> None:
        """
        Loads the step value according to the presets config file to the UI.
        Disables the offset-scale when no offset is specified.
        """
        if self.selected_preset.offset:
            self.scale_step["state"] = tk.NORMAL
            self.scale_step_value.set(self.selected_preset.step)
        else:
            self.scale_step["state"] = tk.DISABLED
            self.scale_step_value.set(0)

    def load_chkbox_thickness(self) -> None:
        """
        Loads the thickness checkbox depending on the presets config file and
        the available part parameters.
        """
        if self.selected_preset.coord == 4:
            thickness_param = self.part_helper.get_parameter(
                resource.settings.parameters.thickness
            )
            if thickness_param:
                self.thickness_value.set(True)
                self.chkbox_thickness["state"] = tk.NORMAL
                self.chkbox_thickness[
                    "text"
                ] = f"({resource.settings.parameters.thickness}: {thickness_param})"
                return

        self.thickness_value.set(False)
        self.chkbox_thickness["state"] = tk.DISABLED
        self.chkbox_thickness["text"] = ""

    def load_calculated(self) -> None:
        """
        Calculates the offset for the measurements according to the preset
        config file. Loads the calculated values to the UI.

        Requires valid measurements.
        """
        x_calc, y_calc, z_calc = get_offset(
            self.x_measure,
            self.y_measure,
            self.z_measure,
            self.selected_preset,
            self.selected_axis,
            self.scale_offset_value,
            self.scale_step_value,
        )
        self.entry_value_x_text.set(str(x_calc))
        self.entry_value_y_text.set(str(y_calc))
        self.entry_value_z_text.set(str(z_calc))

    def load_result(self) -> None:
        """
        Loads the result from the calculated values to the UI.
        Validates the calculated values according to the filter
        specified in the preset config file.

        Requires valid calculated values.
        """
        value = sort_base_size(
            self.entry_value_x_text.get(),
            self.entry_value_y_text.get(),
            self.entry_value_z_text.get(),
            self.selected_preset,
            self.selected_axis,
            self.thickness_value,
        )
        self.entry_result_new_text.set(value)
        self.validate_result()

    def validate_result(self) -> None:
        """
        Validates the calculated values according to the filter
        specified in the preset config file. Sets the state of
        the OK button accordingly to the validation result.
        """
        if re.match(
            self.selected_preset.result_filter, self.entry_result_new_text.get()
        ):
            self.btn_save["state"] = tk.NORMAL
            ToolTip(self.btn_save, "")
        else:
            self.btn_save["state"] = tk.DISABLED
            examples = [f"\n  {e}" for e in self.selected_preset.filter_examples]
            ToolTip(
                self.btn_save,
                f"Value cannot be validated against the filter:\n\n"
                f"{self.selected_preset.result_filter}\n\n"
                f"Examples for this filter:{''.join(examples)}\n\n"
                f"Note: Whitespaces at the beginning ot at the end are not allowed.",
                250,
            )
