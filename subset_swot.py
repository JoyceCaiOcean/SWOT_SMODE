import numpy as np
import xarray as xr
import datetime
import os
import pandas as pd

def convert_string_to_npdatetime(string):
    datetime_obj = pd.to_datetime(string, format="%Y%m%dT%H%M%S", errors='coerce', yearfirst=True, utc=True)
    return np.datetime64(datetime_obj)

def find_swot_start_end(data_dir, file_prefix = 'SWOT_L3_LR_SSH_Basic_XXX_YYY_'):
    files = os.listdir(data_dir)
    
    start_dates = [convert_string_to_npdatetime(f[len(file_prefix):len(file_prefix)+15]) for f in files]
    
    end_dates = [convert_string_to_npdatetime(f[len(file_prefix)+16:len(file_prefix)+16+15]) for f in files]
    
    return start_dates, end_dates

def subset_swot(lon_min, lon_max, lat_min, lat_max, window_start_date, window_end_date, start_dates, end_dates, files, ssh_name = 'ssha', data_dir = './21day_orbit'):
    
    lolabox = [lon_min,lon_max,lat_min,lat_max]
    
    window_start = np.datetime64(pd.to_datetime(str(window_start_date).replace('-','')+'T000000', format="%Y%m%dT%H%M%S", errors='coerce', yearfirst=True, utc=True))
    window_end = np.datetime64(pd.to_datetime(str(window_end_date).replace('-','')+'T000000', format="%Y%m%dT%H%M%S", errors='coerce', yearfirst=True, utc=True))
    
    files_load = []
    for i, f in enumerate(files):
        if end_dates[i]>window_start and start_dates[i]<window_end:
            files_load.append(f)
        elif start_dates[i]>window_start and start_dates[i]<window_end:
            files_load.append(f)
        elif end_dates[i]>window_start and end_dates[i]<window_end:
            files_load.append(f)


    paths_load = [data_dir +'/' + f for f in files_load]
    paths_load = sorted(paths_load)
    
    lon = []
    lat = []
    ssh = []

    for p in paths_load:
        with xr.open_dataset(p) as ds: 
            # create mask for subsetting
            time_mask = (ds.time >= window_start) & (ds.time <= window_end)
            lon_mask = (ds.longitude > lolabox[0]) & (ds.longitude < lolabox[1])
            lat_mask = (ds.latitude > lolabox[2]) & (ds.latitude < lolabox[3])

            # Combine masks and extract data 
            mask = lon_mask & lat_mask & time_mask
            if mask.any():  # Check if any data is within the box
                lon.append(ds.longitude.values[mask].ravel())
                lat.append(ds.latitude.values[mask].ravel())
                ssh.append(ds[ssh_name].values[mask].ravel())

    if len(lon)>0:
        longitude = np.concatenate(lon)
        latitude = np.concatenate(lat)
        ssha = np.concatenate(ssh)
        
    return longitude, latitude, ssha


swot_dir = './21day_orbit'
ssh_name = 'ssha'

window_start_date = datetime.date(2023,9,10)
window_end_date = datetime.date(2023,9,20)

lon_min = 150
lon_max = 160
lat_min = 20
lat_max = 30

files = os.listdir(swot_dir)

start_dates, end_dates = find_swot_start_end(swot_dir, file_prefix = 'SWOT_L3_LR_SSH_Basic_XXX_YYY_')

# note some NaN values for SSH might be present due to e.g. rain
lon, lat, ssh = subset_swot(lon_min, lon_max, lat_min, lat_max, window_start_date, window_end_date, start_dates, end_dates, files, ssh_name, swot_dir)