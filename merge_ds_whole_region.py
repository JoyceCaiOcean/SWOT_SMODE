####### the code aims to merge the daily l4 data to ONE datafile with only smode region

import os
import xarray as xr


# the path of the folder
data_path = '/Users/Joyce Cai/calval/'
# Get the list of files in the directory with full paths
file_paths = [os.path.join(data_path, file) for file in os.listdir(data_path)]


# file_paths = ['/Users/Joyce Cai/calval/dt_global_allsat_phy_l4_20230421_20240501.nc','/Users/Joyce Cai/calval/dt_global_allsat_phy_l4_20230422_20240501.nc']

# Open multiple files and concatenate along the time dimension
dataset = xr.open_mfdataset(file_paths, concat_dim='time', combine='nested', parallel=True)

# Load the dataset into memory (optional, depending on your workflow)
dataset.load()

# Now, 'dataset' contains the combined data along the time dimension
print(dataset)

## save the whole dataset as a new nc file
# Define the output file path
output_file = '/Users/Joyce Cai/calval/merged_dataset_l4_20230328_20230711.nc'

# Save the merged dataset to a new NetCDF file
dataset.to_netcdf(output_file)

# Optionally, close the dataset
dataset.close()



#### if only data within the s-mode region
# Define the latitude and longitude range
lat_min, lat_max = 33, 38.5  # Replace with your actual latitude range
lon_min, lon_max = -127+360, -122+360  # Replace with your actual longitude range

# Load the dataset (replace 'your_dataset.nc' with your actual NetCDF file)
ds = dataset

# Slice the data in the specified region
ds_region = ds.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

# Define the output file path
output_file = '/Users/Joyce Cai/calval/merged_dataset_smode_region_l4_20230328_20230711.nc'

# Save the merged dataset to a new NetCDF file
ds_region.to_netcdf(output_file)

# Optionally, close the dataset
ds_region.close()