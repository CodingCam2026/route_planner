
import customtkinter as ct
import re
from collections import defaultdict, deque
from tkinter import messagebox


class SharePopup:
    """Class for managing the share popup for sharing the route"""

    def __init__(self, gui_main):
        self.gui_main = gui_main

    def extract_postcode(self, address):
        pattern = r"\b(?:GIR\s?0AA|[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})\b"

        match = re.search(pattern, str(address), re.IGNORECASE)

        if match:
            return re.sub(r"\s+", "", match.group()).upper()

        return None

    def run_share_popup(self):
        """Runs the share popup"""

        colours = self.gui_main.gui_colours

        self.share_popup_root = ct.CTkToplevel()
        self.share_popup_root.focus()
        self.share_popup_root.grab_set()
        self.share_popup_root.title("Share Route")
        self.share_popup_root.geometry("930x470")
        self.share_popup_root.resizable(False, False)
        self.share_popup_root.configure(
            fg_color=colours.primary_background
        )

        self.share_popup_root.grid_columnconfigure(0, weight=1)

        # Fonts
        details_font = ct.CTkFont(
            family="Arial",
            size=21
        )

        option_font = ct.CTkFont(
            family="Arial",
            size=19
        )

        button_font = ct.CTkFont(
            family="Arial",
            size=19,
            weight="bold"
        )

        # =========================================
        # ROUTE DETAILS - TOP SECTION
        # =========================================

        self.route_details_frame = ct.CTkFrame(
            master=self.share_popup_root,
            fg_color=colours.card_background,
            border_color=colours.primary_border,
            border_width=1,
            corner_radius=12
        )

        self.route_details_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=26,
            pady=(25, 0)
        )

        self.route_details_frame.grid_columnconfigure(
            0, weight=1
        )
        self.route_details_frame.grid_columnconfigure(
            1, weight=1
        )

        
        start_label = ct.CTkLabel(
            master=self.route_details_frame,
            text=f"Start: {self.gui_main.start_entry.get()}",
            font=details_font,
            text_color=colours.primary_text,
            anchor="w"
        )

        start_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(28, 10),
            pady=(22, 10)
        )
        comboboxes = [i for i in self.gui_main.route_listbox.winfo_children() if isinstance(i,ct.CTkComboBox)][2:]
        additional_stop_label = ct.CTkLabel(
            master=self.route_details_frame,
            text=f"Additional Stops: {len(comboboxes)}",
            font=details_font,
            text_color=colours.primary_text,
            anchor="w"
        )

        additional_stop_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(28, 10),
            pady=(0, 10)
        )

        end_label = ct.CTkLabel(
            master=self.route_details_frame,
            text=f"End: {self.gui_main.end_entry.get()}",
            font=details_font,
            text_color=colours.primary_text,
            anchor="w"
        )

        end_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=(28, 10),
            pady=(0, 22)
        )

        total_distance_label = ct.CTkLabel(
            master=self.route_details_frame,
            text=self.gui_main.total_time_label.cget("text"),
            font=details_font,
            text_color=colours.primary_text,
            anchor="w"
        )

        total_distance_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(15, 22),
            pady=(22, 10)
        )

        total_time_label = ct.CTkLabel(
            master=self.route_details_frame,
            text=self.gui_main.total_distance_label.cget("text"),
            font=details_font,
            text_color=colours.primary_text,
            anchor="w"
        )

        total_time_label.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(15, 22),
            pady=(0, 10)
        )

        # =========================================
        # SHARE OPTIONS - FOUR TILES
        # =========================================

        self.share_options_frame = ct.CTkFrame(
            master=self.share_popup_root,
            fg_color="transparent"
        )

        self.share_options_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=26,
            pady=(18, 0)
        )

        for column in range(4):
            self.share_options_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="share_tiles"
            )

        # Google Calendar tile

        google_calendar_tile = ct.CTkFrame(
            master=self.share_options_frame,
            height=145,
            fg_color=colours.card_background,
            border_color=colours.primary_colour,
            border_width=2,
            corner_radius=10
        )

        google_calendar_tile.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        google_calendar_tile.grid_propagate(False)
        google_calendar_tile.grid_columnconfigure(
            0, weight=1
        )

        google_calendar_share_button = ct.CTkButton(
            master=google_calendar_tile,
            text="Google Calendar",
            font=option_font,
            height=42,
            fg_color="transparent",
            hover_color=colours.hover_background,
            text_color=colours.primary_text,
            corner_radius=8
        )

        google_calendar_share_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=(14, 0)
        )

        # Blue selection indicator
        selected_indicator = ct.CTkLabel(
            master=google_calendar_tile,
            text="●",
            font=ct.CTkFont(
                family="Arial",
                size=34
            ),
            text_color=colours.primary_colour
        )

        selected_indicator.place(
            x=18,
            rely=0.78,
            anchor="w"
        )

        # Second tile - placeholder
        second_share_tile = ct.CTkFrame(
            master=self.share_options_frame,
            height=145,
            fg_color=colours.card_background,
            border_color=colours.primary_border,
            border_width=1,
            corner_radius=10
        )

        second_share_tile.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=7
        )

        second_share_tile.grid_propagate(False)

        # Third tile - placeholder
        third_share_tile = ct.CTkFrame(
            master=self.share_options_frame,
            height=145,
            fg_color=colours.card_background,
            border_color=colours.primary_border,
            border_width=1,
            corner_radius=10
        )

        third_share_tile.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=7
        )

        third_share_tile.grid_propagate(False)

        # Fourth tile - placeholder
        fourth_share_tile = ct.CTkFrame(
            master=self.share_options_frame,
            height=145,
            fg_color=colours.card_background,
            border_color=colours.primary_border,
            border_width=1,
            corner_radius=10
        )

        fourth_share_tile.grid(
            row=0,
            column=3,
            sticky="nsew",
            padx=(7, 0)
        )

        fourth_share_tile.grid_propagate(False)

        # =========================================
        # BOTTOM BAR - CALENDAR AND SHARE
        # =========================================

        self.share_frame = ct.CTkFrame(
            master=self.share_popup_root,
            fg_color="transparent"
        )

        self.share_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=26,
            pady=(18, 25)
        )

        self.share_frame.grid_columnconfigure(
            0, weight=1
        )
        self.share_frame.grid_columnconfigure(
            1, weight=0
        )

        self._create_google_car_share_options()
        
        share_button = ct.CTkButton(
            master=self.share_frame,
            text="Share",
            font=button_font,
            width=200,
            height=44,
            fg_color=colours.primary_button,
            hover_color=colours.primary_button_hover,
            text_color=colours.button_text,
            corner_radius=8,
            command=lambda:self.share_button_command()
        )

        share_button.grid(
            row=0,
            column=1,
            sticky="e"
        )

        

    def _create_google_car_share_options(self):
        """Creates the widgets for when you share via google calendar"""

        colours = self.gui_main.gui_colours
        # get calendars minus the se
        try:
            calendar_name = self.gui_main.calendar_popup.calendar_popup_commands.test["calendar"]
        except AttributeError:
            # Has not imported from calendar
            calendar_name = None
        
        calendars = self.gui_main.calendar_popup.calendar_popup_commands.google_cal_reader.get_calendars()
        calendar_names = [i["calendar_name"] for i in calendars]
        if calendar_name:
            calendar_names.remove(calendar_name)
        
            
        self.calendar_options_combobox = ct.CTkComboBox(
            master=self.share_frame,
            values=calendar_names,
            width=260,
            height=44,
            font=ct.CTkFont(
                family="Arial",
                size=18
            ),
            dropdown_font=ct.CTkFont(
                family="Arial",
                size=17
            ),
            fg_color=colours.input_background,
            border_color=colours.input_border,
            border_width=1,
            button_color=colours.secondary_button,
            button_hover_color=colours.secondary_button_hover,
            text_color=colours.input_text,
            dropdown_fg_color=colours.secondary_background,
            dropdown_hover_color=colours.hover_background,
            dropdown_text_color=colours.primary_text,
            corner_radius=8
        )

        self.calendar_options_combobox.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.calendar_options_combobox.set("Calendar")

    def share_button_command(self):
        """Command for sharing the route"""
        try:
            self.gui_main.calendar_popup.selected_calendar_checkbox
        except:
            # Has not imported the route from calendar
            test = {}
        else:
            test = self.gui_main.calendar_popup.selected_calendar_checkbox

        # Get events from the calendar
        calendar_id = test.get("calendar_id")
        date = test.get("date")

        if date and calendar_id:
            events = self.gui_main.calendar_popup.calendar_popup_commands.google_cal_reader.get_events(
                date, calendar_id
            )

            # Get route addresses
            route_addresses = [
                i.get()
                for i in self.gui_main.route_listbox.winfo_children()
                if isinstance(i, ct.CTkComboBox)
            ][2:]

            # Organise calendar events by postcode
            events_by_postcode = defaultdict(deque)

            for event in events:
                postcode = self.extract_postcode(
                    event.get("location", "")
                )

                if postcode:
                    events_by_postcode[postcode].append(event)

            # Match route stops to calendar events
            new_events = []
            unmatched = []

            for address in route_addresses:
                postcode = self.extract_postcode(address)

                if postcode and events_by_postcode[postcode]:
                    event = events_by_postcode[postcode].popleft()
                    new_events.append(event)
                else:
                    unmatched.append(address)

            # Report addresses that could not be matched
            if unmatched:
                messagebox.showwarning(
                    "Unmatched Events",
                    "No matching calendar event found for:\n\n"
                    + "\n".join(unmatched)
                )

            if not new_events:
                return
            
        
            for i,cal_dict in enumerate(self.gui_main.calendar_popup.calendar_popup_commands.google_cal_reader.get_calendars()):
                print(cal_dict["calendar_name"],self.calendar_options_combobox.get())
                
                if cal_dict["calendar_name"].strip().lower() == self.calendar_options_combobox.get().strip().lower():
                    target_cal_id = cal_dict["calendar_id"]
                    break
            
            else:
                messagebox.askretrycancel(
                    title="Select Calendar",
                    message="Please select a valid calendar"
                )
                return None

            #target_cal_id = "l0n9c98g86amrp693s024vhoks@group.calendar.google.com"

            i = 0

            for e in events:
                if e.get("location"):
                    new_event = {
                        "summary": new_events[i]["summary"],
                        "location": new_events[i]["location"],
                        "description": "",
                        "start": {
                            "dateTime": e["start"]["dateTime"],
                            "timeZone": "Europe/London"
                        },
                        "end": {
                            "dateTime": e["end"]["dateTime"],
                            "timeZone": "Europe/London"
                        }
                    }

                    i += 1

                    
                    self.gui_main.calendar_popup.calendar_popup_commands.google_cal_reader.copy_event(
                        event=new_event,
                        target_calendar_id=target_cal_id
                    )
            
            messagebox.askokcancel(
                title="Sucess",
                message=f"Calendar shared to {self.calendar_options_combobox.get()}"
            )
                    
                    

        else:
            print("Calendar not imported ")
