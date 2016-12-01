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
original_x = -1 * R * pi
original_y = R * pi


def LonLat2WebMercator(longitude, latitude):
	x = R * longitude * pi / 180
	y = R * math.log(math.tan(pi / 4 + latitude * pi / 360))
	return x, y


def WebMercator2LonLat(x, y):
	longitude = float(x) / R * 180 / pi
	latitude = 360 * math.atan(e ** (y / R)) / pi - 90
	return longitude, latitude


def LonLat2Mercator(longitude, latitude):
	x = K * longitude * pi / 180
	y = K * math.log(math.tan(pi / 4 + latitude * pi / 360) * (
	(1 - e1 * math.sin(latitude * pi / 180)) / (1 + e1 * math.sin(latitude * pi / 180))) ** (e1 / 2))
	return x, y


def WebMercator2TileId(x, y, level):
	tile_x = math.floor((x - original_x)/(R * pi)*2**(level-1))
	tile_y = math.floor(abs((y - original_y))/(R * pi)*2**(level-1))
	return int(tile_x), int(tile_y)


def DrawTile(tile_x, tile_y, level):
	min_x = R * pi / 2**(level-1) * tile_x + original_x
	max_x = R * pi / 2**(level-1) * (tile_x + 1) + original_x
	min_y = original_y - R * pi / 2**(level-1) * (tile_y + 1)
	max_y = original_y - R * pi / 2**(level-1) * tile_y
	print min_x, min_y
	print max_x, max_y
	print WebMercator2LonLat(min_x, min_y)
	print WebMercator2LonLat(max_x, max_y)

x, y = LonLat2WebMercator(116.397458, 39.908709)
DrawTile(13489, 6208, 14)