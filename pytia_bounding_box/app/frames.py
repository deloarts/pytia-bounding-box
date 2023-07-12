"""
    Frames submodule for the app. Holds all frames for the main app.
"""

from tkinter import Tk, X, ttk


class Frames:
    """The Frames class. Holds all frames for the main app."""

    def __init__(self, root: Tk) -> None:
        """
        Inits the Frames class. Provides the main app frames as properties.

        Args:
            root (Tk): The main window of the application.
        """
        self._fr_main_selection = ttk.Labelframe(
            root, style="Selection.TLabelframe", text="Selection"
        )
        self._fr_main_values = ttk.Labelframe(
            root, style="Values.TLabelframe", text="Values"
        )
        self._fr_main_result = ttk.Labelframe(
            root, style="Result.TLabelframe", text="Result"
        )
        self._fr_footer = ttk.Frame(root, height=50, style="Footer.TFrame")

        self._fr_main_selection.grid(
            row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 5)
        )
        self._fr_main_values.grid(
            row=1, column=0, sticky="nsew", padx=(10, 10), pady=(5, 5)
        )
        self._fr_main_result.grid(
            row=2, column=0, sticky="nsew", padx=(10, 10), pady=(5, 5)
        )
        self._fr_footer.grid(row=3, column=0, sticky="swe", padx=10, pady=(5, 10))

    @property
    def selection(self) -> ttk.Labelframe:
        """Return the frame of the selection."""
        return self._fr_main_selection

    @property
    def values(self) -> ttk.Labelframe:
        """Return the frame of the values."""
        return self._fr_main_values

    @property
    def result(self) -> ttk.Labelframe:
        """Return the frame of the result."""
        return self._fr_main_result

    @property
    def footer(self) -> ttk.Frame:
        """Return the footer frame."""
        return self._fr_footer
