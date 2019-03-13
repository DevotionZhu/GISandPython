# coding:utf-8
import time
import os
import json

def save_json(obj, out_dir, fn):
    t = time.strftime('[%Y-%m-%d %H-%M-%S] ',time.localtime(time.time()))
    out_name = t + fn + ".json"
    out_path = os.path.join(out_dir, out_name)
    with open(out_path, "w+") as json_file:
        json.dump(obj, json_file)
        json_file.close()
    pass


def read_json(fpath):
    with open(fpath, 'r') as fp:
        ret = json.load(fp)
        fp.close()
    return ret