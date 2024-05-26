"""
    Test the helper.py file.
"""

import importlib.resources
import json
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import Tk

import pytest
from pytia.exceptions import PytiaValueError

from pytia_bounding_box.app import helper
from pytia_bounding_box.const import CONFIG_PRESETS_DEFAULT
from pytia_bounding_box.const import Axes
from pytia_bounding_box.resources import Preset
from pytia_bounding_box.resources import resource

root = Tk()


def test_get_offset():
    """Tests the get_offset method from the helper.py file."""
    offset = helper.get_offset(
        x=100,
        y=80,
        z=20,
        selected_preset=resource.presets[0],
        selected_axis=Axes.X,
        selected_offset=IntVar(master=root, value=resource.settings.offset.tick),
        selected_step=IntVar(master=root, value=resource.settings.step.tick),
    )
    assert isinstance(offset, tuple)
    with pytest.raises(PytiaValueError):
        helper.get_offset(
            x="a",
            y=80,
            z=20,
            selected_preset=resource.presets[0],
            selected_axis=Axes.X,
            selected_offset=IntVar(master=root, value=resource.settings.offset.tick),
            selected_step=IntVar(master=root, value=resource.settings.step.tick),
        )


def test_get_preferred_axis():
    """Tests the get_preferred_axis method from the helper.py file."""
    with importlib.resources.open_binary("resources", CONFIG_PRESETS_DEFAULT) as f:
        presets = [Preset(**i) for i in json.load(f)]
        for preset in presets:
            match preset.name:
                case "Standard":
                    assert (
                        helper.get_preferred_axis(
                            x=100, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.X.value
                    )
                case "Exact":
                    assert (
                        helper.get_preferred_axis(
                            x=100, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.X.value
                    )
                case "Cut":
                    assert (
                        helper.get_preferred_axis(
                            x=80, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.Z.value
                    )
                    assert (
                        helper.get_preferred_axis(
                            x=100, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.X.value
                    )
                case "Sawn":
                    assert (
                        helper.get_preferred_axis(
                            x=100, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.Z.value
                    )
                case "Pre-Milled":
                    assert (
                        helper.get_preferred_axis(
                            x=100, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.Z.value
                    )
                case "Shaft":
                    assert (
                        helper.get_preferred_axis(
                            x=20, y=20, z=100, selected_preset=preset
                        ).value
                        == Axes.Z.value
                    )
                    assert (
                        helper.get_preferred_axis(
                            x=20, y=25, z=100, selected_preset=preset
                        ).value
                        == Axes.Z.value
                    )
                case "Custom":
                    assert (
                        helper.get_preferred_axis(
                            x=100, y=80, z=20, selected_preset=preset
                        ).value
                        == Axes.X.value
                    )


def test_get_preferred_axis_exception():
    """Tests the PytiaValueError exception from the method."""
    with pytest.raises(PytiaValueError):
        with importlib.resources.open_binary("resources", CONFIG_PRESETS_DEFAULT) as f:
            presets = [Preset(**i) for i in json.load(f)]
            helper.get_preferred_axis(x="a", y=20, z=100, selected_preset=presets[0])


def test_sort_base_size():
    """Tests the sort_base_size method from the helper.py file."""
    with importlib.resources.open_binary("resources", CONFIG_PRESETS_DEFAULT) as f:
        presets = [Preset(**i) for i in json.load(f)]
        for preset in presets:
            match preset.name:
                case "Standard":
                    assert (
                        helper.sort_base_size(
                            x=20,
                            y=100,
                            z=50,
                            selected_preset=preset,
                            selected_axis=Axes.X,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"100{resource.settings.signs.dimension}50{resource.settings.signs.dimension}20"
                    )
                case "Exact":
                    assert (
                        helper.sort_base_size(
                            x=20,
                            y=100,
                            z=50,
                            selected_preset=preset,
                            selected_axis=Axes.X,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"100{resource.settings.signs.dimension}50{resource.settings.signs.dimension}20"
                    )
                case "Cut":
                    assert (
                        helper.sort_base_size(
                            x=50,
                            y=100,
                            z=50,
                            selected_preset=preset,
                            selected_axis=Axes.Y,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"50{resource.settings.signs.dimension}50{resource.settings.signs.dimension}100"
                    )
                case "Cut":
                    assert (
                        helper.sort_base_size(
                            x=40,
                            y=100,
                            z=50,
                            selected_preset=preset,
                            selected_axis=Axes.Y,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"40{resource.settings.signs.dimension}50{resource.settings.signs.dimension}100"
                    )
                case "Sawn":
                    assert (
                        helper.sort_base_size(
                            x=80,
                            y=100,
                            z=20,
                            selected_preset=preset,
                            selected_axis=Axes.Z,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"100{resource.settings.signs.dimension}80{resource.settings.signs.dimension}20F"
                    )
                case "Pre-Milled":
                    assert (
                        helper.sort_base_size(
                            x=80,
                            y=100,
                            z=20,
                            selected_preset=preset,
                            selected_axis=Axes.Z,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"100{resource.settings.signs.dimension}80{resource.settings.signs.dimension}20F"
                    )
                case "Shaft":
                    assert (
                        helper.sort_base_size(
                            x=20,
                            y=100,
                            z=20,
                            selected_preset=preset,
                            selected_axis=Axes.Y,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"{resource.settings.signs.diameter}20{resource.settings.signs.dimension}100"
                    )
                case "Shaft":
                    assert (
                        helper.sort_base_size(
                            x=18,
                            y=100,
                            z=20,
                            selected_preset=preset,
                            selected_axis=Axes.Y,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"{resource.settings.signs.diameter}20{resource.settings.signs.dimension}100"
                    )
                case "Custom":
                    assert (
                        helper.sort_base_size(
                            x=20,
                            y=100,
                            z=50,
                            selected_preset=preset,
                            selected_axis=Axes.X,
                            thickness=BooleanVar(master=root, value=False),
                        )
                        == f"100{resource.settings.signs.dimension}50{resource.settings.signs.dimension}20"
                    )


def test_sort_base_size_invalid_value():
    """Tests the sort_base_size method with an invalid input value."""
    with importlib.resources.open_binary("resources", CONFIG_PRESETS_DEFAULT) as f:
        presets = [Preset(**i) for i in json.load(f)]
        assert (
            helper.sort_base_size(
                x="a",
                y=100,
                z=50,
                selected_preset=presets[0],
                selected_axis=Axes.X,
                thickness=BooleanVar(master=root, value=False),
            )
            == ""
        )
