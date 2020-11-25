import os
from datetime import datetime

import xarray
import s3fs

ds = xarray.open_dataset(
    "https://thredds.met.no/thredds/dodsC/aromearcticlatest/arome_arctic_pp_2_5km_latest.nc",
    decode_times=False,
)

# Get reference time from dataset
ref_time_epoch = ds["forecast_reference_time"].values.cumsum()[0]
ref_time = datetime.fromtimestamp(ref_time_epoch)

# Drop variables that have 0 dimensions, as upload fails when trying to upload them.
ds = ds.drop_vars("forecast_reference_time")
ds = ds.drop_vars("projection_lambert")

# Get environment variables
S3_HOST = os.getenv('S3_PATH', 'http://localhost:9000') 
S3_KEY = os.getenv('S3_KEY', 'test')
S3_SECRET = os.environ.get('S3_SECRET', 'testtesttest1')

# Initilize the S3 file system
s3_path = 's3://aromearctic/' + ref_time.strftime("%Y%m%dT%H00Z") 
s3 = s3fs.S3FileSystem(client_kwargs={"endpoint_url": S3_HOST},key=S3_KEY, secret=S3_SECRET)
store = s3fs.S3Map(root=s3_path, s3=s3, check=False)

# Save to zarr
begin_time = datetime.now()
print(datetime.now())

ds.to_zarr(store=store, consolidated=True)

print(datetime.datetime.now() - begin_time)

