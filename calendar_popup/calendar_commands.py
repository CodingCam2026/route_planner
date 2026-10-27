
from calendar_readers.ical_reader import IcalReader
from calendar_readers.google_cal_reader import GoogleCalendarReader
from datetime import date, datetime
from tkinter import messagebox
import customtkinter as ct

class CalendarPopupCommands:
    """Class for managing the commands for the calendar popup"""
    def __init__(self,calendar_main):
        self.calendar_main = calendar_main
        self.gui_colours = self.calendar_main.gui_main.gui_colours
        self.ical_reader = IcalReader()
        self.google_cal_reader = GoogleCalendarReader()
        self.selected_calendar_checkbox = []
        self.selected_calendar_bool = False
    
    def get_events(self, calendar_day):
        """Get calendar events when the date is selected."""
        #print(self.selected_calendar_checkbox)
        if not self.selected_calendar_checkbox:
            messagebox.askretrycancel(
                title="Select Calendar",
                message="Please select a calendar"
            )
            return None
            
        elif len(self.selected_calendar_checkbox) >= 2:
            messagebox.askretrycancel(
                title="To many Calendar",
                message="Please select only 1 calendar"
            )
            return None
        
        # events = self.ical_reader.get_events(calendar_day)
        events = []
        for selected_calendar_dict in self.selected_calendar_checkbox:
            events.append(self.google_cal_reader.get_events(calendar_day,selected_calendar_dict["calendar_id"]))
       
        
        # Clear previous events
        for row_id in self.calendar_main.tree.get_children():
            self.calendar_main.tree.delete(row_id)

        
        no_locations = {}
        # Add events
        for event_dict in events:
            t = []
            for event in event_dict:
                if not event.get("location"):
                    #self.selected_calendar_checkbox = []
                    if event["organizer"]["email"] == "shelteradams01@gmail.com":
                        owner = "Rob"
                        
                        
                    else:
                        owner = event["organizer"]["displayName"]
                    
                    t.append(event["summary"])   
                    no_locations[owner] = t
                    
                else:   
                    organizer = event["organizer"]["displayName"]
                    background_colour = [i["colour"] for i in self.selected_calendar_checkbox if i["calendar"] == organizer][0]
                    if organizer == "ADAMS DAILY JOBS":
                        foreground = "black"
                    else:
                        foreground = "white"
                    tag_name = organizer
                    
                    self.calendar_main.tree.tag_configure(
                        tag_name,
                        background=background_colour,
                        foreground=foreground
                    )
                    
                    self.calendar_main.tree.insert(
                        "",
                        "end",
                        values=(
                            "Time",
                            event["summary"].strip(),
                            event["location"],
                            ""
                        ),
                        tags=(tag_name,)
                    )
        
    
        if no_locations:
            message = ""
            for owner, e in no_locations.items():
                message += f"{owner.strip()} has {', '.join([i for i in e])} events with no locations"
                message += "\n"
            
            messagebox.askretrycancel(
                title="",
                message=message
            )
        #print(", ".join(no_locations))
        # # Update event counter
        # count = len(events)

        # self.calendar_main.event_count_label.configure(
        #     text=f"{count} event{'s' if count != 1 else ''}"
        # )
        
        # Show message box for not valid locations
        
        
            # for cal_name in calendars_no_locations:
            #     print(f"{cal_name} has no location for {[i[1]['summary'] for i in calendars_no_locations.items()]}")
            
                    
                    

    def today_button_command(self):
        """Command for setting the day back to today."""

        today = date.today()
        self.calendar_main.calendar.selection_set(today)

    def import_to_route_planner_command(self):
        """Import calendar events into the route planner."""

        valid_locations = self._check_valid_location()
       
        # Remove additional comboboxes
        for widget in self.calendar_main.gui_main.route_listbox.winfo_children()[5:]:
            widget.destroy()

         
        for location, status in valid_locations.items():
            postcode = " ".join(location.split()[-2:])
            self.calendar_main.gui_main.gui_commands.add_stop_command(postcode)
        
        #print()
        #print(self.selected_calendar_checkbox)
        self.calendar_main.gui_main.route_details["calendars"] = [i["calendar"] for i in self.selected_calendar_checkbox]
        self.calendar_main.popup_root.destroy()
        self.selected_calendar_checkbox.clear()

    def _check_valid_location(self):
        """Checks the location via its postcode."""

        address_located = {}

        for row_id in self.calendar_main.tree.get_children():

            values = self.calendar_main.tree.item(row_id, "values")
            address = values[2]

            postcode = " ".join(address.split()[-2:])

            locations = self.calendar_main.gui_main.gui_commands.geocode(
                postcode,
                country_codes="gb",
                exactly_one=True,
                addressdetails=True
            )

            if locations:
                address_located[address] = "found"
            else:
                address_located[address] = "not_found"

        return address_located
    
    
    def checkbox_command(self,checkbox,calendar,calendar_id,colour):
        """Command for setting which checkbox is selected"""
        d = {"checkbox":checkbox,"calendar":calendar,"calendar_id":calendar_id,"colour":colour}
        if checkbox.get() == 1:
            # Unchecked
            self.selected_calendar_checkbox.append(d)
        else:
            if d in self.selected_calendar_checkbox:
                self.selected_calendar_checkbox.remove(d)
        
        # [i.deselect() for i in self.calendar_main.scrollable_frame.winfo_children() if isinstance(i,ct.CTkCheckBox)]
        # checkbox.select()
        
       
            
        
            
        
        
        
            