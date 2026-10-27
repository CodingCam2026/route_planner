# Tkinter Widget Helper

A Python helper module for creating Tkinter and CustomTkinter interfaces with less repeated setup code. It combines widget creation, default settings and grid placement into reusable methods.

Use it when building desktop applications that need labels, buttons, input fields, dropdowns, frames and other common widgets.

## Features

- Create seven types of CustomTkinter widget and four types of standard Tkinter widget/window.
- Position supported widgets using a `grid_position=(row, column)` argument.
- Reuse helper defaults for fonts, colours, dimensions and spinbox ranges.
- Check that a parent widget and a correctly shaped grid-position tuple have been supplied.
- Receive the created widget back so you can update its contents or settings afterwards.
- Load image files into `CTkImage` objects for use with supported CustomTkinter widgets.

## Requirements

- **Python 3.10 or later**, required by the type annotations used in this module.
- **Tkinter**, with a working graphical desktop/display.
- **CustomTkinter**.
- **Pillow**, imported in the code as `PIL`.

No API keys, accounts or external services are required by the module. Internet access is needed to download dependencies unless they are already available locally.

## Installation

The examples below assume you save the supplied helper code as **`widget_helper.py`**. If you choose another filename, adjust the import statements accordingly.

### 1. Create a project folder

Place `widget_helper.py` inside your project folder and open a terminal there.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command for your terminal:

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

On macOS or Linux, use `python3` to create the environment if `python` is unavailable.

### 3. Install dependencies

```bash
python -m pip install customtkinter pillow
```

Check that Tkinter is available:

```bash
python -m tkinter
```

This should open a small demonstration window. If Tkinter is missing, install Tk support for your Python installation through your operating system or Python installer.

## Quick start

Create a file named **`demo.py`** beside `widget_helper.py` and add:

```python
import customtkinter as ct

from widget_helper import CreateWidgets


def main():
    ct.set_appearance_mode("light")

    app = ct.CTk()
    app.title("Widget Helper Demo")
    app.geometry("420x220")
    app.grid_columnconfigure(0, weight=1)

    widgets = CreateWidgets()

    label = widgets.create_ct_label(
        master=app,
        grid_position=(0, 0),
        text="Hello, Cam!",
        width=300,
        height=40,
        text_color="black",
        padx=20,
        pady=20,
    )

    def change_message():
        label.configure(text="The button works!")

    widgets.create_ct_button(
        master=app,
        grid_position=(1, 0),
        text="Click me",
        command=change_message,
        text_color="white",
        fg_color="#2563EB",
        hover_color="#1D4ED8",
        padx=20,
        pady=10,
    )

    app.mainloop()


if __name__ == "__main__":
    main()
```

Run it with:

```bash
python demo.py
```

**Expected result:** a window containing a greeting and a button. Clicking the button changes the greeting to `The button works!`.

Running `widget_helper.py` alone does not open a window: it defines reusable classes, but does not create an application or start its event loop.

## Available classes

| Class | Purpose |
| --- | --- |
| `WidgetConfigHelper` | Validates required arguments and supplies selected default settings. Used internally by `CreateWidgets`. |
| `CreateWidgets` | Creates widgets, applies supported settings, places most widgets in a grid and returns each created object. |
| `ImageLoader` | Opens an image file with Pillow and returns a CustomTkinter `CTkImage`. |

## Supported widgets

| Method | Returns | Notable options |
| --- | --- | --- |
| `create_ct_label()` | `CTkLabel` | `text`, `font`, `text_color`, `wraplength`, dimensions |
| `create_ct_button()` | `CTkButton` | `text`, `command`, `image`, colours, font, dimensions |
| `create_ct_combobox()` | `CTkComboBox` | `values`, `state`, `command`, font, dimensions |
| `create_ct_frame()` | `CTkFrame` | Foreground/border colours, border width, dimensions |
| `create_ct_textbox()` | `CTkTextbox` | Font, colours, border width, dimensions; word wrapping is enabled |
| `create_ct_scrollable_frame()` | `CTkScrollableFrame` | Width and height |
| `create_ct_entry()` | `CTkEntry` | `placeholder_text`, placeholder/text colours, font, width, border settings |
| `create_tk_listbox()` | `tk.Listbox` | Font, dimensions, optional `bind_event` and `command` pair |
| `create_tk_toplevel()` | `tk.Toplevel` | Parent only; focuses the window and calls `grab_set()` |
| `create_tk_spinbox()` | `tk.Spinbox` | `from_`, `to`, `increment`, font, width |
| `create_tk_entry()` | `tk.Entry` | Font and width |

Only arguments explicitly read by a helper are forwarded to its widget. Passing an additional keyword does not automatically enable the corresponding Tkinter or CustomTkinter option.

## Configuration

### Required arguments

Every widget-creation method requires `master`, the parent window or frame.

All methods except `create_tk_toplevel()` also require `grid_position`, supplied as a two-item tuple:

