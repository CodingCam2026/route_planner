import folium
from folium.plugins import PolyLineTextPath
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import openrouteservice
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Set API_KEY in your .env file")

geolocator = Nominatim(
    user_agent="route_planner",
    timeout=10,
)

geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1,
)
address_list = []

start_flag = True
end_flag = True
loop_bool = True
while loop_bool:
    if start_flag:
        address = input("Enter the start location full address: ").strip()
        start_flag = False
    else:
        address = input("Enter addintional stop full address (enter q to enter end location): ").strip()
        if address == "q":
            address = input("Enter end location full address: ").strip()
            end_flag = False
            
    
    
    location = geocode(address, country_codes="gb")
    

    if location:
        print("Matched address:", location.address)
        print("Latitude:", location.latitude)
        print("Longitude:", location.longitude)
        address_list.append({location.address:(location.latitude,location.longitude)})
        if not end_flag:
            loop_bool = False
        
    
    else:
        print("Address not found")



address_list_coords = [[i for i in i.values()][0] for i in address_list]


ors_coords = [(i[1],i[0]) for i in address_list_coords]

start_coords = ors_coords[0]
addintional_stops_coords = ors_coords[1:-1]
end_coords = ors_coords[-1]

additional_stops = []

for i, coord in enumerate(addintional_stops_coords):
    additional_stops.append(
        {"id":i+1,"location":coord}
        )

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



client = openrouteservice.Client(
    key=API_KEY,
    base_url="https://api.heigit.org/openrouteservice"
)

optimization_url = "https://api.heigit.org/vroom/v0"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(
    optimization_url,
    headers=headers,
    json=payload
)

optimized = response.json()
steps = optimized["routes"][0]["steps"]

optimized_coords = []

for step in steps:
    if step["type"] in ["start", "job", "end"]:
        optimized_coords.append(step["location"])



route_legs = []

for i in range(len(optimized_coords) - 1):

    start = optimized_coords[i]
    end = optimized_coords[i + 1]

    route = client.directions(
        coordinates=[
            start,
            end
        ],
        profile="driving-car",
        preference="fastest",
        format="geojson"
    )

    route_legs.append(route)
   
   
total_distance = 0
total_duration = 0
 

for i, route in enumerate(route_legs):

    summary = route["features"][0]["properties"]["summary"]

    distance_miles = summary["distance"] / 1609.344
    duration_minutes = summary["duration"] / 60
    
    total_distance += summary["distance"]
    total_duration += summary["duration"]
   
    
    


new_address_list = []

for step in steps:

    if step["type"] == "start":
        new_address_list.append(address_list[0])

    elif step["type"] == "job":

        job_id = step["job"]

        new_address_list.append(
            address_list[job_id]
        )

    elif step["type"] == "end":
        new_address_list.append(address_list[-1])



map = folium.Map(location=[[i for i in i.values()][0] for i in new_address_list][0])


# Make Map Markers
stop_counter = 1    
for item in new_address_list:
    coords = [i for i in item.values()][0]
    if (start_coords[1],start_coords[0]) == coords and (end_coords[1],end_coords[0]) == coords:
        tool_tip = f"1 / {len(address_list)}"
    else:
        tool_tip = stop_counter
        
        
    folium.Marker(
        location=(coords[0],coords[1]),
        tooltip=tool_tip,
        popup="Helo",
        icon=folium.Icon(icon="cloud",color="blue"),
    ).add_to(map)
    
    stop_counter += 1  
    

# Draw the route lines
prev_long_lat = (start_coords[1],start_coords[0])
for item in new_address_list[1:]:
    coords = [i for i in item.values()][0]
    route = client.directions(
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
    ).add_to(map)
    
    
map.save("index.html")

print("Map Saved")
print("############################")
miles = round(total_distance / 1609,1)
mins = total_duration / 60
hours = mins / 60
if hours < 1:
    print(f"Route is {miles} miles and will take {mins} minutes")
else:
    if mins >= 60:
        remaining_mins = mins - 60
        hours += 1
        print(f"Route is {miles} miles and will take {hours} hours and {remaining_mins} minutes")

