"""
    Callback submodule for the app.
"""

import tkinter as tk
from tkinter import messagebox as tkmsg

from pytia.const import USERNAME
from pytia.log import log
from pytia_ui_tools.handlers.workspace_handler import Workspace
from resources import resource

from app.helper import LazyPartHelper
from app.layout import Layout
from app.loaders import Loaders
from app.vars import Variables


class Callbacks:
    """The Callbacks class. Handles all callbacks and bindings from the main apps widgets."""

    def __init__(
        self,
        root: tk.Tk,
        variables: Variables,
        lazy_part_helper: LazyPartHelper,
        layout: Layout,
        loaders: Loaders,
        workspace: Workspace,
    ) -> None:
        """
        Inits the Callbacks class. Adds callbacks and bindings to the widgets on instantiation.

        Args:
            root (tk.Tk): The main app window.
            vars (Variables): The main app variables.
            lazy_part_helper (LazyPartHelper): The lazy part helper instance.
            layout (Layout): The main app layout.
            loaders (Loaders): The loaders instance.
            workspace (Workspace): The workspace instance.
        """ """"""
        self.root = root
        self.vars = variables
        self.part_helper = lazy_part_helper
        self.layout = layout
        self.loaders = loaders
        self.workspace = workspace

        self.readonly = bool(
            not resource.user_exists(USERNAME)
            and not resource.settings.restrictions.allow_all_users
        )

        self._add_callbacks()
        self._add_bindings()

    def _add_callbacks(self) -> None:
        """Adds callbacks to the widgets."""
        self.layout.scale_offset.configure(command=self.callback_scale_offset)
        self.layout.scale_step.configure(command=self.callback_scale_step)
        self.layout.chkbox_thickness.configure(command=self.callback_thickness)
        self.layout.btn_save.configure(command=self.on_btn_save)
        self.layout.btn_abort.configure(command=self.on_btn_abort)

    def _add_bindings(self) -> None:
        """Adds bindings to the widgets."""
        self.layout.combo_preset.bind(
            "<<ComboboxSelected>>", self.callback_combobox_preset
        )
        self.layout.combo_axis.bind("<<ComboboxSelected>>", self.callback_combobox_axis)

    def on_btn_save(self) -> None:
        """Event handler for the OK button."""
        log.info("User pressed OK button.")

        if not self.workspace.elements.active:
            tkmsg.showinfo(
                message=(
                    "This workspace is disabled. You cannot make changes to this document."
                )
            )
            return

        if self.readonly:
            log.warning(
                f"Did not save values to the part properties: {USERNAME} is not available in the "
                "user configuration."
            )
            tkmsg.showinfo(
                title=resource.settings.title,
                message=(
                    f"You are not allowed to save to the part properties: {USERNAME} is not "
                    "available in the user configuration."
                ),
            )
            return

        if (
            self.workspace.elements.editors
            and USERNAME not in self.workspace.elements.editors
            and not resource.settings.restrictions.allow_all_editors
        ):
            tkmsg.showinfo(
                message=(
                    f"You are not allowed to make changes to the part properties: {USERNAME} is "
                    f"not available in the workspace configuration."
                )
            )
            return

        self.part_helper.write_property(
            resource.props.base_size, self.layout.entry_result_new.get()
        )
        self.part_helper.write_property(
            resource.props.base_size_preset, self.vars.selected_preset.name
        )
        self.part_helper.write_modifier()

        if resource.settings.restrictions.enable_information:
            for msg in resource.get_info_msg_by_counter():
                tkmsg.showinfo(
                    title=resource.settings.title, message=f"Did you know:\n\n{msg}"
                )

        self.root.withdraw()
        self.root.destroy()

    def on_btn_abort(self) -> None:
        """Event handler for the abort button."""
        log.info("User pressed Abort button.")
        self.root.withdraw()
        self.root.destroy()

    def callback_combobox_preset(self, _: tk.Event) -> None:
        """Callback for the presets combo box widget."""
        log.info(
            f"Callback Combobox Preset: User selected {self.layout.combo_preset.get()!r}"
        )
        self.vars.pre_selected_preset_reason = ""

        self.loaders.load_combobox_preset()
        self.loaders.load_combobox_axis()
        self.loaders.load_scale_offset()
        self.loaders.load_scale_step()
        self.loaders.load_chkbox_thickness()
        self.loaders.load_calculated()
        self.loaders.load_result()

    def callback_combobox_axis(self, _: tk.Event) -> None:
        """Callback for the axis combo box widget."""
        log.info(
            f"Callback Combobox Axis: User selected {self.layout.combo_axis.get()!r}"
        )
        self.loaders.load_combobox_axis()
        self.loaders.load_calculated()
        self.loaders.load_result()

    def callback_scale_offset(self) -> None:
        """Callback for the offset scale widget."""
        log.info(
            f"Callback Scale Offset: User selected {self.layout.scale_offset.get()!r}"
        )
        self.loaders.load_calculated()
        self.loaders.load_result()

    def callback_scale_step(self) -> None:
        """Callback for the step scale widget."""
        log.info(f"Callback Scale Step: User selected: {self.layout.scale_step.get()}")
        self.loaders.load_calculated()
        self.loaders.load_result()

    def callback_thickness(self) -> None:
        """Callback for the thickness checkbox widget."""
        log.info(
            f"Callback Checkbox Thickness: User selected: {self.vars.thickness_value.get()}"
        )
        self.loaders.load_result()
