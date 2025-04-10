from collections import defaultdict
from Database_connection import connect_Database
import psycopg2
from psycopg2 import extras
import random
import requests
from geopy.distance import geodesic

from logging_and_monitoring.centralized_logging import setup_logger

TOMTOM_API_KEY = "EQEuzLbnAf2rBfIu244A8ds4A3sPD6BK"

db_logger = setup_logger("database_logging", "traffic_Data_script", "posgres", "logs/database_logs.log")
traffic_data_main_logger = setup_logger("traffic_data_script", "traffic_data_main", "python", "logs/database_logs.log")
functions_Com = setup_logger("traffic_data_script", "get_route()", "python", "logs/database_logs.log")


#step 1 get all road data from lat,lon,radius and calc bounding box points


# # Function to get node details (coordinates) from Overpass API
# def make_api_requests(url,params,logger,stage,max_retries=3):
#     """Generic function to handle API requests with retries."""
#     for attempt in range(max_retries):
#         try:
#             response = requests.get(url, params=params, verify=False,timeout=10)
#             response.raise_for_status()  # Raise an HTTP error if occurs
#             return response.json()  # Return data if successful
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Attempt {attempt + 1}: API request failed: {e}", extra={"stage": stage})
#             if attempt == max_retries - 1:
#                 return None

def tomtom_api(lat, lon):
    API_KEY = "EQEuzLbnAf2rBfIu244A8ds4A3sPD6BK"
    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

    try:
        # Add a small random offset to avoid cached responses
        lat += random.uniform(-0.0005, 0.0005)
        lon += random.uniform(-0.0005, 0.0005)

        # Use a params dictionary for cleaner URL building
        params = {
            "point": f"{lat},{lon}",
            "key": API_KEY,
            "realTime": "true"
        }
        response = requests.get(url, params=params, verify=False)
        functions_Com.info(f"Calling TomTom API for route: {url},parameter:{params}", extra={"stage": "tomtom_api"})

        if response.status_code == 200:
            functions_Com.info(f"Response: {response.status_code},result:{response.json()}", extra={"stage": "tomtom_api"})
            return response.json()  # Return traffic data directly
        functions_Com.error(f"Error fetching traffic data: {response.status_code} - {response.text}", extra={"stage": "tomtom_api"})

    except requests.RequestException as e:
        functions_Com.critical(f"Network error fetching traffic data: {e}", extra={"stage": "tomtom_api"})
        print(f"Network error fetching traffic data: {e}")
    except Exception as e:
        functions_Com.critical(f"Unexpected error querying point ({lat}, {lon}): {e}", extra={"stage": "tomtom_api"})
    return None  # Return None if an error occurs

def bulk_insert_into_traffic_Data_Table(traffic_data_list,conn):
    db_logger.info("bulk_insert_into_road_Table function called", extra={"stage": "start"})

    if not traffic_data_list:
        db_logger.warning("No data provided for insertion in traffic_data_list", extra={"stage": "start"})
        return
    query = f"""
                 INSERT INTO roads_traffic.traffic_data 
                 (road_id,road_name,latitude,longitude ,current_speed, free_flow_speed, 
                 current_travel_time, free_flow_travel_time,mapurl,weather_conditions,
                 temperature,humidity,traffic_condition) 
                 VALUES %s
           """

    try:
        values = [(data["road_id"], data["road_name"], data["latitude"], data["longitude"], data["current_speed"], data["free_flow_speed"],
                   data["current_travel_time"],
                   data["free_flow_travel_time"], data['mapurl'], data['weather_conditions'], data['temperature'], data['humidity'],
                   data['traffic_condition'])
                  for data in traffic_data_list]
        db_logger.info(f"Preparing to insert {len(values)} records into database.", extra={"stage": "execution"})
        with conn.cursor() as cur:  # Automatically closes cursor after execution
            extras.execute_values(cur, query, values)
            conn.commit()
        db_logger.info(f"Successfully inserted {len(values)} / {len(traffic_data_list)}records into database.", extra={"stage": "success"})

    except psycopg2.Error as db_err:
        db_logger.exception(f"Database error during bulk insert :{db_err}", extra={"stage": "error"})
        conn.rollback()  # Rollback on error
    except Exception as e:
        db_logger.exception(f"Unexpected error: {e}", extra={"stage": "error"})
        conn.rollback()  # Rollback on error


