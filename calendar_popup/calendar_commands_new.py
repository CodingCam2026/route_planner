
from calendar_readers.ical_reader import IcalReader
from calendar_readers.google_cal_reader import GoogleCalendarReader
from datetime import date, datetime
from tkinter import messagebox
import customtkinter as ct

class CalendarCommands:
    """Class for managing the calendar commands"""
    def __init__(self,calendar_main):
        self.calendar_main = calendar_main
        self.gui_colours = self.calendar_main.gui_main.gui_colours
        self.ical_reader = IcalReader()
        self.google_cal_reader = GoogleCalendarReader()
        self.selected_calendar_bool = False
    
    
    def today_button_command(self):
        """Command for selecting the day back to today"""
        today = date.today()
        self.calendar_main.calendar.selection_set(today)
    
    
    def import_to_route_planner_command(self):
        """Command for importing the postcodes into the route planner"""
        # Checks for valid locations and creates a dict
        locations = {}
        no_locations = []
        for row_id in self.calendar_main.tree.get_children():
            values = self.calendar_main.tree.item(row_id, "values")
            address = values[2]
            postcode = " ".join(address.split()[-2:])
            if postcode != "N/A":
                # check it is a valid postcode
                location = self.calendar_main.gui_main.gui_commands.geocode(
                    postcode,
                    country_codes="gb",
                    exactly_one=True,
                    addressdetails=True
                )
                if location:
                    locations[address] = "found"
                else:
                    locations[address] = "not_found"
            else:
                # Dont import the address
                no_locations.append(values[1])
        
        # Show message box for events with no location
        if no_locations:
            calendar = self.calendar_main.selected_calendar_checkbox["calendar"]
            message = f'{calendar} has {len(no_locations)} events with no location\n{", ".join([i for i in no_locations])}.\nThese will not be imported'
            messagebox.showinfo(
                title="No location",
                message=message
            )
            
        # Remove additional comboboxes
        for widget in self.calendar_main.gui_main.route_listbox.winfo_children()[5:]:
            widget.destroy()
        
        
        # import evetns into the route
        for location, status in locations.items():
                postcode = " ".join(location.split()[-2:])
                self.calendar_main.gui_main.gui_commands.add_stop_command(postcode)
        
        self.calendar_main.popup_root.destroy()
        self.test = self.calendar_main.selected_calendar_checkbox
        
    
    def get_events(self,calendar_day):
        """Gets the events of the selected calendar"""
        data = self.calendar_main.selected_calendar_checkbox
        # Get the events from that calendar above
        if data:
            events = self.google_cal_reader.get_events(calendar_day,data["calendar_id"])
            # Save the date of the events actually loaded, not the date
            # selected when the calendar checkbox was first clicked.
            data["date"] = calendar_day
        else:
            messagebox.askretrycancel(
                title="No Calendar Selected",
                message="No Calendar is selected, please select one"
            )
            return None
            
            
        # Clear the tree
        for row_id in self.calendar_main.tree.get_children():
            self.calendar_main.tree.delete(row_id)
            
        # Insert events into the tree
        for event in events:
            
            # Checks if there is a location
            if event.get("location"):
                location = event.get("location")
            else:
                location = "N/A"
                
            self.calendar_main.tree.insert(
                "",
                "end",
                values=(
                    "Time",
                    event["summary"].strip(),
                    location,
                    ""
                ),
                #tags=(tag_name,)
            )
            
        
        
    def checkbox_command(self,checkbox,calendar,calendar_id,colour):
        """Command for """
        details = {"checkbox":checkbox,"calendar":calendar,"calendar_id":calendar_id,"colour":colour,"date":self.calendar_main.calendar.selection_get()}
        if checkbox.get() == 1:
            # Unchecked
            self.calendar_main.selected_calendar_checkbox = details
        
        [i.deselect() for i in self.calendar_main.scrollable_frame.winfo_children() if isinstance(i,ct.CTkCheckBox)]
        checkbox.select()
    