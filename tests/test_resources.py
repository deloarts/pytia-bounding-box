"""
    Test the resources.py file.
"""

import os

import validators


def test_resources_class():
    from pytia_bounding_box.resources import Resources

    resource = Resources()


def test_settings():
    from pytia_bounding_box.resources import resource

    assert isinstance(resource.settings.title, str)
    assert len(resource.settings.title) > 0
    assert isinstance(resource.settings.debug, bool)
    assert isinstance(resource.settings.precision, int)

    assert isinstance(resource.settings.offset.min, int)
    assert isinstance(resource.settings.offset.max, int)
    assert isinstance(resource.settings.offset.tick, int)

    assert isinstance(resource.settings.step.min, int)
    assert isinstance(resource.settings.step.max, int)
    assert isinstance(resource.settings.step.tick, int)

    assert isinstance(resource.settings.parameters.thickness, str)

    assert isinstance(resource.settings.restrictions.allow_all_users, bool)
    assert isinstance(resource.settings.restrictions.allow_all_editors, bool)
    assert isinstance(resource.settings.restrictions.allow_unsaved, bool)
    assert isinstance(resource.settings.restrictions.allow_outside_workspace, bool)
    assert isinstance(resource.settings.restrictions.allow_property_creation, bool)
    assert isinstance(resource.settings.restrictions.enable_information, bool)

    assert isinstance(resource.settings.save_modifier_by, str)

    assert isinstance(resource.settings.paths.local_dependencies, str)
    assert isinstance(resource.settings.paths.release, str)
    assert resource.settings.files.app.endswith(".pyz")
    assert resource.settings.files.launcher.endswith(".catvbs")

    if resource.settings.urls.help:
        assert validators.url(resource.settings.urls.help)  # type: ignore
    assert validators.email(resource.settings.mails.admin)  # type: ignore


def test_users():
    from pytia_bounding_box.resources import resource

    logon_list = []

    for user in resource.users:
        assert isinstance(user.logon, str)
        assert isinstance(user.id, str)
        assert isinstance(user.name, str)
        assert isinstance(user.mail, str)
        assert user.logon not in logon_list

        logon_list.append(user.logon)


def test_props():
    from pytia_bounding_box.resources import resource

    assert "base_size" in resource.props.keys
    assert "base_size_preset" in resource.props.keys
    assert "creator" in resource.props.keys
    assert "modifier" in resource.props.keys
    assert "process" in resource.props.keys

    assert all([len(v) > 0 for v in resource.props.values])


def test_local_dependencies_folder():
    from pytia_bounding_box.resources import resource

    assert os.path.isdir(resource.settings.paths.local_dependencies)


def test_release_folder():
    from pytia_bounding_box.resources import resource

    assert os.path.isdir(resource.settings.paths.release)


def test_modifier_filter():
    import re

    from pytia.const import USERNAME

    from pytia_bounding_box.resources import resource

    user = resource.get_user_by_logon(USERNAME)
    filter_result = re.findall(r"\%(.*?)\%", resource.settings.save_modifier_by)

    assert all(elem in user.keys for elem in filter_result)
    assert any(i in resource.settings.save_modifier_by for i in resource.users[0].keys)


def test_debug_mode():
    from pytia_bounding_box.resources import resource

    assert resource.settings.debug == False
