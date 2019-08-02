# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 17:44
# @Author  : PasserQi
# @Email   : passerqi@gmail.com
# @File    : batch_cut
# @Software: PyCharm
# @Version :
# @Desc    :

from osgeo import ogr

def batch_cut_merge(input_list, cut_shp):
    # get cutting geometry
    ds = ogr.Open(cut_shp)


    pass

def cut(input_file, cut_file):
    pass


if __name__ == '__main__':
    out_dir = r'E:\SAR\ps'
    out_name_field = u""
    cut_shp = r"E:\SAR\ps\xiamen.shp"
    input_list = [
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_160.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_161.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_162.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_163.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_164.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_165.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_166.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_167.shp",
        r"E:\SAR\ps\geocoding\4PS_20190405_PS_75_168.shp",
    ]


    pass