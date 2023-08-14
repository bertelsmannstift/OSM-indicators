### GLOBAL VARIABLES ###

# Change the variables below to your liking
index_column = "count_osm" # name of the column containing the count of OSM places per gemeinde
gemeinden_data = "data/regions_wwk.geojson" # path to GeoJSON file containing gemeinden data from Wegweiser Kommune
osm_data = "data/osm_data.csv" # path to csv file containing geocoded OSM data
save_path = "output/regions_with_index.csv" # select save path of csv file


### CODE ###

import os
import pandas as pd
import geopandas as gpd

# read in the osm and gemeinden files
gemeinden = gpd.read_file(gemeinden_data)
osm = pd.read_csv(osm_data)

# convert the osm geometry column to a GeoSeries and read it as a GeoDataFrame
osm["geometry"] = gpd.GeoSeries.from_wkt(osm["geometry"].astype(str))
osm = gpd.GeoDataFrame(osm, crs='EPSG:4326', geometry='geometry')

# perform a spatial join between the osm and gemeinden GeoDataFrames
joined = gpd.sjoin(osm, gemeinden, predicate="within")

# get the count of places in each gemeinde
osm_per_gemeinde_count = joined.groupby("gkz")["index_right"].count()

# merge the count back into the gemeinden GeoDataFrame
df_out = gemeinden.merge(
    osm_per_gemeinde_count, on="gkz", how="left"
)

# rename the column
df_out.rename(columns={"index_right": index_column}, inplace=True)

# if a gemeinde has no OSM places, fill the count with 0
df_out[index_column] = df_out[index_column].fillna(0)

# Check if output directory exists - if not, create it
if not os.path.exists("output/"):
    os.makedirs("output/")

# save the GeoDataFrame to a file
df_out.to_csv(save_path, index=False)