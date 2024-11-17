import geopandas as gpd
import os
from owslib.wms import WebMapService
import random


# wd
wd = r""

# save foder
save_folder = r""

# Read the point gpkg where the cranes are located (see Drive folder)
#crane_gpkg = gpd.read_file(f"{wd}/DRIVE_FOLDER/0_data_preprocessing_GPKGs/1_obb_attempt_gpkg/Cranes_OBB.gpkg")
#crane_gpkg = gpd.read_file(f"{wd}DRIVE_FOLDER//0_data_preprocessing_GPKGs/2_cls_gpkgs/Constructions_without_cranes_Bavaria.gpkg")
crane_gpkg = gpd.read_file(f"{wd}/DRIVE_FOLDER/0_data_preprocessing_GPKGs/2_cls_gpkgs/Cranes_CLS_Bavaria.gpkg")
#crane_gpkg = gpd.read_file(f"{wd}/DRIVE_FOLDER/0_data_preprocessing_GPKGs/2_cls_gpkgs/Cranes_CLS_Stuttgart.gpkg")
#crane_gpkg = gpd.read_file(f"{wd}/DRIVE_FOLDER/0_data_preprocessing_GPKGs/2_cls_gpkgs/RandomPoints_Bavaria_Top10cities.gpkg")


#crane_gpkg = crane_gpkg.to_crs("EPSG:32632")

# png boxes
boxes = []

# size of the box in meters
box_size = 96

# Source CRS & Target CRS
source_crs = "EPSG:32632"
target_crs = "EPSG:4326"

# Iterate over the points and create boxes around them with the point in the center and the box size
for i in range(len(crane_gpkg)):

    # creating a random number between 20 and -20 to shift the centroids randomnly so that the construction/crane is not always in the center
    random_number_x = random.randint(-20, 20)
    random_number_y = random.randint(-20, 20)

    point = crane_gpkg.iloc[i].geometry
    x, y = point.x, point.y
    # randomnly shift the centroids
    x = x + random_number_x
    y = y + random_number_y
    x_min, y_min, x_max, y_max = x - box_size/2, y - box_size/2, x + box_size/2, y + box_size/2
    # Create 4 points for the box
    points = gpd.points_from_xy([x_min, x_max, x_max, x_min], [y_max, y_max, y_min, y_min], crs=source_crs)

    # Points in new CRS
    points_new = points.to_crs(target_crs)

    # Get the new x_min, y_min, x_max, y_max
    x_min_new, y_min_new, x_max_new, y_max_new = points_new.x[0], points_new.y[3], points_new.x[2], points_new.y[1]

    boxes.append([x_min_new, y_min_new, x_max_new, y_max_new])

# WMS server URL
wms_url = "https://geoservices.bayern.de/od/wms/dop/v1/dop20"
#wms_url = "https://owsproxy.lgl-bw.de/owsproxy/ows/WMS_LGL-BW_ATKIS_DOP_20_C?"

# Connect to the WMS service
wms = WebMapService(wms_url)

# Define layer name
layer_name = "by_dop20c"
#layer_name = "IMAGES_DOP_20_RGB"

# Define output image size
output_size = (box_size / 0.2, box_size / 0.2)
# as integer
output_size = (int(output_size[0]), int(output_size[1]))

# Define the output image format
output_format = "image/png"

# Iterate over boxes and download the images
for i in range(len(boxes)):
    # Print current progress
    print(f"Downloading image {i+1}/{len(boxes)}")

    globals()[f'map_request_{i}'] = wms.getmap(
        layers=[layer_name],
        srs=target_crs,
        bbox=boxes[i],
        size=output_size,
        format=output_format
    )

    # Save the image
    with open(os.path.join(wd, save_folder, f"/crane_Bav_{i}.png"), 'wb') as out:
        out.write(globals()[f'map_request_{i}'].read())
