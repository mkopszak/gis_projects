from PyQt4.QtGui import QInputDialog

def docstring():
	"""QGIS script
	
	This script imports OSM-based data equipped with Digital Elevation Model data 
	supplied in the setup_gis_tables script to qgis with appropriate labels, 
	marking altitude in each OSM node. 
	Database connection parametera are obtained in the run-time 
	(password can (and should) be skipped if using .pgpass file).."""
	
help(docstring)

uri = QgsDataSourceURI()

host, rest = QInputDialog.getText(None, " ", "insert host")
port, rest = QInputDialog.getText(None, " ", "insert port")
db_name, rest = QInputDialog.getText(None, " ", "insert db_name")
user, rest = QInputDialog.getText(None, " ", "insert user")
label_size, rest = QInputDialog.getText(None, " ", "insert size of labels")


uri.setConnection(host, port, db_name, user, "")

uri.setDataSource("public", "osm_nmt_altitude", "geom", "")
vl_alt = QgsVectorLayer(uri.uri(), "osm_nmt_altitude", "postgres")
if not vl_alt.isValid():
    print "vector layer not valid"
    
my_renderer = vl_alt.rendererV2()
my_renderer.symbol().setSize(1)
vl_alt.triggerRepaint()

label = QgsPalLayerSettings()
label.readFromLayer(vl_alt)
label.enabled = True
label.fieldName = "h"
label.placement= QgsPalLayerSettings.AroundPoint
label.setDataDefinedProperty(QgsPalLayerSettings.Size,True,True,label_size,"")
label.writeToLayer(vl_alt)

QgsMapLayerRegistry.instance().addMapLayers([vl_alt])

uri.setDataSource("public", "planet_osm_point", "way", "")
vl_point = QgsVectorLayer(uri.uri(), "planet_osm_point", "postgres")
if not vl_point.isValid():
    print "vector layer not valid"
QgsMapLayerRegistry.instance().addMapLayers([vl_point])

uri.setDataSource("public", "planet_osm_polygon", "way", "")
vl_polygon = QgsVectorLayer(uri.uri(), "planet_osm_polygon", "postgres")
if not vl_polygon.isValid():
    print "vector layer not valid"
QgsMapLayerRegistry.instance().addMapLayers([vl_polygon])

uri.setDataSource("public", "planet_osm_line", "way", "")
vl_line = QgsVectorLayer(uri.uri(), "planet_osm_line", "postgres")
if not vl_line.isValid():
    print "vector layer not valid"
QgsMapLayerRegistry.instance().addMapLayers([vl_line]) 


