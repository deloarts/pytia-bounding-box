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
        self.layout.input_preset["state"] = tk.DISABLED
        self.layout.input_axis["state"] = tk.DISABLED
        self.layout.input_offset["state"] = tk.DISABLED
        self.layout.input_step["state"] = tk.DISABLED
        self.layout.input_thickness["state"] = tk.DISABLED
        self.layout.input_x["state"] = tk.DISABLED
        self.layout.input_y["state"] = tk.DISABLED
        self.layout.input_z["state"] = tk.DISABLED
        self.layout.input_result["state"] = tk.DISABLED
        self.layout.button_save["state"] = tk.DISABLED
        self.layout.button_abort["state"] = tk.DISABLED
        self.root.update()

    def normal(self) -> None:
        """Sets the main windows state to normal."""
        self.root.config(cursor="wait")
        self.root.update()
        self.layout.input_preset["state"] = "readonly"
        self.layout.input_axis["state"] = "readonly"
        self.layout.input_offset["state"] = tk.NORMAL
        self.layout.input_step["state"] = tk.NORMAL
        # self.layout.input_thickness["state"] = tk.NORMAL
        self.layout.input_x["state"] = tk.NORMAL
        self.layout.input_y["state"] = tk.NORMAL
        self.layout.input_z["state"] = tk.NORMAL
        self.layout.input_result["state"] = tk.NORMAL
        self.layout.button_save["state"] = tk.NORMAL
        self.layout.button_abort["state"] = tk.NORMAL
        self.root.config(cursor="arrow")
        self.root.update()
