import geopandas as gpd
from shapely.geometry import Point

# paths
wd = r""
berlin_gpkg = f"{wd}/3_rollout_berlin/Bezirke_EW_Zahlen.gpkg"

# Load the berlin districts
berlin = gpd.read_file(berlin_gpkg)
# reproject to EPSG:32633
berlin = berlin.to_crs("EPSG:32633")
berlin_union = berlin.unary_union


# Create a point geodataframe over berlin_union with points every 96 meters
points = []
for i in range(int(berlin_union.bounds[0]), int(berlin_union.bounds[2]), 96):
    for j in range(int(berlin_union.bounds[1]), int(berlin_union.bounds[3]), 96):
        points.append(Point(i, j))

berlin_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:32633")
# Clip the points to the berlin districts
berlin_points = gpd.clip(berlin_points, berlin)

# Intersect the points with berlin and append the cols Gemeinde_n and Gemeinde_s to the points
berlin_points_join = gpd.sjoin(berlin_points, berlin[["Gemeinde_n", "Gemeinde_s", "geometry"]], how="inner", op="intersects")
berlin_points_join.to_file(f"{wd}/Data/Berlin/berlin_points.gpkg", driver="GPKG")
