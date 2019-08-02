# POI
1. 记录点、线、面的ID




# detail
## 举例
【点】厦门市人民政府 http://ditu.amap.com/detail/get/detail?id=B02500088C
【线】理工路 http://ditu.amap.com/detail/get/detail?id=B0FFH6JRIF
【面】厦门园林植物园 http://ditu.amap.com/detail/get/detail?id=B025003OPX

## 请求
【URL】http://ditu.amap.com/detail/get/detail?id=POIID
【参数】POI的ID
【获得方法】https://lbs.amap.com/api/webservice/guide/api/search

## 返回值
【说明】
1. 未知类型标记为str
2. 只截取有用信息

- object dict
	- status : int `可能值：1(OK)`
	- data dict
		- share_url : str  `http://wb.amap.com/?p=B025003OPX%2C24.451736%2C118.112119%2C%E5%8E%A6%E9%97%A8%E5%9B%AD%E6%9E%97%E6%A4%8D%E7%89%A9%E5%9B%AD%2C%E5%8E%A6%E9%97%A8%E5%B8%82%E6%80%9D%E6%98%8E%E5%8C%BA%E8%99%8E%E5%9B%AD%E8%B7%AF25%E5%8F%B7`
		- spec dict
			- sp_pic dict
			- mining_shape dict `坐标信息：包括线、面`
				- level : int
				- area : double
				- shape : 118.11613,24.454292;118.116297,24.46341;...
		- base dict
			- name : 厦门园林植物园
			- alias_name : 万石植物园
			- business
			- x : double
			- y : double
			- poiid : str
			- pixely : str
			- new_type : str
			- poi_tag : str
			- city_adcode : int
			- geodata dict
				- aoi list
					- area : double
					- name : str
					- mainpoi : str
			- title : 风景名胜
			- navi_geometry : 118.090795,24.456474 `[?] 几何中心`
			- tag : 风景名胜;公园广场;植物园
			- city_name : 厦门市
			- classify : 公园广场
		- pic list
			- weight : 998
			- srcheight int
			- url `可能为空`
			- iscover
			- title 厦门园林植物园 `可能为空`
			- text_sensibility : 2
		- score
			- 总分 : 4.5
			- 星级 : 4A景区

# 参数配置
```python
params = {
    #输出的文件夹
    "out_dir" : "D:\\mycode\\GISandPython\\3CrawlerOfGIS\\amap\\data", 
    #输出的文件名
    "out_name" : "厦门市地铁站.shp",                                        
    #类型 0:point 1:line 2:polygon
    "shp_type" : 0,                                                    
    #最大页数
    "MAX_PAGE" : 100000,       
    #url中的参数：https://lbs.amap.com/api/webservice/guide/api/search#text                                        
    "url_param" : {                                                        
        # 【keywords】与【types】至少填一种
        "keywords" : "地铁",  
        # 查看Excel文件[0 POIcode.xlsx]
        "types" : "",
        0citycode.xlsx
        "city" : "厦门市",
        "citylimit" : "true",
        "output" : "json",
        "key" : "4fac3db866dcc3b8a735651d3a7db1c7"
    },
    "save_field" : [
        #get_pois()中把ID保存成了poiid --> 所以保存ID要写成poiid
        ["poiid", "TEXT", 250],
        ["name", "TEXT", 250],
        ["type", "TEXT", 500],
        ["typecode", "TEXT", 250],
        ["adname", "TEXT", 250],
        ["address", "TEXT", 500],
        ["pname", "TEXT", 250],
        ["cityname", "TEXT", 250],
        ["tel", "TEXT", 250]
    ]
}
```