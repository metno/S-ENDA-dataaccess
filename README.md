# S-ENDA-dataaccess
Scripts, setup, config, docs related to data access services for the S-ENDA project.

# S3 and Zarr format data access service

* Download Arome Arctic from thredds.met.no: https://thredds.met.no/thredds/catalog/aromearcticlatest/catalog.html?dataset=aromearcticlatest/arome_arctic_vc_2_5km_latest.nc
* Setup jupyter environment.
* Run jupyter notebook for reformatting netcdf to zarr and upload to a local S3 service.
* Plot one variable from arome arctic by streaming that variable from S3.
