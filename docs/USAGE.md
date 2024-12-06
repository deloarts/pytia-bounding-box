# usage

> ✏️ This covers the usage of the app, which depends on the configuration of the `settings.json` config file. If you use different names for properties or disable some of the functionality, the apps layout may be different from the one in this guide.

- [usage](#usage)
  - [1 launcher](#1-launcher)
  - [2 app](#2-app)
    - [2.1 selection](#21-selection)
    - [2.2 measured / selected](#22-measured--selected)
    - [2.3 result](#23-result)

## 1 launcher

If your setup is done (see [installation](./INSTALLATION.md)), open the app from within CATIA. If this is the first time, you'll see the launcher will install all necessary dependencies:

![Installer](/assets/images/installer.png)

After the installation you can run the app.

## 2 app

The usage itself is pretty straight forward, as long as all config files are setup properly.

![app](/assets/images/app.png)

### 2.1 selection

The selection area is for applying various settings to the bounding box calculation.

- **Preset**: Apply a preset. By default there are various presets available. For a quick hint of what which preset does, hover with your mouse over the preset option menu.
- **Axis**: The axis is relevant for some presets. For example the turning axis of a shaft.
- **Offset**: The offset is the minimum value that will be applied to the parts minimum bounding box.
- **Step**: The step is the value to which the offset will be rounded up to.
- **Thickness**: Some presets allow a thickness parameter. It will be added to the resulting value. For example the thickness of a section profile.

### 2.2 measured / selected

The measured / selected area is for the user to compare the values of the exact bounding box and the calculated result. The results can be edited by the user, if the automatically created values won't fit the users needs.

### 2.3 result

The result area is for a last check before saving the bounding box value to the part-properties.

- **Current value**: Shows an applied current bounding box value, if the app has been run before.
- **New value**: Shows the newly calculated bounding box value. This input is tested against a filter. If the value doesn't pass the test, the user can hover over the input field to get an explanation why the new value doesn't match the filter criteria.