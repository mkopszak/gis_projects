from PyQt4.QtGui import QInputDialog
def docstring():
	"""Import table with altitude labels to QGIS."""
	
help(docstring)

uri = QgsDataSourceURI()

host, rest = QInputDialog.getText(None, " ", "insert host")
port, rest = QInputDialog.getText(None, " ", "insert port")
db_name, rest = QInputDialog.getText(None, " ", "insert db_name")
user, rest = QInputDialog.getText(None, " ", "insert user")
label_size, rest = QInputDialog.getText(None, " ", "insert size of label")


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

uri.setDataSource("public", "osm_line", "geom", "")
vl_osm_line = QgsVectorLayer(uri.uri(), "osm_line", "postgres")
if not vl_osm_line.isValid():
    print "vector layer not valid"
    
QgsMapLayerRegistry.instance().addMapLayers([vl_osm_line])