def get_road_id(conn):
    functions_Com.info(f"get_road_id() begins", extra={"stage": "get_road_id"})
    query = f"SELECT road_id ,start_lat,start_lon,end_lat,end_lon,road_name FROM roads_traffic.roads"
    functions_Com.info(f"getting road id from query - {query}", extra={"stage": "get_road_id"})

    try:
        with conn.cursor() as cur:
                cur.execute(query)
                road_data = cur.fetchall()
        if road_data:
            functions_Com.info(f"road_Data - {road_data}", extra={"stage": "get_road_id"})
            return road_data
        else:
            functions_Com.error(f"Empty result from query - {road_data}", extra={"stage": "get_road_id"})
            return None

    except Exception as e:
        functions_Com.critical(f"error fetching road id : {e}", extra={"stage": "get_road_id"})
        return None


def get_weather_data(lat, lon):
    API_KEY = "951ff261d9454ad189355359252002"
    url = "http://api.weatherapi.com/v1/current.json"

    functions_Com.info("get_weather_data() begins", extra={"stage": "get_weather_data"})

    try:
        params = {
            "key": API_KEY,
            "q": f"{lat},{lon}"
        }

        response = requests.get(url, params=params,timeout=10)
        response.raise_for_status()  # Raise an error for bad HTTP responses (4xx, 5xx)

        data = response.json()
        current = data.get("current", {})

        # Extract weather data safely
        weather_conditions = current.get("condition", {}).get("text", "Unknown")
        temperature = float(current.get("temp_c", 0.0))
        humidity = float(current.get("humidity", 0.0))

        functions_Com.info(f"Weather data fetched successfully ,weather_condition:{weather_conditions},temperature:{temperature},humidity:{humidity}", extra={"stage": "get_weather_data"})

        return weather_conditions, temperature, humidity

    except requests.exceptions.RequestException as e:
        functions_Com.error(f"Network error: {e}", extra={"stage": "get_weather_data"})
    except (ValueError, KeyError) as e:
        functions_Com.error(f"Data parsing error: {e}", extra={"stage": "get_weather_data"})

    return None, None, None  # Return None values on failure


def get_route(start_lat, start_lon, end_lat, end_lon):
    try:
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_lat},{start_lon}:{end_lat},{end_lon}/json?key={TOMTOM_API_KEY}"
        functions_Com.info(f"Calling TomTom API for route: {url}", extra={"stage": "get_route"})

        response = requests.get(url, verify=False, timeout=10)  # Added timeout for reliability
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        data = response.json()
        # Check if "routes" key exists and has data
        if not data.get("routes"):
            functions_Com.warning(f"No route found for coordinates ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})",
                                  extra={"stage": "get_route"})
            return None, None
        route_legs = data["routes"][0].get("legs", [])
        if not route_legs:
            functions_Com.warning(f"Route legs missing for ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})",
                                  extra={"stage": "get_route"})
            return None, None

        points = route_legs[0].get("points", [])
        route_length = route_legs[0].get("summary", {}).get("lengthInMeters", 0)  # Get total route length

        functions_Com.info(f"Successfully retrieved route. Length: {route_length} meters",
                           extra={"stage": "get_route"})
        functions_Com.info(f"Successfully retrieved route. points: {points}",
                           extra={"stage": "get_route"})
        return points, route_length

    except requests.exceptions.Timeout:
        functions_Com.error(f"Request timed out for route ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})",
                            exc_info=True, extra={"stage": "get_route"})
    except requests.exceptions.ConnectionError:
        functions_Com.error(f"Network connection error for route ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})",
                            exc_info=True, extra={"stage": "get_route"})
    except requests.exceptions.HTTPError as http_err:
        functions_Com.error(f"HTTP error: {http_err} for route ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})",
                            exc_info=True, extra={"stage": "get_route"})
    except requests.exceptions.RequestException as req_err:
        functions_Com.error(f"Unexpected request error: {req_err} for route ({start_lat}, {start_lon}) -> ({end_lat}, {end_lon})",
                            exc_info=True, extra={"stage": "get_route"})
    except Exception as e:
        functions_Com.critical(f"Unexpected error in get_route: {e}", exc_info=True, extra={"stage": "get_route"})

    return None, None  # Return None in case of any failure


