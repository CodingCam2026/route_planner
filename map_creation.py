import tkinter as tk
from pathlib import Path
from tkwry import WebView
import folium
import customtkinter as ct

class MapCreation:
    """Class for creating, displaying and the map"""
    def __init__(self,gui_main):
        self.gui_main = gui_main
        self.root = self.gui_main.root
    
    
    def create_map_from_location(self,current_lat_long,map_name):
        """Creates the starting map from the current lat and long"""
        map = folium.Map(location=current_lat_long)
        map.save(f"{map_name}.html")
        return map
    
    def create_map_container(self):
        """Creates the map container"""
        # Container for map and toolbar
        self.map_container = ct.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.map_container.grid(
            row=0,
            column=1,
            rowspan=4,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # Configure container grid
        self.map_container.grid_columnconfigure(0, weight=1)
        self.map_container.grid_rowconfigure(1, weight=1)

        
            
            
    def display_map_from_path(self,map_path):
        """Displays the folium map from the map path"""
        # Configure root grid
        # Create map frame inside container
        self.map_frame = tk.Frame(
            self.map_container,
            width=800,
            height=600,
            bg="lightblue"
        )

        self.map_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(5, 0)
        )

        self.map_frame.grid_propagate(False)
        self.map_frame.pack_propagate(False)

    
        # Read Folium map
        map_html = Path(map_path).read_text(encoding="utf-8")

        self.map_browser = WebView(
            self.map_frame,
            html="<h2>Browser started — loading map...</h2>",
            user_agent="CamRoutePlanner/1.0",
            devtools=True
        )

        self.map_browser.when_ready(lambda:self.map_browser.load_html(map_html))

        self.map_browser.when_failed(
            lambda error: print("Browser creation failed:", error)
        )
        
    
    
    def create_map_stops(self,route_list):
        """Creates the map including map markers and route lines for each stop in the route"""
        #print(route_list)
        starting_lat_long = (route_list["start"].latitude,route_list["start"].longitude)
        calculated_route_map  = folium.Map(location=starting_lat_long)
        
        self._create_map_markers(route_list,calculated_route_map)
        self._create_route_lines(route_list,calculated_route_map)
            
        # Save map
        map_name = "html_maps/new_map.html"
        calculated_route_map.save(map_name)
        self.display_map_from_path(map_name)
        self.gui_main.return_combobox_focus()
    
    
    def _create_map_markers(self,route_list,calculated_route_map):
        """Creates the map markers for the folium map from the route_list"""
        for stop,address in route_list.items():
            if isinstance(address,dict):
                # Dealing with addiotnal jobs
                job_number = 1
                coord_list = [(i[1].latitude,i[1].longitude) for i in address.items()]
                for coord in coord_list:
                    folium.Marker(
                            location=(coord[0],coord[1]),
                            tooltip=f"Stop {job_number}",
                            popup=[i for i in address.items()][job_number-1][1],
                            icon=folium.Icon(icon="home",color="blue"),
                        ).add_to(calculated_route_map)
                    job_number += 1
                
            else:
                # Only a start and end
                coords = (address.latitude,address.longitude)
                if (route_list["start"].latitude,route_list["start"].longitude) == (route_list["end"].latitude,route_list["end"].longitude): 
                    stop = "Start / End"
                    color = "green"
                else:
                    color = "blue"
                    
                folium.Marker(
                    location=(coords[0],coords[1]),
                    tooltip=stop,
                    popup=address,
                    icon=folium.Icon(icon="home",color=color),
                ).add_to(calculated_route_map)
    
    
    def _create_route_lines(self,route_list,calculated_route_map):
        """Creates the route lines for the folium map from the route_list"""
        starting_lat_long = (route_list["start"].latitude,route_list["start"].longitude)
        prev_long_lat = (starting_lat_long[0],starting_lat_long[1])
        for stop,address in route_list.items():
            if isinstance(address,dict):
                coords = [(i[1].latitude,i[1].longitude) for i in address.items()]
                for c in coords:
                    route = self.gui_main.gui_commands.route_optimizer.client.directions(
                            coordinates=[
                                [prev_long_lat[1], prev_long_lat[0]],
                                [c[1], c[0]],
                            ],
                            profile="driving-car",
                            format="geojson",
                        )
                    prev_long_lat = c
                    
                    route_layer = folium.GeoJson(
                        route,
                        name="Driving route",
                        style_function=lambda feature: {
                            "color": "blue",
                            "weight": 5,
                            "opacity": 0.8,
                        },
                        ).add_to(calculated_route_map)
            else:
                coords = (address.latitude,address.longitude)
            
                route = self.gui_main.gui_commands.route_optimizer.client.directions(
                    coordinates=[
                        [prev_long_lat[1], prev_long_lat[0]],
                        [coords[1], coords[0]],
                    ],
                    profile="driving-car",
                    format="geojson",
                )
                
                prev_long_lat = coords
                                        
                route_layer = folium.GeoJson(
                    route,
                    name="Driving route",
                    style_function=lambda feature: {
                        "color": "blue",
                        "weight": 5,
                        "opacity": 0.8,
                    },
                    ).add_to(calculated_route_map)
