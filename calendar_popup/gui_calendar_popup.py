
import customtkinter as ct
from calendar_readers.ical_reader import IcalReader
from datetime import date, datetime
from tkcalendar import Calendar
from tkinter import ttk
from calendar_readers.google_cal_reader import GoogleCalendarReader
from calendar_popup.calendar_commands_new import CalendarCommands

class CalendarPopup:
    """Class for managing the popup window for importing calendar jobs."""

    def __init__(self, gui_main):
        self.gui_main = gui_main
        self.gui_colours = self.gui_main.gui_colours
        self.ical_reader = IcalReader()
        self.google_cal_reader = GoogleCalendarReader()
        self.calendar_popup_commands = CalendarCommands(self)

    def style_treeview(self):
        """Apply the application colour theme to the Treeview."""

        colours = self.gui_colours

        # Use a dedicated style for the calendar popup
        self.tree_style = ttk.Style(self.popup_root)
        self.tree_style.theme_use("clam")

        self.tree_style.configure(
            "Calendar.Treeview",
            background=colours.card_background,
            foreground=colours.primary_text,
            fieldbackground=colours.card_background,
            borderwidth=0,
            relief="flat",
            rowheight=42,
            font=("Arial", 12)
        )

        # Column headers
        self.tree_style.configure(
            "Calendar.Treeview.Heading",
            background=colours.secondary_background,
            foreground=colours.secondary_text,
            relief="flat",
            borderwidth=0,
            padding=(12, 12),
            font=("Arial", 12, "bold")
        )

        # Selected rows
        self.tree_style.map(
            "Calendar.Treeview",
            background=[
                ("selected", colours.selected_background)
            ],
            foreground=[
                ("selected", colours.primary_text)
            ]
        )

        # Header hover
        self.tree_style.map(
            "Calendar.Treeview.Heading",
            background=[
                ("active", colours.hover_background),
                ("pressed", colours.tertiary_background)
            ],
            foreground=[
                ("active", colours.primary_text)
            ]
        )

    def popup(self):
        """Shows popup window."""

        colours = self.gui_colours

        self.popup_root = ct.CTkToplevel(
            fg_color=colours.primary_background
        )
        self.selected_calendar_checkbox = None
        
        self.popup_root.title("Import Calendar Events")
        self.popup_root.geometry("1150x700")
        self.popup_root.minsize(950, 550)

        self.popup_root.focus()
        self.popup_root.grab_set()

        # ===================================
        # MAIN WINDOW GRID
        # ===================================

        self.popup_root.grid_columnconfigure(0, weight=0, minsize=470)
        self.popup_root.grid_columnconfigure(1, weight=1)

        # Calendar row
        self.popup_root.grid_rowconfigure(0, weight=0)

        # Scrollable frame row
        self.popup_root.grid_rowconfigure(1, weight=1)

        # Import button row
        self.popup_root.grid_rowconfigure(2, weight=0)

        # ===================================
        # CALENDAR SECTION
        # ===================================

        cal_frame = ct.CTkFrame(
            self.popup_root,
            fg_color=colours.card_background,
            corner_radius=10,
            border_width=1,
            border_color=colours.primary_border
        )

        cal_frame.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=(20, 5),
            sticky="new"
        )

        cal_frame.grid_columnconfigure(0, weight=1)
        cal_frame.grid_columnconfigure(1, weight=1)

        # Calendar heading
        ct.CTkLabel(
            cal_frame,
            text="Select Date",
            font=("Arial", 19, "bold"),
            text_color=colours.primary_text,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=15,
            pady=(15, 10),
            sticky="ew"
        )

        # ===================================
        # CALENDAR
        # ===================================

        self.calendar = Calendar(
            cal_frame,
            selectmode="day",
            date_pattern="dd/mm/yyyy",
            font=("Arial", 18),

            # Main colours
            background=colours.card_background,
            foreground=colours.primary_text,
            bordercolor=colours.primary_border,

            # Header
            headersbackground=colours.tertiary_background,
            headersforeground=colours.primary_text,

            # Selected date
            selectbackground=colours.primary_colour,
            selectforeground=colours.primary_text,

            # Normal days
            normalbackground=colours.input_background,
            normalforeground=colours.primary_text,

            # Weekends
            weekendbackground=colours.input_background,
            weekendforeground=colours.accent_colour,

            # Disabled dates
            disabledbackground=colours.disabled_background,
            disabledforeground=colours.disabled_text,

            # Other month dates
            othermonthbackground=colours.secondary_background,
            othermonthforeground=colours.muted_text,
            othermonthwebackground=colours.secondary_background,
            othermonthweforeground=colours.muted_text
        )

        self.calendar.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 15)
        )

        # ===================================
        # CALENDAR BUTTONS
        # ===================================

        # Today button
        self.gui_main.create_widgets.create_ct_button(
            master=cal_frame,
            grid_position=(2, 0),
            text="Today",
            sticky="ew",
            padx=15,
            pady=(0, 15),
            command=self.calendar_popup_commands.today_button_command,
            fg_color=colours.primary_button,
            hover_color=colours.primary_button_hover
        )

        # Get Events button
        self.gui_main.create_widgets.create_ct_button(
            master=cal_frame,
            grid_position=(2, 1),
            text="Get Events",
            sticky="ew",
            padx=15,
            pady=(0, 15),
            command=lambda: self.calendar_popup_commands.get_events(
                self.calendar.selection_get()
            ),
            fg_color=colours.primary_button,
            hover_color=colours.primary_button_hover
        )

        # ===================================
        # SCROLLABLE FRAME BELOW CALENDAR
        # ===================================

        self.scrollable_frame = ct.CTkScrollableFrame(
            self.popup_root,
            fg_color=colours.card_background,
            border_width=1,
            border_color=colours.primary_border,
            corner_radius=10,
            scrollbar_button_color=colours.secondary_button,
            scrollbar_button_hover_color=colours.secondary_button_hover,
        )

        self.scrollable_frame.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(5, 20),
            sticky="nsew"
        )

        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        
        # ===================================
        # Selectable Calendars
        # ===================================
        
        # Show all calendars
        calendars = self.google_cal_reader.get_calendars()
        for cal_dict in calendars:
            if cal_dict["calendar_name"] == "ADAMS DAILY JOBS":
                calendars.remove(cal_dict)
                calendars.insert(0,cal_dict)
                break
                
    
        row = 0
        for cal_dict in calendars:
            select_calendar_checkbox = ct.CTkCheckBox(
                master = self.scrollable_frame, text = ""
            )
            select_calendar_checkbox.grid(row = row,column=0)
            select_calendar_checkbox.configure(
                command = lambda cb = select_calendar_checkbox,cal = cal_dict["calendar_name"], cal_id = cal_dict["calendar_id"],colour = cal_dict["bg_colour"]:
                    self.calendar_popup_commands.checkbox_command(cb,cal,cal_id,colour)
            )
            self.gui_main.create_widgets.create_ct_label(
                master = self.scrollable_frame, text = cal_dict["calendar_name"],grid_position = (row,1),text_color = "white",
                font = ct.CTkFont(family="Arial",size=38)
            )
            row += 1
        
        
        
        
        # ===================================
        # EVENTS SECTION
        # ===================================

        events_frame = ct.CTkFrame(
            self.popup_root,
            fg_color=colours.card_background,
            corner_radius=10,
            border_width=1,
            border_color=colours.primary_border
        )

        # Spans calendar and scrollable frame rows
        events_frame.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(10, 20),
            pady=20,
            sticky="nsew"
        )

        events_frame.grid_columnconfigure(0, weight=1)
        events_frame.grid_rowconfigure(1, weight=1)

        # ===================================
        # EVENTS HEADER
        # ===================================

        header_frame = ct.CTkFrame(
            events_frame,
            fg_color="transparent"
        )

        header_frame.grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 10),
            sticky="ew"
        )

        header_frame.grid_columnconfigure(0, weight=1)

        ct.CTkLabel(
            header_frame,
            text="Calendar Events",
            font=("Arial", 19, "bold"),
            text_color=colours.primary_text
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        # Event counter
        self.event_count_label = ct.CTkLabel(
            header_frame,
            text="0 events",
            font=("Arial", 12),
            text_color=colours.muted_text
        )

        self.event_count_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ===================================
        # TREEVIEW
        # ===================================

        self.style_treeview()

        tree_frame = ct.CTkFrame(
            events_frame,
            fg_color=colours.card_background,
            corner_radius=0
        )

        tree_frame.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="nsew"
        )

        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("time", "event", "address", "include"),
            show="headings",
            selectmode="extended",
            style="Calendar.Treeview"
        )

        # Column headings
        self.tree.heading("time", text="TIME", anchor="w")
        self.tree.heading("event", text="EVENT", anchor="w")
        self.tree.heading("address", text="ADDRESS", anchor="w")
        self.tree.heading("include", text="INCLUDE", anchor="center")

        # Column widths
        self.tree.column(
            "time",
            width=90,
            minwidth=75,
            stretch=False,
            anchor="w"
        )

        self.tree.column(
            "event",
            width=180,
            minwidth=120,
            stretch=True,
            anchor="w"
        )

        self.tree.column(
            "address",
            width=250,
            minwidth=150,
            stretch=True,
            anchor="w"
        )

        self.tree.column(
            "include",
            width=90,
            minwidth=80,
            stretch=False,
            anchor="center"
        )

        # Alternating row colours
        self.tree.tag_configure(
            "odd",
            background=colours.card_background,
            foreground=colours.primary_text
        )

        self.tree.tag_configure(
            "even",
            background=colours.tertiary_background,
            foreground=colours.primary_text
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # ===================================
        # TREEVIEW SCROLLBAR
        # ===================================

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        # ===================================
        # IMPORT BUTTON
        # ===================================

        self.gui_main.create_widgets.create_ct_button(
            master=self.popup_root,
            grid_position=(2, 1),
            text="Import",
            sticky="e",
            padx=20,
            pady=(0, 20),
            command=self.calendar_popup_commands.import_to_route_planner_command,
            fg_color=colours.primary_button,
            hover_color=colours.primary_button_hover
        )

  
        