```python
grid_position=(0, 1)  # Row 0, column 1
```

Use non-negative integer row and column values. The helper checks that the value is a tuple with two items; it does not validate the types or ranges of those items itself.

### Grid layout options

The gridded helpers accept `padx`, `pady` and `sticky`. They also accept `columnspan` and `rowspan`, except for `create_ct_combobox()`, which does not forward those two options.

Configure grid row/column weights on the parent yourself when you want widgets to expand as the window resizes.

### Defaults supplied by the helper

| Setting | Default |
| --- | --- |
| Font, where the font helper is used | Arial, size 20 |
| Label/button text colour | Black |
| Label wrapping length | `0` |
| Button dimensions | Width `140`, height `30` |
| Combobox dimensions | Width `200`, height `30` |
| Scrollable frame dimensions | Width `200`, height `200` |
| Frame foreground colour | Black |
| Tkinter listbox dimensions | Width `20`, height `10` |
| Spinbox range and increment | `0` to `10`, increment `1` |
| Spinbox width | `20` |

Several other dimensions default to `0`, so pass explicit sizes when needed. Standard Tkinter entry/listbox/spinbox widths are generally character-based; CustomTkinter dimensions are pixel-based. Listbox height is measured in rows.

Defaults are not identical across methods. For example, entry and textbox text colours are passed directly from their keyword arguments rather than using the black-text helper.

### Callbacks

- **Button:** pass a function without calling it, such as `command=save_data`.
- **Combobox:** the callback should accept the selected value.
- **Listbox binding:** supply both `bind_event` and `command`; the callback should accept the event object.

## Loading an image

After creating your application window, load an image and pass it to a button:

```python
from widget_helper import ImageLoader

loader = ImageLoader()
icon = loader.load_image("assets/icon.png", size=(24, 24))

image_button = widgets.create_ct_button(
    master=app,
    grid_position=(2, 0),
    text="Open",
    image=icon,
    text_color="white",
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    padx=20,
    pady=10,
)
```

This snippet extends the quick-start example: put it inside `main()`, before `app.mainloop()`, and provide a real `assets/icon.png` file. Keep the image reference while it is in use.

Relative file paths are resolved from the terminal's current working directory. The loader uses the same file for light and dark appearance modes; it does not provide separate images for each mode.

## Updating

If you obtained this project through a Git clone, commit your local changes on the appropriate branch before updating, then run:

```bash
git pull --ff-only
```

Review any changes to the helper's arguments or dependencies, then close and restart your demo/application to load the updated code. Pulling source changes does not update installed Python packages automatically.

## Testing

No automated tests are included in the supplied code. The quick-start example is a manual smoke test:

1. Launch `demo.py` and confirm the window opens.
2. Click the button and confirm the label changes.
3. Close the window and confirm the process exits normally.

Test additional widgets and appearance modes in the applications that use them. The README examples have not been verified in a live graphical session.

## Known limitations

- This is a helper module, not a standalone application or visual interface designer.
- Optional arguments are handled unevenly. Some missing settings, such as `border_width` on certain helpers, are passed as `None` rather than omitted. Supply explicit values where required by the underlying widget.
- Unrecognised keyword arguments are silently ignored by the wrapper methods, which can hide spelling mistakes.
- Fixed black text and foreground defaults may need overriding for readability in dark mode.
- The listbox and spinbox are standard Tkinter widgets, so their appearance may differ from CustomTkinter controls.
- `create_tk_toplevel()` takes an input grab; it does not call `wait_window()`, so creating it does not pause the calling code until it closes.
- `ImageLoader` does not catch missing-file or invalid-image errors.
- Dependency versions and cross-platform compatibility have not been established by the supplied source alone.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `ModuleNotFoundError: No module named 'customtkinter'` | Activate the correct environment and run `python -m pip install customtkinter`. |
| `ModuleNotFoundError: No module named 'PIL'` | Install Pillow with `python -m pip install pillow`. |
| `ModuleNotFoundError: No module named 'widget_helper'` | Save the helper as `widget_helper.py` beside `demo.py`, or adjust the import to its actual module name. |
| `Missing required argument: 'master'` | Pass an existing parent window or frame. |
| Missing or invalid `grid_position` | Supply a tuple such as `(0, 0)`, not a list or string. |
| A type error mentions `None` or a border setting | Check the helper and provide a concrete value, such as `border_width=0`, where needed. |
| No window appears when running the helper | Run an application such as `demo.py` that creates a root window and calls `mainloop()`. |
| Image file cannot be opened | Check the file exists and its path is correct relative to your working directory. |
| Display-related error on a server | Run the GUI in an environment with an available graphical display. |

## Feedback and contributions

When reporting a problem, include your Python and dependency versions, operating system, full error message and a small example that reproduces it.

Useful areas for contributions include consistent optional-argument handling, stronger validation, tests and additional widget options.

## Licence

No licence was supplied with this code. Check with the author before redistributing it or incorporating it into another project.
