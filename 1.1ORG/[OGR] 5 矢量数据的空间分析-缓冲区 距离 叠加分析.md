# 叠加分析

## 验证几何对象之间关系的操作种类
1. 相交（Intersects）：两个要素之间是否有公共区域
2. 接触（Touches）：查看两个几何对象是否在边缘处接触，但实际上并不共享任何区域
3. 包含（Containes）或内部（Within）：查看一个几何对象是否完全位于另一个对象内
4. 穿过：
5. 重叠：
6. 不相交：

## 基于现有的空间关系来创建新的几何对象
1. 相交（Intersection：A∩B）：可获得一个新的几何对象，用于表示另外两个对象中共同的区域
2. 联合（Union：A∪B）：将两个现有的几何对象的区域合并成一个
	- 如果输入的几何对象类型不同，就会返回一个几何对象集
	- 可以把几何对象集当成复合几何对象，只不过每一部分并不需要是同一种几何对象类型
3. 差集（difference：A-B）：从一个几何对象上剪出相交的部分，余下部分与第二个几何对象不再相交
4. 对称差集（SymDifference：(A-B)∪(B-A) ）：返回移除了交集后的联合结果

## 例子
### 相交Intersection——单独要素相交
```python
from osgeo import ogr

# 获得Geometry
water_ds = ogr.Open(2001) #打开一个水体（包含湖泊、河流、运河、沼泽等）数据
water_lyr = water_ds.GetLayer(0) #得到图层
water_lyr.SetAttributeFilter('WaterbdyID = 1011327') # 按属性选择
marsh_feat = water_lyr.GetNextFeature() #上一句之后，获得筛选后的第一个要素
marsh_geom = marsh_feat.geometry().Clone() #拷贝这个geometry

# 获得另一个Geometry
nola_ds = ogr.Open(2001)
nola_lyr = nola_ds.GetLayer(0)
nola_feat = nola_lyr.GetNextFeature()
nola_geom = nola_feat.geometry.Clone()

# 两个多边形【相交操作】
intersection = marsh_geom.Intersection(nola_geom)

# 【显示查看结果】
from ospybook.vectorplotter import VectorPlotter
vp = VectorPlotter(False) #非交互模式创建
vp.plot(intersection, 'yellow', hatch='x')
vp.draw() #调用draw函数绘制

# 【计算结果的总面积】
water_lyr.SetAttirbuteFilter("Feature !='Lake'") #【属性过滤】将湖泊数据排除 
water_lyr.SetSpatialFilter(nola_geom) #【空间过滤条件】将所有不在nola_geom内的要素过滤掉
wetlands_area = 0	# 计算面积
for feat in water_lyr: #遍历要素
	intersect = feat.geometry.Intersection(nola_geom) #剩下的feat数据与nola_geom边界相交
	wetland_area += intersect.GetArea() #获得Geom的面积

pcnt = wetlands_area / nola_geom.GetArea()
```

### 相交Intersection——两个图层相交
```python
# 属性过滤在图层中得到目标要素
water_lyr.SetAttributeFilter("Feature !='Lake'")

# 在内存中创建一个临时图层
memory_driver = ogr.GetDriverByName('Memory')
tmp_ds = memory_driver.CreateDataSource('tmp')
tmp_lyr = tmp_ds.CreateLayer('tmp')

# 将图层相交，并将结果存储在临时图层tmp_lyr内
nola_lyr.Intersection(water_lyr, tmp_lyr)

# 计算面积
sql = 'SELECT SUM(OGR_GEOM_AREA) AS area FROM tmp'
lyr = tmp_ds.ExecuteSQL(sql)
```

# 邻近分析
【OGR邻近分析工具】
1. 用来量测几何要素间的距离
2. 创建缓冲区

## 缓冲区
> 方法一有漏洞，建议使用方法二


【例子】美国有多少城市位于火山1600米的范围之内

【方法一】有问题的方法，后面会对比
1. 没有针对整个图层的缓冲功能，所以需要单独缓冲每个点，并把他们添加到一个临时层中
2. 第一步完成后，就可以将缓冲区图层与城市图层相交

```python
from osgeo import ogr

shp_ds = ogr.Open(2001)
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

# 创建一个临时图层，用于存储缓冲区域
memory_driver = ogr.GetDriverByName('memory')
memory_ds = memory_driver.CreateDataSource('temp')
buff_lyr = memory_ds.CreateLayer('buffer')
buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())

# 缓冲每一个火山点，将结果添加到缓冲图层中
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000)
    tmp = buff_feat.SetGeometry(buff_geom)
    tmp = buff_lyr.CreateFeature(buff_feat)


# 将城市图层与火山缓冲图层相交
result_lyr = memory_ds.CreateLayer('result')
buff_lyr.Intersection(cities_lyr, result_lyr)

# 获得城市数：美国有多少个城市在火山1600米范围内
print('Cities: {}'.format(result_lyr.GetFeatureCount()))
## 输出 Cities：83
```

【方法二】将缓冲区添加到一个复合多边形中，而不是临时图层
1. UnionCascaded方法可以有效地将所有的多边形合并成一个符合多边形
2. 使用此方法将所有的火山缓冲区合并成一个多边形
3. 然后使用最终结果作为城市图层的空间过滤条件

```python
import ogr

# 打开两个图层
shp_ds = ogr.Open(2001)
volcano_lyr = shp_ds.GetLayer('us_volcanos_albers')
cities_lyr = shp_ds.GetLayer('cities_albers')

# 创建复合面图层
multipoly = ogr.Geometry(ogr.wkbMultiPolygon)
for volcano_feat in volcano_lyr:
    buff_geom = volcano_feat.geometry().Buffer(16000) #缓冲区Fenix
    multipoly.AddGeometry(buff_geom) #将缓冲得到的面数据添加到复合面图层

# 然后将复合面图层内的所有面进行联合
# 对城市进行空间选择
cities_lyr.SetSpatialFilter(multipoly.UnionCascaded())
print('Cities: {}'.format(cities_lyr.GetFeatureCount()))

## 输出 Cities：78
```

【对比】
1. 第一种方法83，第二种方法78
2. 第一种所算的城市比较多，是因为缓冲区生成的面有交集
3. 第二种按照空间选择，就不会多选择出来点

## 距离
查询两个要素的距离：`geom1.Distance(geom2)`

【例子】查看西雅图离活火山雷尼尔山的距离
```python
volcano_lyr.SetAttributeFilter("NAME = 'Rainier'")
feat = volcano_lyr.GetNextFeature()
rainier = feat.geometry().Clone()

cities_lyr.SetAttributeFilter("NAME= 'Seattle'")
feat = cities_lyr.GetNextFeature()
seattle = feat.geometry().Clone()

meters = round( rainier.Distance(seattle) )
miles = meters / 1600
print('{} meters ({} miles)'.format(meters, miles))
```

# 注意
【关于2.5D的问题】
1. geometry可以创建为2.5D，也就是有Z值
2. 但是在空间分析时，不会考虑它的Z值
3. 比如两个2.5D的点，计算距离，他们的距离还是2D的距离，不会考虑Z