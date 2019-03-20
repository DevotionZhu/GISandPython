【定义】只有X和Y坐标的几何要素被认为是二维的
1. 在OGR中带有额外Z坐标的几何要素被认为是2.5D，而不是3D
2. 因为OGR进行空间操作时，不考虑Z值

【OGR常量表示的不同几何类型】

|几何类型|2D常量|2.5D常量|
|-|-|-|
|点|wkbPoint|wkbPoint25D|
|多点|wkbMultiPoint|wkbMultiPoint25D|
|线|wkbLineString|wkbLineString25D|
|多线|wkbMultiLineString|wbkMultiLineString25D|
|多边形环|wkbLinearRing|n/a|
|面|wkbPolygon|wkbPolygon25D|
|多面|wkbMultiPolygon|wkbMultiPolygon|
|几何集合|wkbGeometryCollection|wkbGeometryCollection25D|


【知识补充】

1. WKT（well-known text）：文本标记语言由开放地理空间联盟(OGC)制定，用于表示矢量数据中的几何对象。
2. WKB（well-known binary）：在数据传输与数据库存储时，WKT的二进制形式
【总结】两者利用文本简洁明了的表达矢量空间要素的几何信息，使得几何信息能以字段的形式存储于数据库中

# 单点Point

```python
from osgeo import ogr
point = ogr.Geometry(ogr.wkbPoint) #创建一个空的点
point.AddPoint(59.5, 11.5) #添加坐标值：北方向为11.5，东方向为59
x,y = point.GetX(),point.GetY() #获得X，Y
print(point) #按照WKT格式输出几何对象
point.SetPoint(0, 59.5, 13)
	# SetPoint(point, x, y, [z])：point为编辑定点的索引值，而wkbPoint只允许有一个点，即为0
```

# 多点MultiPoint
```python
points = ogr.Geometry(ogr.wkbMultiPoint) #创建多点
point = ogr.Geometry(ogr.wkbPoint) #创建一个空点
point.AddPoint(67.5, 16) # 设置数值
points.AddGeometry(point) # 将点加到多点
point.AddPoint(73, 31) #【重用点对象】point是单个点，再次AddPoint会把原来的数值替换掉
points.AddGeometry(point) #再添加
# 获得指定点
points.GetGeometryRef(1).AddPoint(75, 32) #修改第二点的坐标为75，32
# 遍历点
for i in range(points.GetGeometryCount() ):
	pt = points.GetGeometryRef(i)
	pt.AddPoint(pt.GetX() +2, pt.GetY() ) #每个点的X坐标都加2
```

# 线要素Line
```python
line = ogr.Geometry(ogr.wkbLineString)
# 按顺序添加点
line.AddPoint(54, 37)
line.AddPoint(62, 35.5)
line.AddPoint(70.5, 38)
# 编辑
line.SetPoint(2, 70, 38) #重新设置第3个点的坐标
# 获取
line.GetX(2),line.GetY(2) #得到第3个点的坐标
line.GetPoints()
# 遍历
for i in range(line.GetPointCount()):
	line.SetPoint(i , line.GetX(i), line.Get(Y)+1) #每个点的Y都偏移1
```

【在线的点集中再插入一个点】
```python
# 在线的点集中再插入一个点
points = line.GetPoints() #取出点集
points[2:2] = [(66.5, 35) ] #list[i:i]在列表第i个位置插入元素
for point in points: #再逐点插入
	line.SetPoint(*vertex) #Python运算符*将元组展开成为独立参数->变为vertex[0]，vertex[1]再传入
		# 若line只有10个点（索引0-9），SetPoint方法设置索引为15时，它也将创建10~14的定点，但10~14的坐标只为0
```

# 多线MultiLine
【创建】
```python
# 创建路径1
path1 = ogr.Geometry(ogr.wkbLineString); path1.AddPoint(61.5, 29); path1.AddPoint(63, 20)
# 创建路径2
path2 = ogr.Geometry(ogr.wkbLineString); path2.AddPoint(69.5, 33); path2.AddPoint(80, 33)
# 创建多线几何
paths = ogr.Geometry(ogr.wkbMultiLineString)
paths.AddGeometry(path1); paths.AddGeometry(path2)
```

【编辑】
```python
paths.GetGeometryRef(0).SetPoint(1, 63, 22) #编辑第1条线的第2个点：坐标设置为63,22
```

【遍历】
```python
for i in range(paths.GetGeometryCount() ):
	path = paths.GetGeometryRef(i)
	for j in range(path.GetPointCount()):
		path.SetPoint(j, path.GetX(j)+2, path.GetY(j)-3 ) #对MultiLine中的所有点做偏移
```

