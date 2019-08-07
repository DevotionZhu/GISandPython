1) 判断map中是否有该key  

        key in map.keys() #map里有key，返回ture
        map.has_key(key) #有，返回true
        #理论上 第一种快
        
2) Python与json
   
        import json
        data = {"span" : "foo", "parrot" : 42}
        jsonStr = json.dumps(data) # map-->JSON
        json.loads(jsonStr) # JSON-->map
        
3) ArcPy创建可中断的线(两条线联合成一条线存储) 不行，创建线时只能传一个数组

        
4) ArcPy保存几何对象

        arcpy.CopyFeatures_management(对象, "路径")
        
5) 获取目录下所有文件名
        
       import os
       def file_name(file_dir):
            for root,dirs,files in os.walk(file_dir):
                print root #当前目录路径
                print dirs #当前路径下所有子目录
                print files #当前路径下所有非目录子文件

6) 拆分字符串得 文件名、扩展名

        def GetFileNameAndExt(dir):
            import os
            (filepath,tmpfilename) = os.path.split(dir)
            (filename,extension) = os.path.splitext(tmpfilename)
            return filename,extension
            
7) 延时

        time.sleep(2)
        
8) ESRI JSON或GeoJSON转换为ArcPy几何对象  
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
