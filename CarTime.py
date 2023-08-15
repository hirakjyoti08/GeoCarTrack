import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon,Point
import glob
from datetime import datetime, date
from dateutil.parser import parse
import os
import re


def divide_map_into_rectangles(place_name, num_rows, num_columns):
    graph = ox.graph_from_place(place_name, network_type="all")
    roma_area = ox.geocode_to_gdf(place_name) 
    roma_polygon = roma_area['geometry'].iloc[0]

    xmin, ymin, xmax, ymax = roma_polygon.bounds
    width = xmax - xmin
    height = ymax - ymin

    rectangles = []
    for i in range(num_rows):
        y = ymin + i * (height / num_rows)
        for j in range(num_columns):
            x = xmin + j * (width / num_columns)
            # Ensure the correct order of vertices (clockwise)
            rectangle = Polygon([(x, y), (x + (width / num_columns), y),
                     (x + (width / num_columns), y + (height / num_rows)), (x, y + (height / num_rows))])
            rectangles.append(rectangle)

    return graph, rectangles

def search_cars_in_rectangle(rectangle, date_input, time_slot, car_dataset_path, rectangle_id_input):
    time_slot_start, time_slot_end = time_slot.split("-")
    time_slot_start_dt = datetime.combine(date_input, parse(time_slot_start).time())
    time_slot_end_dt = datetime.combine(date_input, parse(time_slot_end).time())

    cars_found = []
    files = glob.glob(os.path.join(car_dataset_path, "*.txt"))
    for file_path in files:
        with open(file_path, "r") as file:
            for line in file:
                car_num, date_time_str, coordinates_str = line.strip().split(";")
                date_str, time_str = date_time_str.split(" ")
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                time_obj = parse(time_str).time()
                date_time_obj = datetime.combine(date_obj, time_obj)
                formatted_date_time_obj = date_time_obj.strftime("%Y-%m-%d %H:%M:%S")
                dt_obj = datetime.strptime(formatted_date_time_obj, "%Y-%m-%d %H:%M:%S")
                #for coordinates
                matches = re.findall(r'-?\d+\.\d+', coordinates_str)
                longitude = float(matches[1])
                latitude = float(matches[0])
                coordinates = Point(longitude, latitude)
                
                if time_slot_start_dt <= dt_obj <= time_slot_end_dt:
                    if coordinates.within(rectangle):
                    #     print(f"abc: {coordinates}")
                         
                        cars_found.append(car_num)

    return cars_found       


place_name = "Rome, Italy"
num_rows = 12 #18
num_columns =5 #7
car_dataset_path = "D:\VS code\internship\Car Dataset"  

graph, rectangles = divide_map_into_rectangles(place_name, num_rows, num_columns)
gdf = gpd.GeoDataFrame({'ID': range(1, len(rectangles) + 1), 'geometry': rectangles})

fig, ax = ox.plot_graph(graph, show=False, close=False, figsize=(12.44, 18))
gdf.plot(ax=ax, color='none', edgecolor='red', linewidth=0.5)

for idx, row in gdf.iterrows():
    ax.text(row.geometry.centroid.x, row.geometry.centroid.y, str(row['ID']), fontsize=6, ha='center', va='center', color='red')

time_slot_input = "14:00:00-23:00:00"
date_input = date(2014, 2, 1)
rectangle_id_input = 27


selected_rectangle_idx = rectangle_id_input - 1  

selected_rectangle = rectangles[selected_rectangle_idx]


gdf_selected = gpd.GeoDataFrame({'ID': [rectangle_id_input], 'geometry': [selected_rectangle]})
gdf_selected.plot(ax=ax, color='none', edgecolor='blue', linewidth=2)

cars_found = search_cars_in_rectangle(selected_rectangle, date_input, time_slot_input, car_dataset_path, rectangle_id_input)
cars = set(cars_found)

if not cars:
    print("no cars found")
else:
    car_ids = ", ".join(cars)
    print(f"Number of cars found at that specific time and rectangle : {len(cars)} and the car id's are : {car_ids}")

plt.show()