# Imports for optimising route
import openrouteservice
import os
from dotenv import load_dotenv
import requests

class RouteOptimizer:
    """Class for managing the logic for optimising the route"""
    def __init__(self):
        API_KEY = self.load_api_key()
        self.client = openrouteservice.Client(
            key=API_KEY,
            base_url="https://api.heigit.org/openrouteservice"
        )
        
        self.optimization_url = "https://api.heigit.org/vroom/v0"
        
        self.headers = {
            "Authorization": API_KEY,
            "Content-Type": "application/json"
        }
        
    
    def load_api_key(self):
        """Loads the api key from the .env file and returns it"""
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        if not API_KEY:
            raise ValueError("Set API_KEY in your .env file")
        return API_KEY
    
    
    def _create_route_payload(self,route_list):
        """Takes a list of coords as route_list and creates the payload for the request returns the payload"""
        start_coords, additional_stops, end_coords = self._create_route_payload_stops(route_list)
        
        payload = {
            "jobs": additional_stops,
            "vehicles": [
                {
                    "id": 1,
                    "profile": "driving-car",
                    "start": start_coords,
                    "end": end_coords
                }
            ]
        }
        return payload
    
    def _create_route_payload_stops(self,route_list):
        """Takes the stops from route_list and returns the start_coords,addiontal_stop list and end_coords"""
        additional_stops = []
        
        for i, coord in enumerate(route_list[1:-1]):
            additional_stops.append(
                {"id":i+1,"location":coord}
                )
        
        start_coords = route_list[0]
        end_coords = route_list[-1]
        
        return start_coords,additional_stops,end_coords
        
    def send_request(self,route_list):
        """Sends the payload"""
        response = requests.post(
            self.optimization_url,
            headers=self.headers,
            json=self._create_route_payload(route_list)
        )
        # check for response 200
        return response.json()
    

    def _calculate_total_distnace(self,address_dict):
        """Calculates the total distance from all stops"""
        # Get all coords from route
        all_coords = []
        for stop,address in address_dict.items():
            if isinstance(address,dict):
                for a in address.items():
                    all_coords.append((a[1].longitude,a[1].latitude))
            else:
                all_coords.append((address.longitude,address.latitude))
        
        
        # Calculate directions and travel time
        route_legs = []  
        for i in range(len(all_coords) - 1):
            start = all_coords[i]
            end = all_coords[i + 1]
            
            route = self.client.directions(
                coordinates=[
                    start,
                    end
                ],
                profile="driving-car",
                preference="fastest",
                format="geojson"
            )
            route_legs.append(route)
            
        
        # calculate total distance
        total_distance = 0
        total_duration = 0
        

        for i, route in enumerate(route_legs):

            summary = route["features"][0]["properties"]["summary"]

            distance_miles = summary["distance"] / 1609.344
            duration_minutes = summary["duration"] / 60
            
            total_distance += distance_miles
            total_duration += summary["duration"]
        
        return total_distance,total_duration
        
        