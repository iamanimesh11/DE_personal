from collections import defaultdict
from Database_connection import connect_Database
import psycopg2
from psycopg2 import extras

import requests

import folium
conn = connect_Database()
if conn==None:
    exit()


#step 1 get all road data from lat,lon,radius and calc bounding box points
def get_osm_data(lat, lon, radius):
    # Define a bounding box (latitude and longitude of the area of interest)
    # Define bounding box coordinates
    north, south, east, west = calc_bounding_box_points(lat, lon, radius)
    # Overpass API query for roads (can be customized for other features like traffic, incidents, etc.)
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    way["highway"~"secondary|tertiary|primary"]
    ({south},{west},{north},{east});
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    if response.status_code == 200:
        data = response.json()
        return data.get("elements", []), north, east, west, south
    else:
        raise Exception(f"Error fetching OSM data: {response.status_code}, {response.text}")


def calc_bounding_box_points(lat, lon, radius):
    from math import radians, cos
    Earth_radius = 6371.0
    delta_lat = radius / Earth_radius
    delta_lon = radius / (Earth_radius * cos(radians(lat)))
    north = lat + delta_lat
    south = lat - delta_lat
    east = lon + delta_lon
    west = lon - delta_lon
    return north, south, east, west


# Function to get node details (coordinates) from Overpass API
def get_node_coordinates(node_ids):
    overpass_url = "http://overpass-api.de/api/interpreter"
    node_query = f"""
    [out:json];
    node(id:{','.join(map(str, node_ids))});
    out body;
    """
    response = requests.get(overpass_url, params={'data': node_query})
    if response.status_code == 200:
        data = response.json()
        return {node["id"]: (node["lat"], node["lon"]) for node in data.get("elements", [])}
    else:
        raise Exception("Error fetching node coordinates.")


def merge_road_segments(roads):
    # Group roads by name
    grouped_roads = defaultdict(lambda: {"type": None, "nodes": []})

    for road in roads:
        road_name = road["name"]
        road_type = road["type"]
        nodes = road["nodes"]

        # Add nodes and ensure road type consistency (if needed)
        grouped_roads[road_name]["type"] = road_type
        grouped_roads[road_name]["nodes"].extend(nodes)

    # Remove duplicate nodes for each road
    merged_roads = []
    for name, data in grouped_roads.items():
        unique_nodes = list(dict.fromkeys(data["nodes"]))  # Remove duplicates while maintaining order
        merged_roads.append({"name": name, "type": data["type"], "nodes": unique_nodes})

    return merged_roads


def process_road_data(road_data):
    roads = []
    for element in road_data:
        if element["type"] == "way" and "tags" in element:
            tags = element["tags"]
            road_name = tags.get("name", "Unknown Road")
            road_type = tags.get("highway", "Unknown Type")
            nodes = element.get("nodes", [])  # Get list of node IDs
            roads.append({"name": road_name, "type": road_type, "nodes": nodes})
    return roads


def tomotom_Api(lat, lon):
    API_KEY = "EQEuzLbnAf2rBfIu244A8ds4A3sPD6BK"
    necessary_details = []
    # TomTom Traffic Flow API URL
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    try:
        query = f"?point={lat},{lon}&key={API_KEY}"
        response = requests.get(url + query, verify=False)
        if response.status_code == 200:
            traffic_data = response.json()
            print("Traffic data fetched successfully!")

            return traffic_data
        else:
            print(f"Error fetching traffic data: {response.status_code}")
            print(response.text)  # Print error detail
    except Exception as e:
        print(f"Error querying point ({lat}, {lon}: {e}")


def bulk_insert_into_road_Table(road_list):
    print("bulk_insert_into_road_Table called")
    try:
        cur = conn.cursor()
        query = """
                   INSERT INTO roads_traffic.roads (road_name, road_type, centroid_lat, centroid_lon)
                   VALUES %s
                   RETURNING road_id;  
               """
        values = [(road["name"], road["type"], road["centroid_lat"], road["centroid_lon"]) for road in road_list]
        print(values)
        extras.execute_values(cur, query, values)  # Use extras.execute_values
        inserted_ids = cur.fetchall()  # Fetch all returned IDs
        road_id = [row[0] for row in inserted_ids][0]
        print(f"road_id: {road_id}")
        conn.commit()

        print(f"✅ Inserted {len(road_list)} roads into database.")

        return road_id

    except Exception as e:
        print(f"Error in {e}")
        conn.rollback()
        return None


