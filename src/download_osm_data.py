### GLOBAL VARIABLES ###

# Change the variables below to your liking
tags = {"amenity": "pharmacy"}  # select tag, for all available tags see https://wiki.openstreetmap.org/wiki/Map_features
query = "Germany"  # select region to filter by, for more info see https://osmnx.readthedocs.io/en/stable/user-reference.html#osmnx.features.features_from_place
save_path = "data/osm_data.csv"  # select save path of csv file


### CODE ###

import os
import osmnx as ox

# Download pharmacies from OSM
df = ox.features.features_from_place(query=query, tags=tags)
df.reset_index(drop=True, inplace=True)

# Convert columns to string data type to avoid errors when saving to GeoJSON
string_columns = [col for col in df.columns if col != "geometry"]
df[string_columns] = df[string_columns].astype(str)

# Check if data directory exists - if not, create it
if not os.path.exists("data/"):
    os.makedirs("data/")

# Save data to csv
df.to_csv(save_path, index=False)
