#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/30

import math

R = 6378137
pi = math.pi
e = math.e

def lonlat2webmercator(longitude, latitude):
	x = R * longitude * pi / 180
	y = R * math.log(math.tan(pi / 4 + latitude * pi/360))
	return x, y


def webmercator2lonlat(x, y):
	longitude = float(x) / R * 180 / pi
	latitude = 360 * math.atan(e**(y/R)) / pi - 90
	return longitude, latitude

