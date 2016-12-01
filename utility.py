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


class Point():
	def __init__(self, x, y, srid):
		self.x = x
		self.y = y
		self.srid = srid


	def LonLat2WebMercator(self):
		if 4326 == self.srid:
			self.x = R * self.x * pi / 180
			self.y = R * math.log(math.tan(pi / 4 + self.y * pi / 360))
			self.srid = 3857
		else:
			print 'srid error'


	def WebMercator2LonLat(self):
		if 3857 == self.srid:
			self.x = float(self.x) / R * 180 / pi
			self.y = 360 * math.atan(e ** (self.y / R)) / pi - 90
			self.srid = 4326
		else:
			print 'srid error'


	def LonLat2Mercator(self):
		if 4326 == self.srid:
			self.x = K * self.x * pi / 180
			self.y = K * math.log(math.tan(pi / 4 + self.y * pi / 360) * ((1 - e1 * math.sin(self.y * pi / 180)) / (1 + e1 * math.sin(self.y * pi / 180))) ** (e1 / 2))
			self.srid = 3395
		else:
			print 'srid error'



def WebMercator2TileId(point, level):
	if 3857 == point.srid:
		tile_x = math.floor((point.x - original_x)/(R * pi)*2**(level-1))
		tile_y = math.floor(abs((point.y - original_y))/(R * pi)*2**(level-1))
		return int(tile_x), int(tile_y)


def DrawMapTileGrid(tile_x, tile_y, level):
	min_x = R * pi / 2**(level-1) * tile_x + original_x
	max_x = R * pi / 2**(level-1) * (tile_x + 1) + original_x
	min_y = original_y - R * pi / 2**(level-1) * (tile_y + 1)
	max_y = original_y - R * pi / 2**(level-1) * tile_y
	print min_x, min_y
	print max_x, max_y

