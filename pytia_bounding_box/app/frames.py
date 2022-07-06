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
        """ """"""
        self._fr_main = ttk.Frame(root, style="Main.TFrame")
        self._fr_main_selection_header = ttk.Frame(self._fr_main, style="Main.TFrame")
        self._fr_main_selection = ttk.Frame(self._fr_main, style="Main.TFrame")
        self._fr_main_values_header = ttk.Frame(self._fr_main, style="Main.TFrame")
        self._fr_main_values = ttk.Frame(self._fr_main, style="Main.TFrame")
        self._fr_main_result_header = ttk.Frame(self._fr_main, style="Main.TFrame")
        self._fr_main_result = ttk.Frame(self._fr_main, style="Main.TFrame")
        self._fr_footer = ttk.Frame(root, height=50, style="Footer.TFrame")

        self._fr_main.pack(fill="both", expand=True)
        self._fr_main_selection_header.pack(fill=X)
        self._fr_main_selection.pack(fill=X)
        self._fr_main_values_header.pack(fill=X)
        self._fr_main_values.pack(fill=X)
        self._fr_main_result_header.pack(fill=X)
        self._fr_main_result.pack(fill=X)
        self._fr_footer.pack(fill=X)

    @property
    def selection_header(self) -> ttk.Frame:
        """Return the header frame of the selection."""
        return self._fr_main_selection_header

    @property
    def selection(self) -> ttk.Frame:
        """Return the frame of the selection."""
        return self._fr_main_selection

    @property
    def values_header(self) -> ttk.Frame:
        """Return the header frame of the values."""
        return self._fr_main_values_header

    @property
    def values(self) -> ttk.Frame:
        """Return the frame of the values."""
        return self._fr_main_values

    @property
    def result_header(self) -> ttk.Frame:
        """Return the header frame."""
        return self._fr_main_result_header

    @property
    def result(self) -> ttk.Frame:
        """Return the frame of the result."""
        return self._fr_main_result

    @property
    def footer(self) -> ttk.Frame:
        """Return the footer frame."""
        return self._fr_footer
