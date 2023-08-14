### GLOBAL VARIABLES ###

# Change the variables below to your liking
# For more info, see https://petstore.swagger.io/?url=https://www.wegweiser-kommune.de/openapi#/default/get_rest_map_data__friendlyUrl_
bbox = "5.866,47.270,15.042,55.099"  # bounding box (left, bottom, right, top) for Germany, in EPSG:4326
layer = "COMMUNE" # the level of the returned geometries. Available values: COMMUNE, DISTRICT, STATE
outline = "BUND" # the type of parent municipalities of the currently selected municipalities. Available values: BUND, BUNDESLAND, LANDKREIS
save_path = "data/regions_wwk.geojson" # select save path of GeoJSON file


### CODE ###

import os
import requests
import geopandas as gpd

url = "https://www.wegweiser-kommune.de/data-api/rest/map/data/demografische-entwicklung+geburten+guetersloh-gt+2019+karte"

params = {
    "bbox": bbox,
    "layer": layer,
    "outline": outline,
}

headers = {"accept": "application/json"}

response = requests.get(url, params=params, headers=headers)

# ensure we got a successful response
if response.status_code == 200:
    data = response.json()  # parse JSON response into a Python dictionary

    # Convert the JSON response to a GeoPandas DataFrame
    gdf = gpd.GeoDataFrame.from_features(data["regions"]["features"])

    # Convert any fields with list data types to strings, else errors will occur when saving to file
    for col in gdf.columns:
        if gdf[col].dtype == "object" and isinstance(gdf[col][0], list):
            gdf[col] = gdf[col].apply(lambda x: str(x))

    # Check if data directory exists - if not, create it
    if not os.path.exists("data/"):
        os.makedirs("data/")

    # Save the GeoDataFrame to a file
    gdf.to_file(save_path, driver="GeoJSON")

    print(f"File saved successfully to path {save_path}")

else:
    print(f"Request failed with status {response.status_code}")