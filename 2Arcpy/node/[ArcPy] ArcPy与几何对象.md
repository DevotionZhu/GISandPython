ESRI JSON或GeoJSON转换为ArcPy几何对象：  
arcpy.AsShape(geojson_struct,{esri_json} )

	import arcpy
	esri_json = {
	    "paths" : [
	        [
				[-97.08, 32.8], [-97.05, 32.6], [-97.06, 32.7],[-97.07, 32.6]
			], [
				[-97.4, 32.5], [-97.2, 32.75]
			]
		], "spatialReference" : {
			"wkid" : 4326
		}
	}
	# Set the second parameter to True to use an esri JSON
	polyline = arcpy.AsShape(esri_json, True)
