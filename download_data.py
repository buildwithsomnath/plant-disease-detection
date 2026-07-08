import kagglehub
import shutil
import os

print("Downloading PlantVillage dataset...")

path = kagglehub.dataset_download("emmarex/plantdisease") #or paste your kaggle dataset location

print(f"Downloaded to: {path}")

destination = "data/plant_disease_data"

if os.path.exists(destination):
    shutil.rmtree(destination)

shutil.copytree(path, destination)

print("Dataset copied to ./dataset")