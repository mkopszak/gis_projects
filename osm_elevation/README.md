# About the project
The aim of the project is to connect data from [OSM](https://www.openstreetmap.org) and point cloud containing
altitudes from a specific DEM (Digital Elevation Model) data, since in OSM one doesn't have information aboul object
elevation by default (in fact, it is quite rare). 
OSM-based data is represented in postGIS database. The method can be used with any object that consists of OSM nodes (points, lines, polygons).

# Requirements
- Python3
- QGIS
- PostrgreSQL database with extensions hstore and postgis enabled
- OSM data loaded to PostgreSQL database with osm2psql
- .pgpass with password to database is suggested
- appropriate DEM data stored in csv file:

format (separator - space): <br />
X Y h <br />
for example 568900.00 295200.00 272.66

You can use data from CODGiK: [DEM](http://www.codgik.gov.pl/index.php/darmowe-dane/nmt-100.html) <br />
info about CODGIK file: <br />
srid = 2180 <br />
mesh distance = 100 m

# Directory contents
- sample.osm - small sample of OSM data, a few trails in Tatras
- setup_gis_tables.py - setup to connect data from OSM and altitudes data
- qgis_import_layer.py - visualises altitudes in QGIS

# Step-by-step execution
1. Load data from OSM file to database:
osm2pgsql sample.osm -c -d dbname -U username -H host -P port  --hstore --slim -W

	It shall produce the following schema [osm2pgsql-schema](https://wiki.openstreetmap.org/wiki/Osm2pgsql/schema),
	which is discused further [here](http://www.volkerschatz.com/net/osm/osm2pgsql-db.html)

2. In Python3 run setup_gis_tables.py 

3. In QGIS (Python Editor) run qgis_import_layer.py

# QGIS screenshot
![QGIS visualisation](https://lh6.googleusercontent.com/X8MS9nlskOmpQQ0AwPnB_ixfZfr1Lz9iYEGiaJEQwMvhI25FKkKNmX228A-CHZZT9nlS0EZu7-EogwGsbE3GGEpu6aViBA=w1280-h622)

