# OSM-indicators

## About

This repository provides scripts to calculate indicators based on OpenStreetMap (OSM) data for German territorial divisions (municipalities/*Gemeinden*, districts/*Landkreise* and states/*Bundesländer*). For example, it allows one to calculate how many pharmacies each municipality in Germany has, based on OSM data.

This work is part of Bertelsmann Stiftung's [Wegweiser Kommune](https://www.wegweiser-kommune.de/) project. The Wegweiser Kommune is a platform that provides data on German municipalities, districts and states.
- Please note that as of August 2023, the Wegweiser Kommune API only provides data for municipalities (*Gemeinden*) with 5000 or more inhabitants.

Authors: Nina Hauser ([@ninahauserberlin](https://github.com/ninahauserberlin)), Tim Fangmeyer ([@tifa365](https://github.com/tifa365)), Gabriel da Silva Zech ([@GabZech](https://github.com/GabZech)).


## Installation

The scripts are written in Python 3.11.

To automatically create a virtual environment and install all dependencies, we recommend using [pipenv](https://pipenv.pypa.io/en/latest/).
- To do so, simply run `pipenv install` in the root directory of this repository.
- If you face any dependency issues, use `pipenv sync` instead - this will install the exact versions of the dependencies specified in the `Pipfile.lock`.

Alternatively, you can install the dependencies manually via `pip install -r requirements.txt`.

## Usage

All scripts are found under the folder `src`. To edit those, minimal Python knowledge is required. You simply need to change the variable names found at the the top of each script under the "GLOBAL VARIABLES" section before running them.

Description of each script:

[download_osm_data.py](src/download_osm_data.py): Downloads all OSM data for a given tag and region.
- *For example, using `tags = {"amenity": "pharmacy"}` and `query = Germany` will download the OSM data for all pharmacies in Germany and save this to the file `data/osm_data.csv`.*

[download_regions_data.py](src/download_regions_data.py): Downloads all (geospatial) data for regions of a given type (municipalities, districts or states) from the Wegweiser Kommune API. For help with the API variables, see [here](https://petstore.swagger.io/?url=https://www.wegweiser-kommune.de/openapi#/default/get_rest_map_data__friendlyUrl_).
- *For example, using `layer = "COMMUNE"` and the bbox values for Germany will download the geospatial data for every municipality (Gemeinde/Kommune) in Germany and save this to the file `data/regions_wwk.geojson`*.

[create_index.py](src/create_index.py): Complements the file downloaded from the Wegweiser Kommune with a column containing the number of OSM places for each of the regions - and saves the results to a CSV file under the folder `output`.
- *For example, it will add a column `osm_count` to the original dataframe downloaded after running the `download_regions_data.py` script with the number of OSM pharmacies found for each municipality and save this to the file `output/regions_with_index.csv`*.

[visualise_index.ipynb](src/visualise_index.ipynb): Visualises the results of the file created by the `create_index.py` script on a map.