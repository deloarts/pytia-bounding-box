"""
    The GUI for the application.
"""

import time
import tkinter as tk
from pathlib import Path
from tkinter import font

import ttkbootstrap as ttk
from app.callbacks import Callbacks
from app.frames import Frames
from app.helper import LazyPartHelper
from app.helper import show_help
from app.layout import Layout
from app.loaders import Loaders
from app.state import UISetter
from app.validators import Validators
from app.vars import Variables
from const import APP_VERSION
from const import LOG
from const import LOGON
from const import LOGS
from pytia.exceptions import PytiaBodyEmptyError
from pytia.exceptions import PytiaDifferentDocumentError
from pytia.exceptions import PytiaDocumentNotSavedError
from pytia.exceptions import PytiaNoDocumentOpenError
from pytia.exceptions import PytiaPropertyNotFoundError
from pytia.exceptions import PytiaWrongDocumentTypeError
from pytia.log import log
from pytia_ui_tools.exceptions import PytiaUiToolsOutsideWorkspaceError
from pytia_ui_tools.handlers.error_handler import ErrorHandler
from pytia_ui_tools.handlers.mail_handler import MailHandler
from pytia_ui_tools.handlers.workspace_handler import Workspace
from pytia_ui_tools.window_manager import WindowManager
from resources import resource

t0 = time.perf_counter()


class GUI(tk.Tk):
    """The user interface of the app."""

    HEIGHT = 480
    WIDTH = 390

    def __init__(self) -> None:
        ttk.tk.Tk.__init__(self)
        ttk.Style(theme=resource.appdata.theme)

        self.part_helper: LazyPartHelper  # Instantiate later for performance improvement
        self.loaders: Loaders  # Instantiate later, depends on part_helper
        self.workspace: Workspace  # The workspace and loaders can only be read after the
        # lazy_document_helper has been instantiated. The reason is that the workspace depends on
        # the 'document.full_name' property, which is only available after the lazy_document_helper
        # has been instantiated.
        self.vars = Variables(root=self)
        self.frames = Frames(root=self)
        self.layout = Layout(root=self, frames=self.frames, variables=self.vars)
        self.set_ui = UISetter(root=self, layout=self.layout)
        self.validators = Validators(variables=self.vars, layout=self.layout)

        self.readonly = bool(
            not resource.user_exists(LOGON)
            and not resource.settings.restrictions.allow_all_users
        )

        self.window_manager = WindowManager(self)
        self.mail_handler = MailHandler(
            standard_receiver=resource.settings.mails.admin,
            app_title=resource.settings.title,
            app_version=APP_VERSION,
            logfile=Path(LOGS, LOG),
        )
        self.error_handler = ErrorHandler(
            mail_handler=self.mail_handler,
            warning_exceptions=[
                PytiaNoDocumentOpenError,
                PytiaWrongDocumentTypeError,
                PytiaBodyEmptyError,
                PytiaPropertyNotFoundError,
                PytiaDifferentDocumentError,
                PytiaDocumentNotSavedError,
                PytiaUiToolsOutsideWorkspaceError,
            ],
        )

        self.title(
            f"{resource.settings.title} "
            f"{'(DEBUG MODE)' if resource.settings.debug else APP_VERSION}"
            f"{' (READ ONLY)' if self.readonly else ''}"
        )
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True)
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

        self.update()
        self.window_manager.remove_window_buttons()

    def run(self) -> None:
        """Run the app."""
        t1 = time.perf_counter()  # pylint: disable=C0103
        log.info(f"Loaded UI in {(t1-t0):.4f}s")

        self.after(200, self.run_controller)
        self.mainloop()

    def run_controller(self) -> None:
        """Runs all controllers. Initializes all lazy loaders."""
        self.part_helper = LazyPartHelper()
        self.loaders = Loaders(
            root=self,
            variables=self.vars,
            layout=self.layout,
            validators=self.validators,
            lazy_part_helper=self.part_helper,
            ui_setter=self.set_ui,
        )
        self.workspace = Workspace(
            path=self.part_helper.path,
            filename=resource.settings.files.workspace,
            allow_outside_workspace=resource.settings.restrictions.allow_outside_workspace,
        )
        self.workspace.read_yaml()
        self.callbacks()
        self.traces()
        self.bindings()
        self.main_controller()

    def main_controller(self) -> None:
        """The main controller: Loads and calculates the bounding box."""
        self.set_ui.busy()
        self.loaders.load_process()
        self.loaders.load_measurements()
        self.loaders.load_combobox_preset()
        self.loaders.load_combobox_axis()
        self.loaders.load_chkbox_thickness()
        self.loaders.load_scale_offset()
        self.loaders.load_scale_step()
        self.loaders.load_existing_base_size()
        self.loaders.load_calculated()
        self.loaders.load_result()
        # self.set_ui.normal()

    def bindings(self) -> None:
        """Key bindings."""
        self.bind("<Escape>", lambda _: self.destroy())
        self.bind("<F1>", lambda _: show_help())
        self.bind("<F5>", lambda _: self.main_controller())

        self.layout.input_x.bind("<KeyRelease>", lambda _: self.loaders.load_result())
        self.layout.input_y.bind("<KeyRelease>", lambda _: self.loaders.load_result())
        self.layout.input_z.bind("<KeyRelease>", lambda _: self.loaders.load_result())
        self.layout.input_result.bind(
            "<KeyRelease>", lambda _: self.validators.validate_result()
        )

    def callbacks(self) -> None:
        """Instantiates the Callbacks class and sets up the callbacks."""
        Callbacks(
            root=self,
            variables=self.vars,
            lazy_part_helper=self.part_helper,
            layout=self.layout,
            loaders=self.loaders,
            workspace=self.workspace,
            ui_setter=self.set_ui,
        )

    def traces(self) -> None:
        ...
