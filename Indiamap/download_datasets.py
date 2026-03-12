"""
download_datasets.py
Downloads high-accuracy Natural Earth datasets for country borders and state/province borders.

Resolution: 10m (high resolution)
Outputs: 
- datasets/ne_10m_admin_0_countries.geojson
- datasets/ne_10m_admin_1_states.geojson
"""

import os
import geopandas as gpd
import requests
import zipfile
import io

DATASETS = [
    {
        "name": "Admin-0 Countries",
        "url": "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip",
        "extract_dir": "datasets/ne_dataset",
        "output_path": "datasets/ne_10m_admin_0_countries.geojson"
    },
    {
        "name": "Admin-1 States/Provinces",
        "url": "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_1_states_provinces.zip",
        "extract_dir": "datasets/states_dataset",
        "output_path": "datasets/ne_10m_admin_1_states.geojson"
    }
]

def download_and_process_dataset(dataset):
    os.makedirs("datasets", exist_ok=True)
    
    print(f"Downloading {dataset['name']} dataset...")
    r = requests.get(dataset["url"], timeout=60)
    r.raise_for_status()
    
    print(f"Download complete. Extracting {dataset['name']}...")
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        z.extractall(dataset["extract_dir"])
        
    shp_path = None
    for f in os.listdir(dataset["extract_dir"]):
        if f.endswith(".shp"):
            shp_path = os.path.join(dataset["extract_dir"], f)
            break
            
    if shp_path is None:
        raise RuntimeError(f"Shapefile not found after extraction for {dataset['name']}")
        
    print(f"Reading shapefile with GeoPandas for {dataset['name']}...")
    gdf = gpd.read_file(shp_path)
    print(f"Total features for {dataset['name']}: {len(gdf)}")
    
    print(f"Saving GeoJSON for {dataset['name']}...")
    gdf.to_file(dataset["output_path"], driver="GeoJSON")
    print(f"Saved: {dataset['output_path']}\n")

def main():
    for dataset in DATASETS:
        download_and_process_dataset(dataset)

if __name__ == "__main__":
    main()