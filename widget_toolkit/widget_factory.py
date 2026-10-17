import tkinter as tk
import customtkinter as ct
from PIL import Image

class WidgetConfigHelper:
    """Helper class for configuring widget values and applying defaults."""

    @staticmethod
    def get_grid_position(details: dict) -> tuple[int, int]:
        """
        Return the grid position as a tuple of (row, column).

        Raises:
            ValueError: If grid_position is missing or invalid.
        """
        grid_position = details.get("grid_position")

        if grid_position is None:
            raise ValueError("Missing required argument: 'grid_position'")

        if not isinstance(grid_position, tuple) or len(grid_position) != 2:
            raise ValueError("'grid_position' must be a tuple in the form (row, column)")

        return grid_position

    @staticmethod
    def get_font(details: dict):
        """
        Return the font for the widget.

        If no font is provided, a default CustomTkinter font is used.
        """
        font = details.get("font")
        if font is None:
            font = ct.CTkFont(family="Arial", size=20)
        return font

    @staticmethod
    def get_text_color(details: dict) -> str:
        """
        Return the text colour for the widget.

        Defaults to black if not provided.
        """
        text_color = details.get("text_color")
        if text_color is None:
            text_color = "black"
        return text_color

    @staticmethod
    def get_wraplength(details: dict) -> int:
        """
        Return the wraplength for the widget.

        Defaults to 0 if not provided.
        """
        wraplength = details.get("wraplength")
        if wraplength is None:
            wraplength = 0
        return wraplength

    @staticmethod
    def get_width(details: dict, default_width: int = 0) -> int:
        """
        Return the width for the widget.

        Uses the provided default width if no width is specified.
        """
        width = details.get("width")
        if width is None:
            width = default_width
        return width

    @staticmethod
    def get_height(details: dict, default_height: int = 0) -> int:
        """
        Return the height for the widget.

        Uses the provided default height if no height is specified.
        """
        height = details.get("height")
        if height is None:
            height = default_height
        return height

    @staticmethod
    def get_fg_color(details: dict) -> str:
        """
        Return the foreground colour for the widget.

        Defaults to black if not provided.
        """
        fg_color = details.get("fg_color")
        if fg_color is None:
            fg_color = "black"
        return fg_color

    @staticmethod
    def get_spinbox_from(details: dict) -> int | float:
        """
        Return the starting value for a Spinbox.

        Defaults to 0 if not provided.
        """
        from_value = details.get("from_")
        if from_value is None:
            from_value = 0
        return from_value

    @staticmethod
    def get_spinbox_to(details: dict, default_to_value: int | float = 10) -> int | float:
        """
        Return the ending value for a Spinbox.

        Uses the provided default if no value is specified.
        """
        to_value = details.get("to")
        if to_value is None:
            to_value = default_to_value
        return to_value

    @staticmethod
    def get_spinbox_increment(details: dict) -> int | float:
        """
        Return the increment value for a Spinbox.

        Defaults to 1 if not provided.
        """
        increment_value = details.get("increment")
        if increment_value is None:
            increment_value = 1
        return increment_value

    @staticmethod
    def validate_master(details: dict) -> None:
        """
        Validate that a master widget has been provided.

        Raises:
            ValueError: If master is missing.
        """
        if details.get("master") is None:
            raise ValueError("Missing required argument: 'master'")

class ImageLoader:
    """Class for loading the image"""
    def load_image(self,file,size:tuple):
        """"""
        image = ct.CTkImage(
            light_image=Image.open(file),
            dark_image=Image.open(file),
            size=size
            )
        return image


