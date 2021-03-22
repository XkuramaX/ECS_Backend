"""Routines associated with the application data.
"""
import json

courses = {}


def load_data():
    f = open("./json/course.json")
    d = json.load(f)
    ds = {}
    for i in range(len(d)):
        ds[d[i]["id"]] = d[i]
    f.close()
    return ds

def load_data_list():
    f = open("./json/course.json")
    d = json.load(f)
    f.close()
    return d



