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
    "enable_information": true,
    "allow_all_users": false,
    "allow_property_creation": true,
    "save_modifier_by": "%id% | %name%",
    "paths": {
        "local_dependencies": "C:\\pytia\\local_deps",
        "release": "C:\\pytia\\release"
    },
    "files": {
        "app": "pytia_bounding_box.pyz",
        "launcher": "pytia_bounding_box.catvbs"
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
enable_information | `bool` | If set to true the user will see the notifications from the **information.json** file.
allow_all_users | `bool` | If set to true any user can save the bounding box result to the part properties. If set to false only those users from the **users.json** file can modify the part properties.
allow_property_creation | `bool` | If set to true, the app is allowed to create part properties, if they don't exist. If set to false, all required properties must be created before running the app.
save_modifier_by | `str` | The way the modifier is saved to the part properties. Available options are: `%logon%`, `%id%`, `%name%` and `%mail%`, or any combination, like `%id% | %name%`.
paths.local_dependencies | `str` | The folder where local local_dependencies (python wheel files) for the installer are stored.
paths.release | `str` | The folder where the launcher and the app are released into.
files.app | `str` | The name of the released python app file.
files.launcher | `str` | The name of the release catvbs launcher file.
urls.help | `str` or `null` | The help page for the app. If set to null the user will receive a message, that no help page is provided.
mails.admin | `str` | The mail address of the sys admin. Required for error mails.

## 2.1 users.sample.json

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