class CreateWidgets:
    """Class for creating Tkinter and CustomTkinter widgets."""

    def __init__(self):
        """Initialise the widget configuration helper."""
        self.config = WidgetConfigHelper()

    def create_ct_label(self, **label_details):
        """Create and return a CustomTkinter label."""
        self.config.validate_master(label_details)
        row, column = self.config.get_grid_position(label_details)

        label = ct.CTkLabel(
            master=label_details.get("master"),
            text=label_details.get("text", ""),
            width=self.config.get_width(label_details),
            height=self.config.get_height(label_details),
            font=self.config.get_font(label_details),
            text_color=self.config.get_text_color(label_details),
            wraplength=self.config.get_wraplength(label_details),
            
        )
        label.grid(
            row=row,
            column=column,
            columnspan=label_details.get("columnspan"),
            rowspan=label_details.get("rowspan"),
            padx=label_details.get("padx"),
            pady=label_details.get("pady"),
            sticky=label_details.get("sticky"),
        )
        return label

    def create_ct_button(self, **button_details):
        """Create and return a CustomTkinter button."""
        self.config.validate_master(button_details)
        row, column = self.config.get_grid_position(button_details)

        button = ct.CTkButton(
            master=button_details.get("master"),
            text=button_details.get("text", ""),
            width=self.config.get_width(button_details, default_width=140),
            height=self.config.get_height(button_details, default_height=30),
            font=self.config.get_font(button_details),
            text_color=self.config.get_text_color(button_details),
            command=button_details.get("command"),
            image=button_details.get("image"),
            hover_color=button_details.get("hover_color"),
            fg_color=button_details.get("fg_color")
        )
        button.grid(
            row=row,
            column=column,
            columnspan=button_details.get("columnspan"),
            rowspan=button_details.get("rowspan"),
            padx=button_details.get("padx"),
            pady=button_details.get("pady"),
            sticky=button_details.get("sticky"),
        )
        return button

    def create_ct_combobox(self, **combobox_details):
        """Create and return a CustomTkinter combobox."""
        self.config.validate_master(combobox_details)
        row, column = self.config.get_grid_position(combobox_details)
        
        combobox = ct.CTkComboBox(
            master=combobox_details.get("master"),
            values=combobox_details.get("values", []),
            font=self.config.get_font(combobox_details),
            state=combobox_details.get("state"),
            width=self.config.get_width(combobox_details, default_width=200),
            height=self.config.get_height(combobox_details, default_height=30),
            command=combobox_details.get("command"),
            fg_color=combobox_details.get("fg_color")
        )
        combobox.grid(
            row=row,
            column=column,
            padx=combobox_details.get("padx"),
            pady=combobox_details.get("pady"),
            sticky=combobox_details.get("sticky"),
        )
        return combobox

    def create_ct_frame(self, **frame_details):
        """Create and return a CustomTkinter frame."""
        self.config.validate_master(frame_details)
        row, column = self.config.get_grid_position(frame_details)

        frame = ct.CTkFrame(
            master=frame_details.get("master"),
            fg_color=self.config.get_fg_color(frame_details),
            border_color=frame_details.get("border_color"),
            border_width=frame_details.get("border_width"),
            width=self.config.get_width(frame_details),
            height=self.config.get_height(frame_details),
        )
        frame.grid(
            row=row,
            column=column,
            columnspan=frame_details.get("columnspan"),
            rowspan=frame_details.get("rowspan"),
            padx=frame_details.get("padx"),
            pady=frame_details.get("pady"),
            sticky=frame_details.get("sticky"),
        )
        return frame

    def create_ct_textbox(self, **textbox_details):
        """Create and return a CustomTkinter textbox."""
        self.config.validate_master(textbox_details)
        row, column = self.config.get_grid_position(textbox_details)

        textbox = ct.CTkTextbox(
            master=textbox_details.get("master"),
            font=self.config.get_font(textbox_details),
            width=self.config.get_width(textbox_details),
            height=self.config.get_height(textbox_details),
            wrap=tk.WORD,
            fg_color=textbox_details.get("fg_color"),
            border_color=textbox_details.get("border_color"),
            border_width=textbox_details.get("border_width"),
            text_color=textbox_details.get("text_color")
        )
        textbox.grid(
            row=row,
            column=column,
            columnspan=textbox_details.get("columnspan"),
            rowspan=textbox_details.get("rowspan"),
            padx=textbox_details.get("padx"),
            pady=textbox_details.get("pady"),
            sticky=textbox_details.get("sticky"),
        )
        return textbox

    def create_ct_scrollable_frame(self, **scrollable_frame_details):
        """Create and return a CustomTkinter scrollable frame."""
        self.config.validate_master(scrollable_frame_details)
        row, column = self.config.get_grid_position(scrollable_frame_details)

        scrollable_frame = ct.CTkScrollableFrame(
            master=scrollable_frame_details.get("master"),
            width=self.config.get_width(scrollable_frame_details, default_width=200),
            height=self.config.get_height(scrollable_frame_details, default_height=200),
            fg_color=scrollable_frame_details.get("fg_color")
        )
        scrollable_frame.grid(
            row=row,
            column=column,
            columnspan=scrollable_frame_details.get("columnspan"),
            rowspan=scrollable_frame_details.get("rowspan"),
            padx=scrollable_frame_details.get("padx"),
            pady=scrollable_frame_details.get("pady"),
            sticky=scrollable_frame_details.get("sticky"),
        )
        return scrollable_frame

    def create_ct_entry(self, **entry_details):
        """Create and return a CustomTkinter entry."""
        self.config.validate_master(entry_details)
        row, column = self.config.get_grid_position(entry_details)

        entry = ct.CTkEntry(
            master=entry_details.get("master"),
            font=self.config.get_font(entry_details),
            width=self.config.get_width(entry_details),
            placeholder_text=entry_details.get("placeholder_text"),
            fg_color=entry_details.get("fg_color"),
            border_color=entry_details.get("border_color"),
            border_width=entry_details.get("border_width"),
            placeholder_text_color=entry_details.get("placeholder_text_color"),
            text_color=entry_details.get("text_color")
        )
        entry.grid(
            row=row,
            column=column,
            columnspan=entry_details.get("columnspan"),
            rowspan=entry_details.get("rowspan"),
            padx=entry_details.get("padx"),
            pady=entry_details.get("pady"),
            sticky=entry_details.get("sticky"),
        )
        return entry

    def create_tk_listbox(self, **listbox_details):
        """Create and return a Tkinter listbox."""
        self.config.validate_master(listbox_details)
        row, column = self.config.get_grid_position(listbox_details)

        listbox = tk.Listbox(
            master=listbox_details.get("master"),
            font=self.config.get_font(listbox_details),
            height=self.config.get_height(listbox_details, default_height=10),
            width=self.config.get_width(listbox_details, default_width=20),
            
        )
        listbox.grid(
            row=row,
            column=column,
            columnspan=listbox_details.get("columnspan"),
            rowspan=listbox_details.get("rowspan"),
            padx=listbox_details.get("padx"),
            pady=listbox_details.get("pady"),
            sticky=listbox_details.get("sticky"),
        )

        bind_event = listbox_details.get("bind_event")
        command = listbox_details.get("command")
        if bind_event is not None and command is not None:
            listbox.bind(bind_event, func=command)

        return listbox

    def create_tk_toplevel(self, **toplevel_details):
        """Create and return a Tkinter toplevel window."""
        self.config.validate_master(toplevel_details)

        toplevel = tk.Toplevel(master=toplevel_details.get("master"))
        toplevel.focus()
        toplevel.grab_set()
        return toplevel

    def create_tk_spinbox(self, **spinbox_details):
        """Create and return a Tkinter spinbox."""
        self.config.validate_master(spinbox_details)
        row, column = self.config.get_grid_position(spinbox_details)

        spinbox = tk.Spinbox(
            master=spinbox_details.get("master"),
            font=self.config.get_font(spinbox_details),
            from_=self.config.get_spinbox_from(spinbox_details),
            to=self.config.get_spinbox_to(spinbox_details),
            increment=self.config.get_spinbox_increment(spinbox_details),
            width=self.config.get_width(spinbox_details, default_width=20),
        )
        spinbox.grid(
            row=row,
            column=column,
            columnspan=spinbox_details.get("columnspan"),
            rowspan=spinbox_details.get("rowspan"),
            padx=spinbox_details.get("padx"),
            pady=spinbox_details.get("pady"),
            sticky=spinbox_details.get("sticky"),
        )
        return spinbox

    def create_tk_entry(self, **entry_details):
        """Create and return a Tkinter entry."""
        self.config.validate_master(entry_details)
        row, column = self.config.get_grid_position(entry_details)

        entry = tk.Entry(
            master=entry_details.get("master"),
            font=self.config.get_font(entry_details),
            width=self.config.get_width(entry_details),
        )
        entry.grid(
            row=row,
            column=column,
            columnspan=entry_details.get("columnspan"),
            rowspan=entry_details.get("rowspan"),
            padx=entry_details.get("padx"),
            pady=entry_details.get("pady"),
            sticky=entry_details.get("sticky"),
        )
        return entry