def filter_significant_points(points, interval):
    """Filters points that have a significant change in distance."""
    functions_Com.info(f"filter_significant_points() begins with {len(points)} points", extra={"stage": "filter_significant_points"})
    if not points:
        functions_Com.warning("No points provided, returning empty list.", extra={"stage": "filter_significant_points"})
        return []
    filtered_points = [points[0]]  # Always include the first point
    prev_point = points[0]
    count_filtered = 1  # Start with the first point included


    for point in points[1:]:
        distance = geodesic(
            (prev_point["latitude"], prev_point["longitude"]),
            (point["latitude"], point["longitude"])
        ).meters

        if distance >= interval:
            filtered_points.append(point)
            prev_point = point
            count_filtered += 1  # Increment count for logging
    functions_Com.info(
        f"Filtered {count_filtered} significant points from {len(points)} total",
        extra={"stage": "filter_significant_points"}
    )
    functions_Com.info(
        f"Filtered points ; {filtered_points}", extra={"stage": "filter_significant_points"}
    )

    return filtered_points


def main():
    db_logger.info(f"connect_Database() begins", extra={"stage": "start"})
    conn = connect_Database()
    if conn is None:
        db_logger.critical("connect_Database() Connection failed: No connection established",
                               extra={"stage": "start"})
        exit()

        db_logger.info(f"connect_Database() completed", extra={"stage": "success"})
    traffic_data_main_logger.info(f"get_road_id() calling", extra={"stage": "start"})
    road_Data = get_road_id(conn)
    if not road_Data:
        traffic_data_main_logger.warning("No roads found in get_road_id(), exiting main()", extra={"stage": "start"})
        return
    traffic_data_main_logger.info(f"get_road_id() completed", extra={"stage": "start"})

    traffic_data_list = []
    traffic_data_main_logger.info(f"Loop Over road_data begins ", extra={"stage": "loop_roadData"})

    for i, road in enumerate(road_Data):
        try:
            road_id, start_lat, start_lon, end_lat, end_lon, road_name = road[0], road[1], road[2], road[3], road[4], road[5]
            traffic_data_main_logger.info(f"Processing road: {road_name} (ID: {road_id})", extra={"stage": "loop_roadData"})

            traffic_data_main_logger.info(f"get_route() calling with {start_lon},{start_lon},{end_lon}", extra={"stage": "loop_roadData"})

            intermediate_points, route_length = get_route(start_lat, start_lon, end_lat, end_lon)
            traffic_data_main_logger.info(f"get_route() completed", extra={"stage": "loop_roadData"})

            if not intermediate_points:
                traffic_data_main_logger.warning(f"No intermediate points found for road: {road_name} (ID: {road_id})",
                                                 extra={"stage": "loop_roadData"})
                continue  # Skip this road if no route found

            interval = max(250, min(route_length / 10, 2000))  # Adaptive interval

            traffic_data_main_logger.info(f"filter_significant_points() calling with {intermediate_points},{interval}",
                                          extra={"stage": "loop_roadData"})
            filtered_points = filter_significant_points(intermediate_points, interval)
            traffic_data_main_logger.info(f"filter_significant_points() completed", extra={"stage": "loop_roadData"})

            # Get weather data only once (for the first point in the list)
            if not filtered_points:
                traffic_data_main_logger.warning(f"No significant points found in filtered points for road: {road_name} (ID: {road_id})",
                                                 extra={"stage": "loop_roadData"})
                continue  # Skip if no valid points

            first_point = filtered_points[0]
            for attempt in range(3):

                try:
                    traffic_data_main_logger.info(f"get_weather_data() calling {attempt} with {first_point['latitude']},{first_point['longitude']}",
                                                  extra={"stage": "loop_roadData"})

                    weather_conditions, temperature, humidity = get_weather_data(first_point['latitude'],
                                                                                 first_point['longitude'])
                    if weather_conditions is not None:  # Stop retrying if successful
                              break
                except Exception as e:
                    traffic_data_main_logger.error(f"Attempt {attempt + 1}: Failed to fetch weather data: {e}", exc_info=True,
                                                   extra={"stage": "loop_roadData"})
                    if attempt == 2:  # Last attempt
                        weather_conditions, temperature, humidity = "Unknown", "Unknown", "Unknown"

            print(f"📍 Intermediate Coordinates Along the Road (Interval: {interval}m):")
            traffic_data_main_logger.info(
                f"filtered_point processing",
                extra={"stage": "loop_roadData_filtered_point"})

            for point in filtered_points:
                try:
                    traffic_data_main_logger.info(f"tomotom_Api() calling with ({point['latitude']}{point['longitude']})",
                                                  extra={"stage": "loop_roadData_filtered_point"})
                    traffic_data = tomtom_api(point['latitude'], point['longitude'])
                    traffic_data_main_logger.info(f"tomotom_Api() completed ", extra={"stage": "loop_roadData_filtered_point"})

                    # Extract values safely, with default fallbacks
                    current_speed = traffic_data.get("flowSegmentData", {}).get("currentSpeed", "Unknown")
                    free_flow_speed = traffic_data.get("flowSegmentData", {}).get("freeFlowSpeed", "Unknown")

                    traffic_condition = ("Free Flow" if current_speed >= free_flow_speed
                                         else "Moderate" if current_speed >= 0.5 * free_flow_speed
                    else "Heavy" if current_speed >= 0.3 * free_flow_speed
                    else "Severe")

                    current_travel_time = traffic_data.get("flowSegmentData", {}).get("currentTravelTime", "Unknown")
                    free_flow_travel_time = traffic_data.get("flowSegmentData", {}).get("freeFlowTravelTime", "Unknown")
                    road_closure = traffic_data.get("flowSegmentData", {}).get("roadClosure", "Unknown")

                    print(f"Traffic data for {road_name}: Speed {current_speed}, Free Flow {free_flow_speed}")

                    traffic_data_list.append({
                        "road_id": road_id,
                        "road_name": road_name,
                        "latitude": point['latitude'],
                        "longitude": point['longitude'],
                        "current_speed": current_speed,
                        "free_flow_speed": free_flow_speed,
                        "current_travel_time": current_travel_time,
                        "free_flow_travel_time": free_flow_travel_time,
                        "roadClosure": road_closure,
                        "mapurl": f"https://www.google.com/maps?q={point['latitude']},{point['longitude']}",
                        "weather_conditions": weather_conditions,
                        "temperature": temperature,
                        "humidity": humidity,
                        "traffic_condition": traffic_condition
                    })
                    traffic_data_main_logger.info(f"traffic_data_list:{traffic_data_list} ", extra={"stage": "loop_roadData_filtered_point"})

                except KeyError as ke:
                    traffic_data_main_logger.error(f"Missing expected traffic data key: {ke}", exc_info=True,
                                                   extra={"stage": "loop_roadData_filtered_point"})
                except Exception as e:
                    traffic_data_main_logger.error(f"Unexpected error while processing traffic data: {e}",
                                                   exc_info=True, extra={"stage": "loop_roadData_filtered_point"})
                    # print(f" - {point['latitude']}, {point['longitude']}")
                    # print(f"https://www.google.com/maps?q={point['latitude']},{point['longitude']}")
            if traffic_data_list:
                try:
                    traffic_data_main_logger.info(f"bulk_insert_into_traffic_Data_Table() calling with : {traffic_data_list}",
                                                  extra={"stage": "loop_roadData_filtered_point"})
                    bulk_insert_into_traffic_Data_Table(traffic_data_list,conn)
                    traffic_data_main_logger.info(f"bulk_insert_into_traffic_Data_Table() completed",
                                                  extra={"stage": "loop_roadData_filtered_point"})

                except Exception as e:
                    traffic_data_main_logger.critical(f"Failed to insert traffic data: {e}", exc_info=True,
                                                      extra={"stage": "loop_roadData_filtered_point"})

                traffic_data_list.clear()  # Clear list after insertion

        except ValueError as ve:
            traffic_data_main_logger.error(f"Data unpacking error for road {road}: {ve}", exc_info=True, extra={"stage": "loop_roadData"})
        except Exception as e:
            traffic_data_main_logger.critical(f"Unexpected error in road processing: {e}", exc_info=True, extra={"stage": "loop_roadData"})
            # map = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=15)
            # folium.Marker([centroid_lat, centroid_lon], tooltip="Selected Road").add_to(map)
            # map.save("road_map.html")
            # exit()
        traffic_data_main_logger.info(f"Loop Over road_data completed", extra={"stage": "loop_roadData"})
    traffic_data_main_logger.info(f"main() completed", extra={"stage": "start"})


if __name__ == "__main__":
    main()
