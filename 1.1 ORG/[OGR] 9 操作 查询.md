# 条件查询
## 属性查询
```python
from osgeo import ogr
import os
shpfile = r'C:\tmp\data.shp'
ds = ogr.Open(shpfile)
layer = ds.GetLayer(0) #得到图层
lyr_count = layer.GetFeatureCount()
print(lyr_count) #原先的要素总数
layer.SetAttributeFilter("AREA > 800000") #属性查询条件
lyr_count = layer.GetFeatureCount() #查询过后，layer被更新
print(lyr_count) #满足条件的layer
# 将该layer保存成shp
driver = ogr.GetDriverByName("ESRI Shapefile")
extfile = r'C:\tmp\data.shp'
if os.access( extfile, os.F_OK ):
	driver.DeleteDataSource( extfile )
newds = driver.CreateDataSource(extfile)
layernew = newds.CreateLayer('rect',None,ogr.wkbPolygon)
# 遍历，复制
feat = layer.GetNextFeature()
while feat is not None:
	layernew.CreateFeature(feat)
	feat = layer.GetNextFeature()
newds.Destroy()
```

## 空间查询

## SQL查询
```python
from osgeo import ogr
driver = ogr.GetDriverByName("ESRI Shapefile")
world_shp = r'C:\tmp\test.shp'
world_ds = ogr.Open(world_shp)
world_layer = world_ds.GetLayer()
world_layer_name = world_layer.GetName()
result = world_ds.ExecuteSQL("select * from %s where prov_id = '22' order by BNDRY_ID desc" % (world_layer_name)) # ) # ExecuteSQL是基于数据集进行的，而不是图层
resultFeat = result.GetNextFeature ()
out_shp = r'C:\tmp\test\test_sql_result.shp'
create_shp_by_layer(out_shp, result) #保存结果
# 对查询结果进行遍历
while resultFeat :
    print resultFeat.GetField('BNDRY_ID')
    resultFeat = result.GetNextFeature ()
#执行下一条SQL语句之前一定要先释放
world_ds.ReleaseResultSet(result) 
```