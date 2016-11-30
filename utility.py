#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/30

import math

R = 6378137
a = R
b = 6356752.314245
pi = math.pi
e = math.e

e1 = (1 - (b / a) ** 2) ** 0.5
e2 = ((a / b) ** 2 - 1) ** 0.5
K = (a ** 2 / b) / (1 + e2 ** 2) ** 0.5


def lonlat2webmercator(longitude, latitude):
	x = R * longitude * pi / 180
	y = R * math.log(math.tan(pi / 4 + latitude * pi / 360))
	return x, y


def webmercator2lonlat(x, y):
	longitude = float(x) / R * 180 / pi
	latitude = 360 * math.atan(e ** (y / R)) / pi - 90
	return longitude, latitude


def lonlat2mercator(longitude, latitude):
	x = K * longitude * pi / 180
	y = K * math.log(math.tan(pi / 4 + latitude * pi / 360) * (
	(1 - e1 * math.sin(latitude * pi / 180)) / (1 + e1 * math.sin(latitude * pi / 180))) ** (e1 / 2))
	return x, y

