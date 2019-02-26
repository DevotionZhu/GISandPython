[toc]

# 大地水准面与椭球体

# PROJ.4
【PROJ.4】开源GIS最著名的地图投影库，它专注于地图投影的表达，以及转换
【GDAL】GDAL中的投影转换函数（类CoordinateTransformation中的函数）也是动态调用该库函数的

【详细与安装】https://blog.csdn.net/summer_dew/article/details/86608111#Proj4_24

## 命令行
proj命令是对经纬度进行投影的，实现经纬度坐标、地理坐标相互转换
```bash
> proj #显示proj程序的用法（包括参数设置、可选项、输入文件）
> proj -l | wc -l #显示proj里内置的有关地理投影的参数
> proj -lu | wc -l #查看所支持的单位
> proj -le | wc -l #查看支持的椭球体(elliposid)信息，以及各个椭球体向WGS84椭球体转换的参数
> proj -ld #显示proj4支持的基准面信息
```