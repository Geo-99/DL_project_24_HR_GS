import os
import geopandas as gpd
import pandas as pd

os.getcwd()

# Tiles
part_1 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_upto12000/tiles_autosave.gpkg")
# Add original_id col to part_1 and put the id in it
part_1["original_id"] = part_1.index + 1
part_2 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_12000_21000/tiles_autosave.gpkg")
part_3 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_21000_31000/tiles_autosave.gpkg")
part_4 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_31000_37000/tiles_autosave.gpkg")
part_5 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_37000_46000/tiles_autosave.gpkg")
part_6 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_46000_50000/tiles_autosave.gpkg")
part_7 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_50000_55000_H/tiles_50001_55000.gpkg")
part_8 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_55000_61000_H/tiles_55001_61001.gpkg")
part_9 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_61000_63000/tiles_autosave.gpkg")
part_10 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_63000_69000/tiles_autosave.gpkg")
part_11 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_69000_70000/tiles_autosave.gpkg")
part_12 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_70000_80000/tiles_autosave.gpkg")
part_13 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_80000_85000/tiles_autosave.gpkg")
part_14 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_85000_93000/tiles_autosave.gpkg")
part_15 = gpd.read_file(f"{os.getcwd()}/Data/Berlin/rollout_colab_93000_end/tiles.gpkg")


# Create a merged geodataframe with the same columns as the parts
merged = gpd.GeoDataFrame(columns=part_1.columns)

# Create a list of the parts
parts = [part_1, part_2, part_3, part_4, part_5, part_6, part_7, part_8, part_9, part_10, part_11, part_12, part_13, part_14, part_15]

# Iterate over the parts and append them to the merged geodataframe
for part in parts:
    # Check if there are rows that have the same original_id
    if len(merged[merged["original_id"].isin(part["original_id"])]) > 0:
        # Print the rows of the part and merged that have the same original_id
        part_duplicates = part[part["original_id"].isin(merged["original_id"])]
        merged_duplicates = merged[merged["original_id"].isin(part["original_id"])]
        print("Duplicates in current part:", part_duplicates[["original_id", "constr_conf"]], "\n")
        print("Duplicates in merged dataframe:", merged_duplicates[["original_id", "constr_conf"]], "\n")

        # Different conf values for some tiles that H calculated?!

        # Ask user if the duplicates in the part should be removed
        remove_duplicates = input("Do you want to remove the duplicates in the current part? (y/n): ")
        # If the user wants to remove the duplicates, remove them
        if remove_duplicates == "y":
            part = part[~part["original_id"].isin(merged["original_id"])]
            print("Duplicates removed from the current part.")
        else:
            print("Duplicates not removed from the current part.")
    # Append the part to the merged geodataframe
    merged = pd.concat([merged, part], ignore_index=True)

# Create a df of the rows that have the same geometry
duplicates = merged[merged.duplicated(subset="geometry", keep=False)]

# Drop the duplicates and reset the index
merged = merged.drop_duplicates(subset="geometry").reset_index(drop=True)

# Define the original_id as integer
merged["original_id"] = merged["original_id"].astype(int)

# Read the points file
points = gpd.read_file(f"{os.getcwd()}/Data/Berlin/berlin_points_4.gpkg")
# Drop the index_right column
points = points.drop(columns=["index_right"])
# Create a new column called index_tiles and put the current index +1 in it
points["index_tiles"] = points.index + 1
# Add the constr and constr_conf columns to the points by merging via original_id in merged and index_tiles in points
points = points.merge(merged[["original_id", "constr", "constr_conf"]], left_on="index_tiles", right_on="original_id", how="left")
# Drop the index_tiles col
points = points.drop(columns=["index_tiles"])

# Save both gdfs
merged.to_file(f"{os.getcwd()}/Data/Berlin/MERGED_110924/merged_tiles.gpkg", driver="GPKG")
points.to_file(f"{os.getcwd()}/Data/Berlin/MERGED_110924/merged_points.gpkg", driver="GPKG")
