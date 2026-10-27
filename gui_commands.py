from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from route_optimizer import RouteOptimizer
import customtkinter as ct
from PIL import Image



class GUICommands:
    """Class for managing the gui commands"""
    def __init__(self,gui_main):
        self.gui_main = gui_main
        self.create_widgets = self.gui_main.create_widgets
        self.route_optimizer = RouteOptimizer()
        self.calendar_popup = self.gui_main.calendar_popup
        
        
        geolocator = Nominatim(
            user_agent="route_planner",
            timeout=10,
        )

        self.geocode = RateLimiter(
            geolocator.geocode,
            min_delay_seconds=1,
        )
        

    def add_stop_command(self,place_holder_text = "Additonal Stop"):
        """Command for adding a entry widget for an addiontal stop"""
        # Configures the row to place after addiotnal stop and before end stop
        route_widgets = self.gui_main.route_listbox.winfo_children()
        route_widgets_grid_info = [i.grid_info() for i in route_widgets]
        route_widgets_coords = [(i.get("row"),i.get("column")) for i in route_widgets_grid_info]
        i = max(route_widgets_coords)[0]
        
        # Create additional stop widgets 
        entry_stop = self.gui_main.create_stop_entry(placeholder_text=place_holder_text,grid=(i,0))
        search_address_button = self.gui_main._create_search_address_button(grid = (i,1),combobox = entry_stop)
        button_image = ct.CTkImage(
                    light_image=Image.open("images/remove_stop_icon.png"),
                    dark_image=Image.open("images/remove_stop_icon.png"),
                    size=(34,34)
                )
    
        delete_stop_button = self.create_widgets.create_ct_button(
            master = self.gui_main.route_listbox, grid_position = (i,2),
            command = lambda:self.delete_stop_command(entry_stop,delete_stop_button,search_address_button)
            ,width = 50,height = 42,padx=5,image = button_image,
            fg_color = self.gui_main.gui_colours.danger,hover_color = self.gui_main.gui_colours.danger_hover
        )
        
        # Configure End combobox and search button placement
        self.gui_main.end_entry.grid_configure(row = i+1)
        self.gui_main.end_search_address_button.grid_configure(row = i+1)
    
    
    def delete_stop_command(self,entry_stop,del_button,search_button):
        """Command for removing a additional stop"""
        entry_stop.destroy()
        del_button.destroy()
        search_button.destroy()
  
    
    
        
    def search_address_command(self,combobox):
        """Searches for matched addresses and sets the results as the combobox values"""
        locations = self.geocode(
            combobox.get(),
            country_codes="gb",
            exactly_one=False,
            limit=10,
            addressdetails=True
        )
        if locations:
            combobox.configure(values = [i.address for i in locations])
            
            # print("Matched address:", location.address)
            # print("Latitude:", location.latitude)
            # print("Longitude:", location.longitude)
            
    
    def calulate_route_command(self):
        """Calculates the route"""
        # get long and lat from each address
        route_widgets = self.gui_main.route_listbox.winfo_children()
        matched_location = self._get_address_long_lat(route_widgets)
                    
        
        if len(matched_location) > 2:
            # Addiontal stops
            address_dict = self._create_additional_stops_address_dict(matched_location,route_widgets)
           
        else:
            address_dict = self._create_start_and_end_address_dict(matched_location)
                        
       
        # create map and display markers and lines from address dict
        self.gui_main.map_creation.create_map_stops(address_dict)
        # display total distance 
        total_distance, total_duration = self.route_optimizer._calculate_total_distnace(address_dict)
        
        hours = int(total_duration // 3600)
        minutes = int((total_duration % 3600) // 60)
        
        if hours < 1:
            text = f"Total Time {minutes} Minutes"
        else:
            text = f"Total Time {hours} Hours {minutes} Minutes"
            
        self.gui_main.total_distance_label.configure(text = f"Total Distance {round(total_distance)} Miles")
        self.gui_main.total_time_label.configure(text = text)
        
    
    def _get_address_long_lat(self,route_widgets):
        """Gets the long and lat from each address and returns the matched_location"""
        matched_location = []
        for address in [i.get().strip() for i in route_widgets if isinstance(i,ct.CTkComboBox)]:
            if address != "Start" and address != "End":
                location = self.geocode(address, country_codes="gb")
                if location:
                    matched_location.append(location)
        
        return matched_location


    def _order_uncalculated_comboboxes(self,route_widgets,address_dict):
        """Orders the comboboxes from the calculated route"""
        widgets = [i for i in route_widgets if isinstance(i,ct.CTkComboBox)][2:]
        for i,address in enumerate(address_dict["jobs"].items()):
            widgets[i].set(address[1])
    
    
    def _create_start_and_end_address_dict(self,matched_location):
        """Creates the start and end only dictionary used for route calculation and returns it"""
        address_dict = {}
        location_command = lambda index : matched_location[index]
        address_dict["start"] = location_command(0)
        address_dict["end"] = location_command(1)
        return address_dict
    
    def _create_additional_stops_address_dict(self,matched_location,route_widgets):
        """Creates the start and end only dictionary used for route calculation and returns it"""
        ors_coords = [(i.longitude,i.latitude) for i in matched_location]
        end_stop = ors_coords.pop(1)
        ors_coords.append(end_stop)
        optimized_route = self.route_optimizer.send_request(ors_coords)
        steps = optimized_route["routes"][0]["steps"]
        
        steps = optimized_route["routes"][0]["steps"]
        optimized_coords = []

        for step in steps:
            if step["type"] in ["start", "job", "end"]:
                optimized_coords.append(step["location"])
        
        address_dict = {}
        jobs = {}
        for step in steps:

            if step["type"] == "start":
                address_dict["start"] = matched_location[0]

            elif step["type"] == "job":
                job_id = step["job"]
                step_coords = (step["location"][1],step["location"][0])
                mc = [i for i in matched_location if (i.latitude,i.longitude) == step_coords][0]
                jobs[job_id] = mc
                address_dict["jobs"] = jobs

            elif step["type"] == "end":
                address_dict["end"] = matched_location[1]
                
        self._order_uncalculated_comboboxes(route_widgets,address_dict)
        #print(address_dict)
        
        return address_dict
    
    def calendar_popup_command(self):
        """Command for running the popup for the calendar"""
        self.calendar_popup.popup()
        # Make calendar
        
        
        # get events
        
        
    