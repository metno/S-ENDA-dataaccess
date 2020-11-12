# S-ENDA-dataaccess
Scripts, setup, config, docs related to data access services for the S-ENDA project.

# S3 and Zarr format data access service

* Download Arome Arctic from thredds.met.no: https://thredds.met.no/thredds/catalog/aromearcticlatest/catalog.html?dataset=aromearcticlatest/arome_arctic_vc_2_5km_latest.nc
* Setup jupyter environment.
* Start local S3 service
* Run jupyter notebook for reformatting netcdf to zarr and upload to a local S3 service.
* Plot one variable from arome arctic by streaming that variable from S3.

## Setup jupyter environment.
* Install python version 3.7 or newer. 
* Install jupyter:  pip3 install --user jupyterlab
* Setup virtualenv: python3.7 -m venv --without-pip venv_dataaccess
* Install all dependencies into virtualenv: pip3 install -r requirements.txt
* Add virtualenv as a kernel for jupyter: 
* Start jupyter-lab.


## Start local S3 service.
* `docker run --rm -p 9000:9000 -v <local_data_path>:/data -e "MINIO_ACCESS_KEY=test" -e "MINIO_SECRET_KEY=<password>" minio/minio server /data`
* Check out the content of the S3 storage at : `http://localhost:9000`
