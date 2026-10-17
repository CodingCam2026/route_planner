# Import for gui creation
from widget_toolkit.widget_factory import CreateWidgets
import customtkinter as ct
import asyncio
from winsdk.windows.devices.geolocation import Geolocator, PositionAccuracy
from gui_commands import GUICommands
from map_creation import MapCreation
from gui_colours.gui_colours import GUIColours
from PIL import Image


class Fonts:
    """Class for defining fonts for the GUI"""
    def __init__(self):
        self.route_entry_font = ct.CTkFont(family="Arial",size=30)
        self.total_route_detail_font = ct.CTkFont(family="Arial",size=36)


class GUIMain:
    """Class for running the gui"""
    def __init__(self):
        """"""
        self.create_widgets = CreateWidgets()
        self.gui_commands = GUICommands(self)
        
        
    
    def get_current_lat_long(self):
        """Gets the current latitude and longitude using Windows location services."""

        async def get_position():
            locator = Geolocator()
            locator.desired_accuracy = PositionAccuracy.HIGH

            position = await locator.get_geoposition_async()

            latitude = position.coordinate.point.position.latitude
            longitude = position.coordinate.point.position.longitude

            return latitude, longitude

        try:
            return asyncio.run(get_position())

        except Exception as e:
            print(f"Error getting location: {e}")
            return None

    
    
    
    
    def create_stop_entry(self,placeholder_text,grid):
        """Creates the stop entry widget"""
        entry = self.create_widgets.create_ct_combobox(
            master = self.route_listbox,values = [],
            grid_position = grid,
            width = 250, padx = 10,pady = 5,
            font = self.fonts.route_entry_font,
            fg_color = self.gui_colours.primary_border
            
            )
        entry.set(placeholder_text)
        def restore_focus(event):
            """Restore focus on combobox after map interaction"""
            entry.after(50, lambda: entry._entry.focus_force())

        entry._entry.bind("<Button-1>", restore_focus, add="+")
        
        return entry
    
    def _create_search_address_button(self,grid,combobox):
        """Creates the search address button"""
        button_image = ct.CTkImage(
            light_image=Image.open("images/search_address_icon.png"),
            dark_image=Image.open("images/search_address_icon.png"),
            size=(34,34)
        )
        search_address_button = self.create_widgets.create_ct_button(
            master = self.route_listbox, grid_position = grid,
            command = lambda :self.gui_commands.search_address_command(combobox),
            image = button_image,width = 20,fg_color  = self.gui_colours.primary_button,hover_color = self.gui_colours.primary_button_hover 
        )
        return search_address_button
    
    
    def run_gui(self):
        """Runs the gui"""
        self.root = ct.CTk()
        self.gui_colours = GUIColours()
        self.map_creation = MapCreation(self)
        map_location = "starting_map"
        self.map_creation.create_map_from_location(self.get_current_lat_long(),map_location)
        
        self.fonts = Fonts()
        self.map_creation.display_map_from_path(f"{map_location}.html")

        self.root.configure(fg_color=self.gui_colours.primary_background)
        self.route_listbox = self.create_widgets.create_ct_scrollable_frame(
            master = self.root, grid_position = (0,0),height=600,width =500,
            padx = 10,pady=10,fg_color = self.gui_colours.secondary_background
            )
        
        stop_frame = self.create_widgets.create_ct_frame(
            master = self.route_listbox, grid_position = (0,0)
        )

        # Start Entry
        self.start_entry = self.create_stop_entry(placeholder_text="Start",grid=(0,0))
        self.start_search_address_button = self._create_search_address_button(grid = (0,1),combobox=self.start_entry)
      
        # Stop Entry
        self.end_entry = self.create_stop_entry(placeholder_text="End",grid=(1,0))
        self.end_search_address_button = self._create_search_address_button(grid = (1,1),combobox=self.end_entry)
    
        button_frame = self.create_widgets.create_ct_frame(
            master = self.root,grid_position = (1,0),
            fg_color = self.gui_colours.primary_background
        )
        # Add stop button
        add_stop_button = self.create_widgets.create_ct_button(
            master = button_frame, text = "Add Stop",
            grid_position = (1,0),
            width = 250, padx = 10,
            font = self.fonts.route_entry_font,command = self.gui_commands.add_stop_command,
            height = 50,fg_color = self.gui_colours.secondary_button,hover_color = self.gui_colours.secondary_button_hover,
            text_color = self.gui_colours.primary_text
            
        )
        
        calulate_route_button = self.create_widgets.create_ct_button(
            master = button_frame, text = "Calculate Route",
            grid_position = (1,1),
            width = 250, padx = 10,
            font = self.fonts.route_entry_font,command = lambda:self.gui_commands.calulate_route_command(),
            height = 50, fg_color = self.gui_colours.primary_button,hover_color = self.gui_colours.primary_button_hover,
            
        )
        
        # Total route distance
        route_details_frame = self.create_widgets.create_ct_frame(
            master = self.root, grid_position=(2,0),fg_color = self.gui_colours.secondary_background,
            pady =30
        )
        
        self.total_distance_label = self.create_widgets.create_ct_label(
            master = route_details_frame, text = "Total Distance 0 Miles",
            grid_position=(0,0),text_color = self.gui_colours.primary_text,font = self.fonts.total_route_detail_font,
            padx=70,pady=10
        )
        
        self.total_time_label = self.create_widgets.create_ct_label(
            master = route_details_frame, text = "Total Time 0 Hours",
            grid_position=(1,0),text_color = self.gui_colours.primary_text,font = self.fonts.total_route_detail_font,
            pady=10
        )
        

        # Return keyboard focus to whichever entry you click after map interaction
        self.return_combobox_focus()
  
        self.root.mainloop()
    
    def return_combobox_focus(self):
        """Returns the focus on the combobox"""
        entries = [i for i in self.route_listbox.winfo_children() if isinstance(i,ct.CTkComboBox)]
        for entry in entries:
            entry.bind(
                "<Button-1>",
                lambda event, e= entry: self.root.after_idle(e.focus_force),
                add="+"
            )
            
        

GUIMain().run_gui()
