# sample files

Explains the config of all sample files.

All sample files must be copied, renamed and edited to fit your needs.

## 1 settings.sample.json

This file contains the basic settings for the app.

- **Location**: [/pytia_bounding_box/resources/settings.sample.json](../pytia_bounding_box/resources/settings.sample.json)
- **Rename to**: `settings.json`

### 1.1 file content

```json
{
    "title": "PYTIA Bounding Box",
    "debug": false,
    "precision": 3,
    "offset": {
        "min": 0,
        "max": 10,
        "tick": 1
    },
    "step": {
        "min": 0,
        "max": 10,
        "tick": 5
    },
    "parameters": {
        "thickness": "section_thickness"
    },
    "restrictions": {
        "allow_all_users": true,
        "allow_all_editors": true,
        "allow_unsaved": true,
        "allow_outside_workspace": true,
        "allow_property_creation": true,
        "enable_information": true
    },
    "save_modifier_by": "%id% | %name%",
    "paths": {
        "catia": "C:\\CATIA\\V5-6R2017\\B27",
        "release": "C:\\pytia\\release"
    },
    "files": {
        "app": "pytia_bounding_box.pyz",
        "launcher": "pytia_bounding_box.catvbs",
        "workspace": "workspace.yml"
    },
    "urls": {
        "help": "https://github.com/deloarts/pytia-bounding-box"
    },
    "mails": {
        "admin": "admin@company.com"
    }
}
```

### 1.2 description

name | type | description
--- | --- | ---
title | `str` | The apps title. This will be visible in the title bar of the window.
debug | `bool` | The flag to declare the debug-state of the app. The app cannot be built if this value is true.
precision | `int` | The number of digits after the decimal point.
offset.min | `int` | The minimum offset the user can apply via the offset slider.
offset.max | `int` | The maximum offset the user can apply via the offset slider.
offset.tick | `int` | The steps which the slider can move.
step.min | `int` | The minimum step the user can apply via the step slider.
step.max | `int` | The maximum step the user can apply via the step slider.
step.tick | `int` | The steps which the slider can move.
parameters.thickness | `str` | The name of the thickness parameter in a part.
restrictions.allow_all_users | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users from the **users.json** file can modify the properties.
restrictions.allow_all_editors | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users which are declared in the **workspace** file can modify the properties. If no workspace file is found, or no **editors** list-item is inside the workspace file, then this is omitted, and everyone can make changes.
restrictions.allow_unsaved | `bool` | If set to `false` an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.allow_outside_workspace | `bool` | If set to `false` a **workspace** file must be provided somewhere in the folder structure where the document is saved. This also means, that an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.allow_property_creation | `bool` | If set to true, the app is allowed to create part properties, if they don't exist. If set to false, all required properties must be created before running the app.
restrictions.enable_information | `bool` | If set to true the user will see the notifications from the **information.json** file.
save_modifier_by | `str` | The way the modifier is saved to the part properties. Available options are: `%logon%`, `%id%`, `%name%` and `%mail%`, or any combination, like `%id% | %name%`.
path.catia | `str` | The absolute path to the CATIA executables.
paths.release | `str` | The folder where the launcher and the app are released into.
files.app | `str` | The name of the released python app file.
files.launcher | `str` | The name of the release catvbs launcher file.
files.workspace | `str` | The name of the workspace file.
urls.help | `str` or `null` | The help page for the app. If set to null the user will receive a message, that no help page is provided.
mails.admin | `str` | The mail address of the sys admin. Required for error mails.

## 2 users.sample.json

This file contains a list of users known to the system.

- **Location**: [/pytia_bounding_box/resources/users.sample.json](../pytia_bounding_box/resources/users.sample.json)
- **Rename to**: `users.json`

### 2.1 file content

```json
[
    {
        "logon": "admin",
        "id": "001",
        "name": "Administrator",
        "mail": "admin@company.com"
    },
    ...
]
```

### 2.2 description

name | type | description
--- | --- | ---
logon | `str` | The windows logon name of the user.
id | `str` | The ID of the user. Can be used for the employee ID.
name | `str` | The name of the user.
mail | `str` | The users mail address.
