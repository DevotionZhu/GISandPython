# coding:utf8


# config.py --> pois.json --> shp
# if __name__ == '__main__':
#     import amap_poi
#     pois = amap_poi.get_pois()
#     print pois
#     # 【保存】
#     amap_poi.save_pois(pois)

# pois.json --> shp
if __name__ == '__main__':
    import amap_poi
    from Tools import crawler_log

    POIS_PATH = r'D:\mycode\GISandPython\3CrawlerOfGIS\amap\poi\data\[2019-03-30 11-48-37] pois.json'

    # 【获得POIS】
    pois = crawler_log.read_json(POIS_PATH)
    # print pois
    # 【保存】
    amap_poi.save_pois(pois)
    pass