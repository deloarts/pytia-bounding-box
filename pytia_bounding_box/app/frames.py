"""
    Frames submodule for the app. Holds all frames for the main app.
"""

from tkinter import Tk

from ttkbootstrap import Frame
from ttkbootstrap import Labelframe


class Frames:
    """The Frames class. Holds all frames for the main app."""

    def __init__(self, root: Tk) -> None:
        """
        Inits the Frames class. Provides the main app frames as properties.

        Args:
            root (Tk): The main window of the application.
        """
        root.columnconfigure(0, weight=1)
        root.rowconfigure(3, weight=1)

        self._fr_main_selection = Labelframe(root, text="Selection")
        self._fr_main_selection.grid(
            row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 5)
        )
        self._fr_main_selection.grid_columnconfigure(1, weight=1)

        self._fr_main_values = Labelframe(root, text="Values")
        self._fr_main_values.grid(
            row=1, column=0, sticky="nsew", padx=(10, 10), pady=(5, 5)
        )
        self._fr_main_values.grid_columnconfigure(1, weight=1)

        self._fr_main_result = Labelframe(root, text="Result")
        self._fr_main_result.grid(
            row=2, column=0, sticky="nsew", padx=(10, 10), pady=(5, 5)
        )
        self._fr_main_result.grid_columnconfigure(1, weight=1)

        self._fr_footer = Frame(root, height=30)
        self._fr_footer.grid(row=3, column=0, sticky="swe", padx=10, pady=(5, 10))
        self._fr_footer.grid_columnconfigure(1, weight=1)

    @property
    def selection(self) -> Labelframe:
        """Return the frame of the selection."""
        return self._fr_main_selection

    @property
    def values(self) -> Labelframe:
        """Return the frame of the values."""
        return self._fr_main_values

    @property
    def result(self) -> Labelframe:
        """Return the frame of the result."""
        return self._fr_main_result

    @property
    def footer(self) -> Frame:
        """Return the footer frame."""
        return self._fr_footer
