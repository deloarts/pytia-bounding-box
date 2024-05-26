# default files

Explains the config of all default files.

All default files can be copied, renamed and edited to fit your needs.

## 1 information.default.json

This file contains a list of information, which will be shown to the user when the app has been used `counter` times.

- **Location**: [/pytia_bounding_box/resources/information.default.json](../pytia_bounding_box/resources/information.default.json)
- **Rename to**: `information.json`

### 1.1 file content

```json
[
    {
        "counter": 5,
        "msg": "If you need help using this app, or if you just want to know more about the available features: Press F1."
    },
    ...
]
```

### 1.2 description

name | type | description
--- | --- | ---
counter | `int` | The amount of app-usages when the information is shown.
id | `str` | The message to show.

## 2 presets.default.json

This file contains a list of all presets for the calculation of the bounding box.

- **Location**: [/pytia_bounding_box/resources/presets.default.json](../pytia_bounding_box/resources/presets.default.json)
- **Rename to**: `presets.json`

### 2.1 file content

```json
[
    {
        "name": "Standard",
        "coord": 3,
        "preference": null,
        "preference_postfix": null,
        "step": 5,
        "offset": 3,
        "offset_preference": true,
        "offset_non_preference": true,
        "sort_max_to_min": true,
        "result_filter": "(\\d+|\\d+\\.\\d+)\\s×\\s(\\d+|\\d+\\.\\d+)\\s×\\s(\\d+|\\d+\\.\\d+)$",
        "tooltip": "Applies an offset to all three dimensions of the parts boundaries.",
        "filter_examples": [
            "100 × 80 × 25",
            "40 × 40 × 10"
        ]
    },
    ...
]
```

### 2.2 description

name | type | description
--- | --- | ---
name | `str` | The name of the preset. Will be visible in the apps preset-option menu.
coord | `int` | The amount of coordinated: `2`=shaft, `3`=square, `4`=section.
preference | `str` | The most important direction: `min`, `max`, `axis`.
preference_postfix | `str` | The postfix applied to the preferred direction.
step | `int` | The pre-applied step for the bounding box calculation.
offset | `int` | The pre-applied offset for the bounding box calculation.
offset_preference | `bool` | If set to true, the preferred direction will get an offset. If false, the direction will have the exact measured value.
offset_non_preference | `bool` | If set to true, the non-preferred directions will get an offset. If false, the directions will have the exact measured value.
sort_max_to_min | `bool` | The sorting direction for the output.
result_filter | `str` | The regex filter the output will be tested against.
filter_examples | `list[str]` | Tooltip examples for the result filter.

## 3 processes.default.json

This file contains a list of processes, which are used to pre-apply a preset.

- **Location**: [/pytia_bounding_box/resources/processes.default.json](../pytia_bounding_box/resources/processes.default.json)
- **Rename to**: `processes.json`

### 3.1 file content

```json
[
    {
        "name": "Milling",
        "preset": "Standard"
    },
    {
        "name": "Turning",
        "preset": "Shaft"
    },
    ...
]
```

### 3.2 description

name | type | description
--- | --- | ---
name | `str` | The name of the process.
preset | `str` | The name of the preset to apply.

## 4 properties.default.json

This file contains all part properties, which are required for this app.

- **Location**: [/pytia_bounding_box/resources/properties.default.json](../pytia_bounding_box/resources/properties.default.json)
- **Rename to**: `properties.json`

### 4.1 file content

```json
{
    "base_size": "pytia.base_size",
    "base_size_preset": "pytia.base_size_preset",
    "creator": "pytia.creator",
    "modifier": "pytia.modifier",
    "process": "pytia.process_1"
}
```

### 4.2 description

name | type | description
--- | --- | ---
base_size | `str` | The name of the property, which stores the calculated base size.
base_size_preset | `str` | The name of the property, which stores the applied preset.
creator | `str` | The name of the property, that stores the creators name.
modifier | `str` | The name of the property, that holds the modifiers name.
process | `str` | The name of the property, which is used to pre-apply a preset.
