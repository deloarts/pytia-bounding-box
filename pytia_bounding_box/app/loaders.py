"""
    The loaders submodule of the app. Holds all loader methods in the Loaders class.
"""

import tkinter as tk

from const import Axes
from pytia_ui_tools.widgets.tooltips import ToolTip
from resources import resource

from app.helper import LazyPartHelper, get_offset, get_preferred_axis, sort_base_size
from app.layout import Layout
from app.state import UISetter
from app.validators import Validators
from app.vars import Variables


class Loaders:
    """The Loaders class. Provides access to the loader methods."""

    def __init__(
        self,
        root: tk.Tk,
        variables: Variables,
        validators: Validators,
        lazy_part_helper: LazyPartHelper,
        layout: Layout,
        ui_setter: UISetter,
    ) -> None:
        """
        Inits the Loaders class. This class is responsible for providing the loader methods.

        Args:
            root (tk.Tk): The main window of the application.
            vars (Variables): The variables of the main window.
            validators (Validators): The validators instance.
            lazy_part_helper (LazyPartHelper): The lazy part helper instance.
            layout (Layout): The main layout of the application.
            ui_setter (UISetter): The ui setter of the main window.
        """
        self.root = root
        self.vars = variables
        self.validators = validators
        self.part_helper = lazy_part_helper
        self.layout = layout
        self.set_ui = ui_setter

    def load_existing_base_size(self) -> None:
        """Loads the pre-existing base size from the part document to the UI."""
        if prop := self.part_helper.get_property(resource.props.base_size):
            self.vars.entry_result_current_text.set(prop)
        else:
            self.vars.entry_result_current_text.set("")

    def load_measurements(self) -> None:
        """Retrieves the base size from the body and writes the values to the UI."""
        self.set_ui.busy()

        # Late importing improves the GUI loading time.
        # pylint: disable=C0415
        from pytia.utilities.bounding_box import get_bounding_box

        # pylint: enable=C0415

        (
            self.vars.x_measure,
            self.vars.y_measure,
            self.vars.z_measure,
        ) = get_bounding_box(n_digits=resource.settings.precision)

        self.vars.entry_measure_x_text.set(str(self.vars.x_measure))
        self.vars.entry_measure_y_text.set(str(self.vars.y_measure))
        self.vars.entry_measure_z_text.set(str(self.vars.z_measure))
        self.set_ui.normal()

    def load_process(self) -> None:
        """
        Loads the process property from the part document.
        Pre-selects the preset-combobox by this process or
        on an the existing preset from the parts properties.

        Always favors the existing preset from the parts properties.
        """
        self.set_ui.busy()

        preset_property = self.part_helper.get_property(resource.props.base_size_preset)
        if preset_property and resource.preset_exists(preset_property):
            self.layout.input_preset.set(preset_property)
            self.vars.pre_selected_preset_reason = (
                "This preset has been pre-selected because it "
                "already existed in the part properties.\n\n"
            )
            self.set_ui.normal()
            return

        process_property = self.part_helper.get_property(resource.props.process)
        if process_property and resource.process_exists(process_property):
            process = resource.get_process_by_name(process_property)
            if resource.preset_exists(process.preset):
                self.layout.input_preset.set(process.preset)
                self.vars.pre_selected_preset_reason = (
                    f"This preset has been pre-selected because of the process "
                    f"property {process_property!r}.\n\n"
                )
                self.set_ui.normal()
                return

        self.set_ui.normal()

    def load_combobox_preset(self) -> None:
        """
        Loads the selected preset from the preset-combobox to the UI.
        Pre-selects the axis based on the preference from the presets config file.

        Requires valid measurements.
        """
        self.vars.selected_preset = resource.get_preset_by_name(
            self.layout.input_preset.get()
        )
        self.layout.input_axis.set(
            get_preferred_axis(
                self.vars.x_measure,
                self.vars.y_measure,
                self.vars.z_measure,
                self.vars.selected_preset,
            ).value
        )
        ToolTip(
            self.layout.input_preset,
            text=self.vars.pre_selected_preset_reason
            + self.vars.selected_preset.tooltip,
        )

    def load_combobox_axis(self) -> None:
        """
        Loads the selected axis based on the preference from the
        presets config file to the UI.

        Disables the axis-combobox when no preference is specified.
        """
        if self.vars.selected_preset.preference:
            self.layout.input_axis["state"] = "readonly"
            self.vars.selected_axis = Axes(self.layout.input_axis.get())
        else:
            self.layout.input_axis["state"] = tk.DISABLED
            self.vars.selected_axis = Axes.X

    def load_scale_offset(self) -> None:
        """
        Loads the offset value according to the presets config file to the UI.
        Disables the offset-scale when no offset is specified.
        """
        if self.vars.selected_preset.offset:
            self.layout.input_offset["state"] = tk.NORMAL
            self.vars.scale_offset_value.set(self.vars.selected_preset.offset)
        else:
            self.layout.input_offset["state"] = tk.DISABLED
            self.vars.scale_offset_value.set(0)

    def load_scale_step(self) -> None:
        """
        Loads the step value according to the presets config file to the UI.
        Disables the offset-scale when no offset is specified.
        """
        if self.vars.selected_preset.offset:
            self.layout.input_step["state"] = tk.NORMAL
            self.vars.scale_step_value.set(self.vars.selected_preset.step)
        else:
            self.layout.input_step["state"] = tk.DISABLED
            self.vars.scale_step_value.set(0)

    def load_chkbox_thickness(self) -> None:
        """
        Loads the thickness checkbox depending on the presets config file and
        the available part parameters.
        """
        if self.vars.selected_preset.coord == 4:
            thickness_param = self.part_helper.get_parameter(
                resource.settings.parameters.thickness
            )
            if thickness_param:
                self.vars.thickness_value.set(True)
                self.layout.input_thickness["state"] = tk.NORMAL
                self.layout.input_thickness[
                    "text"
                ] = f"({resource.settings.parameters.thickness}: {thickness_param})"
                return

        self.vars.thickness_value.set(False)
        self.layout.input_thickness["state"] = tk.DISABLED
        self.layout.input_thickness["text"] = ""

    def load_calculated(self) -> None:
        """
        Calculates the offset for the measurements according to the preset
        config file. Loads the calculated values to the UI.

        Requires valid measurements.
        """
        x_calc, y_calc, z_calc = get_offset(
            self.vars.x_measure,
            self.vars.y_measure,
            self.vars.z_measure,
            self.vars.selected_preset,
            self.vars.selected_axis,
            self.vars.scale_offset_value,
            self.vars.scale_step_value,
        )
        self.vars.entry_value_x_text.set(str(x_calc))
        self.vars.entry_value_y_text.set(str(y_calc))
        self.vars.entry_value_z_text.set(str(z_calc))

    def load_result(self) -> None:
        """
        Loads the result from the calculated values to the UI.
        Validates the calculated values according to the filter
        specified in the preset config file.

        Requires valid calculated values.
        """
        value = sort_base_size(
            self.vars.entry_value_x_text.get(),
            self.vars.entry_value_y_text.get(),
            self.vars.entry_value_z_text.get(),
            self.vars.selected_preset,
            self.vars.selected_axis,
            self.vars.thickness_value,
        )
        self.vars.entry_result_new_text.set(value)
        self.validators.validate_result()