def bulk_insert_into_traffic_Data_Table(traffic_data_list):
    try:
        cur = conn.cursor()
        # SQL Query for batch insert
        query = f"""
              INSERT INTO roads_traffic.traffic_data 
              (road_id, current_speed, free_flow_speed, current_travel_time, free_flow_travel_time) 
              VALUES %s
              """
        values = [(data["road_id"], data["current_speed"], data["free_flow_speed"], data["current_travel_time"],
                   data["free_flow_travel_time"])
                  for data in traffic_data_list]
        extras.execute_values(cur, query, values)  # Use extras.execute_values
        conn.commit()
        print(f"✅ Inserted {len(traffic_data_list)} roads into database.")

    except Exception as e:
        print(f"Error in {e}")


def main():
    traffic_data, north, east, west, south = get_osm_data(28.610210438038912, 77.45215918231175, 100)
    processed_roads = process_road_data(traffic_data)

    print("\nNearby Roads:")

    # Filter logic
    relevant_road_types = ["secondary", "tertiary", "primary"]  # Types to keep
    filtered_data = [
        road for road in processed_roads
        if road['type'] in relevant_road_types and "Unknown" not in road['name']
    ]

    merged_roads = merge_road_segments(filtered_data)

    # for bulk insertt:
    road_list = []
    traffic_data_list = []

    for i, road in enumerate(merged_roads):
        print(f"{i + 1}. {road['name']} ({road['type']})")
        selected_road = merged_roads[i]
        node_coordinates = get_node_coordinates(selected_road["nodes"])

        # Optional: Calculate the centroid of the road
        latitudes = [lat for lat, lon in node_coordinates.values()]
        longitudes = [lon for lat, lon in node_coordinates.values()]
        centroid_lat = sum(latitudes) / len(latitudes)
        centroid_lon = sum(longitudes) / len(longitudes)

        road_list.append({
            "name": road['name'],
            "type": road['type'],
            "centroid_lat": centroid_lat,
            "centroid_lon": centroid_lon
        })

        road_id = bulk_insert_into_road_Table(road_list)
        road_list.clear()

        traffic_data = tomotom_Api(centroid_lat, centroid_lon)
        print(traffic_data)

        current_speed = traffic_data["flowSegmentData"].get("currentSpeed", "Unknown")
        free_flow_speed = traffic_data["flowSegmentData"].get("freeFlowSpeed", "Unknown")
        road_closure = traffic_data["flowSegmentData"].get("roadClosure", False)
        current_travel_time = traffic_data["flowSegmentData"].get("currentTravelTime", "Unknown")
        free_flow_travel_time = traffic_data["flowSegmentData"].get("freeFlowTravelTime", "Unknown")
        roadClosure = traffic_data["flowSegmentData"].get("roadClosure", "Unknown")
        print(current_speed)
        print(free_flow_speed)
        print(current_travel_time)
        print(free_flow_travel_time)
        print(roadClosure)

        traffic_data_list.append({
            "road_id": road_id,
            "current_speed": current_speed,
            "free_flow_speed": free_flow_speed,
            "current_travel_time": current_travel_time,
            "free_flow_travel_time": free_flow_travel_time,
            "roadClosure":roadClosure
        })

        print(f"\nCentroid of the road: Latitude: {centroid_lat}, Longitude: {centroid_lon}")

        print(f"https://www.google.com/maps?q={centroid_lat},{centroid_lon}")
        bulk_insert_into_traffic_Data_Table(traffic_data_list)
        traffic_data_list.clear()

        map = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=15)
        folium.Marker([centroid_lat, centroid_lon], tooltip="Selected Road").add_to(map)
        map.save("road_map.html")
        exit()


if __name__ == "__main__":
    main()
