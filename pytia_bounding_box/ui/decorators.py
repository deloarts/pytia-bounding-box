"""
    Module that holds decorators for the app.
"""

import functools
import tkinter as tk
from typing import Callable


def busy(func: Callable) -> Callable:
    """
    Sets the UI to the busy state.

    .. warning::
        This decorator is only useable on the main window!
    """

    @functools.wraps(func)
    def _busy_wrapper(app, *args, **kwargs):
        app.config(cursor="wait")
        app.update()
        state_combo_preset = app.combo_preset["state"]
        app.combo_preset["state"] = tk.DISABLED
        state_combo_axis = app.combo_axis["state"]
        app.combo_axis["state"] = tk.DISABLED
        # state_scale_offset = app.scale_offset["state"]
        app.scale_offset["state"] = tk.DISABLED
        # state_scale_step = app.scale_step["state"]
        app.scale_step["state"] = tk.DISABLED
        # state_chkbox_thickness = app.chkbox_thickness["state"]
        app.chkbox_thickness["state"] = tk.DISABLED
        state_entry_measure_x = app.entry_measure_x["state"]
        app.entry_measure_x["state"] = tk.DISABLED
        state_entry_value_x = app.entry_value_x["state"]
        app.entry_value_x["state"] = tk.DISABLED
        state_entry_measure_y = app.entry_measure_y["state"]
        app.entry_measure_y["state"] = tk.DISABLED
        state_entry_value_y = app.entry_value_y["state"]
        app.entry_value_y["state"] = tk.DISABLED
        state_entry_measure_z = app.entry_measure_z["state"]
        app.entry_measure_z["state"] = tk.DISABLED
        state_entry_value_z = app.entry_value_z["state"]
        app.entry_value_z["state"] = tk.DISABLED
        state_entry_result_current = app.entry_result_current["state"]
        app.entry_result_current["state"] = tk.DISABLED
        state_entry_result_new = app.entry_result_new["state"]
        app.entry_result_new["state"] = tk.DISABLED
        app.btn_save["state"] = tk.DISABLED
        state_btn_abort = app.btn_abort["state"]
        app.btn_abort["state"] = tk.DISABLED
        app.update()

        value = func(app, *args, **kwargs)

        try:
            state_btn_save = app.btn_save["state"]

            app.combo_preset["state"] = state_combo_preset
            app.combo_axis["state"] = state_combo_axis
            # app.scale_offset["state"] = state_scale_offset
            # app.scale_step["state"] = state_scale_step
            # app.chkbox_thickness["state"] = state_chkbox_thickness
            app.entry_measure_x["state"] = state_entry_measure_x
            app.entry_value_x["state"] = state_entry_value_x
            app.entry_measure_y["state"] = state_entry_measure_y
            app.entry_value_y["state"] = state_entry_value_y
            app.entry_measure_z["state"] = state_entry_measure_z
            app.entry_value_z["state"] = state_entry_value_z
            app.entry_result_current["state"] = state_entry_result_current
            app.entry_result_new["state"] = state_entry_result_new
            app.btn_save["state"] = state_btn_save
            app.btn_abort["state"] = state_btn_abort
            app.config(cursor="arrow")
            app.update()
        except Exception:  # pylint: disable=W0703
            pass
        return value

    return _busy_wrapper
