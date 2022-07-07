"""
    The validators submodule for this app.
"""

import re
import tkinter as tk

from pytia_ui_tools.widgets.tooltips import ToolTip

from app.layout import Layout
from app.vars import Variables


class Validators:
    """The Validators class. Responsible for providing the validators methods."""

    def __init__(self, variables: Variables, layout: Layout) -> None:
        """
        Inits the validators class. Adds

        Args:
            vars (Variables): The main window variables.
            layout (Layout): The main window layout.
        """ """"""
        self.vars = variables
        self.layout = layout

    def validate_result(self) -> None:
        """
        Validates the calculated values according to the filter
        specified in the preset config file. Sets the state of
        the OK button accordingly to the validation result.
        """

        if re.match(
            self.vars.selected_preset.result_filter,
            self.vars.entry_result_new_text.get(),
        ):
            self.layout.button_save["state"] = tk.NORMAL
            ToolTip(self.layout.button_save, "")
        else:
            self.layout.button_save["state"] = tk.DISABLED
            examples = [f"\n  {e}" for e in self.vars.selected_preset.filter_examples]
            ToolTip(
                self.layout.button_save,
                f"Value cannot be validated against the filter:\n\n"
                f"{self.vars.selected_preset.result_filter}\n\n"
                f"Examples for this filter:{''.join(examples)}\n\n"
                f"Note: Whitespaces at the beginning ot at the end are not allowed.",
                250,
            )
