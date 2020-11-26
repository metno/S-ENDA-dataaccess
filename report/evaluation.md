# Evaluation of data access services
The focus of the evaulation has been on data access for streaming raw datasets, and two candidates have been evaulauted: OPeNDAP and Zarr via object stores.

Evaluated against these criterias: https://s-enda-documentation.readthedocs.io/en/latest/architecture.html#s-enda-data-access-service-c4-diagrams


The functional criterias that both systems cover equally well will not be mentioned. So criterias omitted  can be assumed to be covered.

## Criteria: Data Producers should be able to produce a dataset and upload results to the data access service without time-consuming transformations

The fastest solution for the producer will probably be the existing solution of writing netcdf file to lustre. Transformation to zarr format is pretty fast, but does require some cpu and time.

If its feasible to produce datasets directly in the zarr format, the transformation cost will disappear. However, using S3 as a storage backend will probably be noticeably slower than lustre.  

So produce on lustre, either zarr or netcdf, and upload to S3 seems more realistic. 

## Criteria: The dataset needs to be on a widely adopted open data format standard
Both DAP and Zarr have a very similar structure, based on the CDM data model and similar to NetCDF file format.

DAP is an older protocol, but how wide has the adoption been and how much support has the protocol today?

Zarr is new, but has a lot of traction, across many scientific disciplines, and will also possibly be adopted as an OGC standard.

## Criteria: The data access service must work together with an event-driven production system
DAP, at least Thredds, works by creating an index from polling the file system. So data access to a dataset through events can not be directly solved, as the event will typically arrive long before the dataset is actually available.

With Zarr/S3, you push data the object store and a successfull reply means the dataset is available. An event can then either be created after the push or by attaching an event system to the object store bucket.


## Criteria: The data access service will work well with the current trends of technology in scientific computing.
The assumption beeing that the meteorological institutions are now moving fast towards a cloud style infrastructure, co-existing with HPC-style infrastructure for running the NWP models and some of the post-processing.

Using cloud-native commodity service like object store with S3 protocol will make it trivial to get up and running with distribution of project results. The project need not maintain any service for data access nor do any special configuration of the distribution service, but can trust that every cloud system, private or public, will have an object store available.

OpenDAP requires mounting a distributed file-system and running a specialized data access service, either centrally or by each project itself. Requiring more maintenance and tighter coupling between access service and production, but also enable more control and customization for special needs.


## Criteria Maintainbility: 
Zarr format uses commodity services like object stores. OpenDAP solutions are a specialized solution with limited community.

Object store scaling for peta-byte of multi-dimensional data has not been tried. Object stores are known to scale well, with relatively easy replication, with no query mechanisms outside reading/writing of blobs of data. So it should scale well, but it remains to be seen.

Also, currently MET has no experience with running large, scalable object stores.

If self-hosted solutions are too costly, it should be straight-forward to move to a cloud provider. However, moving large amounts of data will take time, and there will be a signifcant cost attached to distribution of massive amounts of data from public cloud solutions.

Many cloud providers have non-profit/open-data programs however, and we could also possible host data with EWC.

OpenDAP solution is harder to move to a public cloud solution, but still possible, but it will require a signifcant time for initial setup and for continuous maintainence.

Speculation: It might be easier to maintain data production and data distribution when they can be scaled and maintained separately, since the traffic pattern for production and distribution are so different.

## Performance criterias: 
Slight win for object stores, but with a performant DAP solution like Dars, the storage solution behind the data access service will be the bottleneck.

In terms of pure throughput, probably the best solution would be lustre native on top of Dars.

# Benchmark-ish

## Transform netcdf file and upload of zarr

### From laptop to S3 infra test service
```
CPU times: user 1min 15s, sys: 8.46 s, total: 1min 24s
Wall time: 11min 58s
```

### From laptop to local S3 minio service
```
CPU times: user 1min, sys: 3.8 s, total: 1min 3s
Wall time: 1min 44s
```

## Stream in arome arctic dataset and save as netcdf-file.

### From laptop Dars to laptop netcdf file
```
CPU times: user 40.5 s, sys: 6.76 s, total: 47.3 s
Wall time: 1min 4s
```

### From laptop Minio/Zarr to laptop netcdf file
```
CPU times: user 39 s, sys: 5.49 s, total: 44.5 s
Wall time: 57.5 s
```

# Recommendations
In the near future, 1-3 years, we will definately need DAP and HTTP download. At the same time, the meteorology community is fast adopting cloud technology. So we should start now adapting data access to best cater to distribution in a cloud environment.

At the core of cloud technology are containers, object stores and event-driven architectures. 

Recommendation: Support existing distribution thredds via nfs/cifs mounted lustre, while developing cloud-based distribution using MET and EWC S3 compatible object stores.

Main pros: Fits future technology trends, loose coupling of data production and data distribution service, standardized solutions for scaling and replication across data regions.

Main cons: Data duplication, at least in the near future.

## Data access patterns using S3/Zarr

### Immutable dataset
Upload to Zarr/S3, update metadata service. Dataset available for download and streaming from S3.

### Access latest version of dataset
Poll metadataservice for latest version and/or listen on new dataset events. Use the metadata information to access the relevant S3 bucket.

### Continous timeseries dataset
The continious timerseries becomes a separate dataset. So, first upload the model run dataset, then append to the continous dataset.

### Mapping dataset with OGC standards
Server-side rendering of dataset by reading Zarr/S3, targeting the new OGC protocols: OGC API - Maps and/or OGC API - Tiles.

## Write netcdf file and dist via thredds.met.no

## Write zarr to lustre and dist S3/Zarr and DAP via Object store and OpenDAP server mounting lustre cifs

## Write netcdf to lustre and upload to S3/Zarr

## Write directly to S3/Zarr