from collections import defaultdict
from Database_connection import connect_Database
import psycopg2
from psycopg2 import extras
import logging
import requests
import folium

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from logging_and_monitoring.centralized_logging import setup_logger

db_logger = setup_logger("database_logging", "road_Data_script", "postgres", "logs/database_logs.log")
road_data_main_logger = setup_logger("road_data_logging", "road_data_main", "python", "logs/road_data_main.log")
get_nearby_roads_logger = setup_logger("road_data_logging", "get_nearby_roads_with_coordinates()",
                                                        "python", "logs/road_data_func_get_nearby_roads.log")


# step 1 get all road data from lat,lon,radius and calc bounding box points

def get_nearby_roads_with_coordinates(lat, lng, radius=500):
    """Find nearby roads with names and their start & end coordinates."""
    get_nearby_roads_logger.info(f"function started lat={lat}, lng={lng}, radius={radius}",
                                                  extra={"stage": "start"})

    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    way(around:{radius}, {lat}, {lng}) ["highway"];
    (._;>;);
    out body;
    """
    try:
        response = requests.get(overpass_url, params={"data": query})
        get_nearby_roads_logger.info(f"Request sent to Overpass API", extra={"stage": "processing"})

        if response.status_code == 200:
            get_nearby_roads_logger.info(f"Response received successfully",
                                                          extra={"stage": "processing"})

            data = response.json()
            if "elements" in data:
                get_nearby_roads_logger.info(f"Processing received data...",
                                                              extra={"stage": "processing"})

                ways = [el for el in data["elements"] if el["type"] == "way"]
                nodes = {el["id"]: el for el in data["elements"] if el["type"] == "node"}
                road_details = {}

                get_nearby_roads_logger.info("Found %d roads in response data", len(ways),
                                                              extra={"stage": "processing"})

                for way in ways:
                    if "tags" in way:
                        name = way["tags"].get("name")  # Road name
                        ref = way["tags"].get("ref")  # Highway number (if no name)
                        if not name and ref:
                            name = f"Highway {ref}"  # Use reference if no name
                        if name and "nodes" in way:
                            node_ids = way["nodes"]
                            start_node = nodes.get(node_ids[0])  # First node
                            end_node = nodes.get(node_ids[-1])  # Last node

                            if start_node and end_node:
                                start_coords = (start_node["lat"], start_node["lon"])
                                end_coords = (end_node["lat"], end_node["lon"])

                                # Merge roads with the same name
                                if name in road_details:
                                    # Update start point if it's earlier (smaller lat, lon)
                                    road_details[name]["start"] = min(
                                        road_details[name]["start"], start_coords
                                    )
                                    # Update end point if it's later (bigger lat, lon)
                                    road_details[name]["end"] = max(
                                        road_details[name]["end"], end_coords
                                    )
                                else:
                                    road_details[name] = {"start": start_coords, "end": end_coords}

                                get_nearby_roads_logger.info("Road: %s | Start: %s | End: %s",
                                                                              name, start_coords, end_coords,
                                                                              extra={"stage": "processing"})
                if road_details:
                    get_nearby_roads_logger.info(" Processed %d roads", len(road_details),
                                                                  extra={"stage": "processing"})
                    return road_details
                else:
                    get_nearby_roads_logger.warning(" No named roads found",
                                                                     extra={"stage": "warning"})
                    return {"No named roads found."}
            else:
                get_nearby_roads_logger.warning(" No roads found in response",
                                                                 extra={"stage": "warning"})
                return {"No roads found."}
        else:
            get_nearby_roads_logger.error(
                f"Failed API Request! Status Code: {response.status_code}, Response: {response.text}",
                extra={"stage": "error"})
            return {"error": f"API request failed with status {response.status_code}"}
    except Exception as e:
        get_nearby_roads_logger.critical(f"Exception occurred: {e}", exc_info=True,
                                                          extra={"stage": "critical"})


def bulk_insert_into_road_Table(road_list, conn):
    db_logger.info("bulk_insert_into_road_Table function called", extra={"stage": "start"})
    db_logger.info("Preparing road data for bulk insertion", extra={"stage": "processing"})

    try:
        cur = conn.cursor()
        # db_logger.debug("Cursor created successfully", extra={"stage": "processing"})

        query = """
                   INSERT INTO roads_traffic.roads (road_name, start_lat,start_lon,end_lat,end_lon)
                   VALUES %s
                   RETURNING road_id;  
               """
        values = [(road["name"], road["start_lat"], road["start_lon"], road["end_lat"], road["end_lon"]) for road in
                  road_list]
        db_logger.info(f"query: {query} ,values: {values} ", extra={"stage": "start"})

        extras.execute_values(cur, query, values)  # Use extras.execute_values
        inserted_ids = cur.fetchall()  # Fetch all returned IDs
        road_id = [row[0] for row in inserted_ids] if inserted_ids else []
        conn.commit()
        db_logger.info(f"Inserted {len(road_list)} roads into database ,Returning road_id :{road_id}",
                       extra={"stage": "processing"})
        return road_id

    except Exception as e:
        db_logger.critical(f"exception in bulk_insert_into_road_Table() : {e}", extra={"stage": "processing"})
        conn.rollback()
        return None

def main():

    db_logger.info(f"connect_Database() begins", extra={"stage": "start"})


    try:
        conn = connect_Database()

        if conn is None:
            db_logger.critical("connect_Database() Connection failed: No connection established",
                               extra={"stage": "start"})
            exit()

        db_logger.info(f"connect_Database() completed", extra={"stage": "success"})

        # Example coordinates (replace with real input)

        road_data_main_logger.info(f"road_data Main Started", extra={"stage": "start"})

        LAT, LNG = 28.60507059568563, 77.44698311030206
        road_data_main_logger.info(f"Lat : {LAT}, LNG: {LNG}", extra={"stage": "processing"})

        # Get nearby roads with start and end coordinates
        road_data_main_logger.info("Calling get_nearby_roads_with_coordinates()", extra={"stage": "processing"})
        user_input = input("Do you want to run 'get_nearby_roads_with_coordinates'? (yes/no): ").strip().lower()
        if user_input in ["yes", "y"]:

              nearby_roads = get_nearby_roads_with_coordinates(LAT, LNG)

        road_data_main_logger.info(f"Received {len(nearby_roads)} roads", extra={"stage": "processing"})

        road_data_main_logger.info(f"get_nearby_roads_with_coordinates func completed.", extra={"stage": "processing"})



        if nearby_roads:
            road_list = []
            # Print results
            road_data_main_logger.info(f"Nearby Roads with Start & End Points:", extra={"stage": "processing"})
            for road_name, coords in nearby_roads.items():
                # logging.info(f"Road_name: {road_name}, Start_coords : {coords['start']} , End_coords : {coords['end']}")

                road_list.append({
                    "name": road_name,
                    "start_lat": coords['start'][0],
                    "start_lon": coords['start'][1],
                    "end_lat": coords['end'][0],
                    "end_lon": coords['end'][1],
                })

            road_data_main_logger.info(f"Nearby Roads with Start & End Points:,Road_list : {road_list}", extra={"stage": "processing"})

            road_data_main_logger.info(f"Starting bulk_insert_into_road_Table()", extra={"stage": "processing"})
            user_input = input("Do you want to run 'bulk_insert_into_road_Table'? (yes/no): ").strip().lower()
            if user_input in ["yes", "y"]:

                bulk_insert_into_road_Table(road_list, conn)
            road_data_main_logger.info(f"completed bulk_insert_into_road_Table()", extra={"stage": "success"})

            # map = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=15)
            # folium.Marker([centroid_lat, centroid_lon], tooltip="Selected Road").add_to(map)
            # map.save(f"{road['name']}_road_map.html")
        else:
            road_data_main_logger.error(f"nearby_roads is empty", extra={"stage": "error"})
    except Exception as e:
            road_data_main_logger.error(f"exception in main: {e}", extra={"stage": "error"})
    finally:
        if conn:
            db_logger.info("Database connection closed", extra={"stage": "success"})


if __name__ == "__main__":
    main()