# 单多边形
> 1. shapefile指定外环是顺时针方向
> 2. GeoJSON没有指定顺序


单多边形：第一个和最后一个顶点必须有相同的坐标
1. 可以自己添加最后一个坐标，让他与第一个相同
2. 在环形或多边形上调用CloseRings方法

【创建】
```python
# 创建环
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(58, 38.5)
ring.AddPoint(53, 6)
ring.ADdPoint(99.5, 19)
polygon = ogr.Geometry(ogr.wkbPolygon) #创建多边形
polygon.AddGeometry(ring) #添加环
polygon.CloseRings() #闭合
```

【遍历】
```python
ring = polygon.GetGeometryRef(0) #获得第0个环
for i in range(ring.GetPointCOunt() ):
	ring.SetPoint(i, ring.GetX(i)-5, ring.GetY(i) )
```

【在环中再插入点】
```python
ring = polygon.GetGeometryRef(0)
vertices = ring.GetPoints()
vertices[2:3] = ( (90,16), (90,27) ) #再插入两个点
for i in range(len(vertices) ):
	ring.SetPoint(i, *vertices[i])
```

# 复合多边形MutliPolygon
```python
# 创建第一个多边形
box1 = ogr.Geometry(ogr.wkbLinearRing)
box1.AddPoint(87.5, 25.5)
box1.AddPoint(89, 25.5)
box1.AddPoint(89, 24)
box1.AddPoint(87.5, 24)
garden1 = ogr.Geometry(ogr.wkbPolygon)
garden1.AddGeometry(box1)

# 创建第二个多边形
box2 = ogr.Geometry(ogr.wkbLinearRing)
box2.AddPoint(89, 23)
box2.AddPoint(92, 23)
box2.AddPoint(92,22)
box2.AddPoint(89,22)
garden2 = ogr.Geometry(ogr.wkbPolygon)
garden2.AddGeometry(box2)

# 加入到复合多边形中
gardens = ogr.Geometry(ogr.wkbMultiPolygon)
gardens.AddGeometry(garden1)
gardens.AddGeometry(garden2)
gardens.CloseRings()

# 遍历
for i in range(polygons.GetGeometryCount() ):
	ring = gardens.GetGeometryRef(i).GetGeometryRef(0)
	for j in range(ring.GetPointCount() ):
		ring.SetPoint(j, ring.GetX(j)+1, ring.GetY(j)+0.5 )
```

# 带洞的多边形
```python
from osgeo import ogr
# 外环
lot = ogr.Geometry(ogr.wkbLinearRing)
lot.AddPoint(58, 38.5)
lot.AddPoint(53, 6)
lot.AddPoint(99.5, 19)
lot.AddPoint(73, 42)

# 内环
house = ogr.Geometry(ogr.wkbLinearRing)
house.AddPoint(67.5, 29)
house.AddPoint(69, 25.5)
house.AddPoint(64, 23)
house.AddPoint(69, 15)
house.AddPoint(82.5, 22)
house.AddPoint(76, 31.5)

yard = ogr.Geometry(ogr.wkbPolygon) #创建多边形
yard.AddGeometry(lot) # 先添加外环
yard.AddGeometry(house) #后添加内环
yard.CloseRings() #闭合

from ospybook.vectorplotter import VectorPlotter
vp = VectorPlotter(False) #非交互模式创建
vp.plot(yard, fill=False, hatch='X', color='blue')
vp.draw()
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190320175744984.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3N1bW1lcl9kZXc=,size_16,color_FFFFFF,t_70)

【遍历】
```python
for i in range(yard.GetGeometryCount() ):
	ring = yard.GetGeometryRef(i)
	for j in range(ring.GetPointCount() ):
		ring.SetPoint(j, ring.GetX(j)-5, ring.GetY(j) )
```

# 其他模块处理几何要素
## Fiona
【Fiona】读写矢量数据的几何库，建立在OGR库基础上
1. Fiona不使用特殊的几何类型，而是使用Python列表来存储定点
2. 列表里填充着包含定点坐标的元组
3. 用户手册优秀：https://fiona.readthedocs.io/en/latest/
4. 不能做空间分析


## Shapely
【Shapely】专为处理几何类型而设计的优秀模块，但不能读写数据
1. 不像Fiona，Shapely确实有特殊的几何类型，这就是为什么shapely可以做空间分析，而Fiona不行
2. 尽管拥有自己的数据类型，但基本的几何类型概念则始终不变
3. 用户手册：https://shapely.readthedocs.io/en/latest/