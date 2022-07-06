"""
    The state submodule of this app. Takes care of the apps widgets' state.
"""

import tkinter as tk

from app.layout import Layout


class UISetter:
    """The UISetter class, responsible for providing methods that can alter the widgets' state."""

    def __init__(
        self,
        root: tk.Tk,
        layout: Layout,
    ) -> None:
        """
        Initialize the UISetter class.

        Args:
            root (tk.Tk): The main window of the application.
            layout (Layout): The main layout of the application.
        """
        self.root = root
        self.layout = layout

    def busy(self) -> None:
        """Sets the main windows state to busy."""
        self.root.config(cursor="wait")
        self.root.update()
        self.layout.combo_preset["state"] = tk.DISABLED
        self.layout.combo_axis["state"] = tk.DISABLED
        self.layout.scale_offset["state"] = tk.DISABLED
        self.layout.scale_step["state"] = tk.DISABLED
        self.layout.chkbox_thickness["state"] = tk.DISABLED
        self.layout.entry_value_x["state"] = tk.DISABLED
        self.layout.entry_value_y["state"] = tk.DISABLED
        self.layout.entry_value_z["state"] = tk.DISABLED
        self.layout.entry_result_current["state"] = tk.DISABLED
        self.layout.entry_result_new["state"] = tk.DISABLED
        self.layout.btn_save["state"] = tk.DISABLED
        self.layout.btn_abort["state"] = tk.DISABLED
        self.root.update()

    def normal(self) -> None:
        """Sets the main windows state to normal."""
        self.root.config(cursor="wait")
        self.root.update()
        self.layout.combo_preset["state"] = "readonly"
        self.layout.combo_axis["state"] = "readonly"
        self.layout.scale_offset["state"] = tk.NORMAL
        self.layout.scale_step["state"] = tk.NORMAL
        self.layout.chkbox_thickness["state"] = tk.NORMAL
        self.layout.entry_value_x["state"] = tk.NORMAL
        self.layout.entry_value_y["state"] = tk.NORMAL
        self.layout.entry_value_z["state"] = tk.NORMAL
        self.layout.entry_result_current["state"] = tk.NORMAL
        self.layout.entry_result_new["state"] = tk.NORMAL
        self.layout.btn_save["state"] = tk.NORMAL
        self.layout.btn_abort["state"] = tk.NORMAL
        self.root.config(cursor="arrow")
        self.root.update()
