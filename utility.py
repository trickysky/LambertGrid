#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/30

import math
from pgutil import Database

R = 6378137
a = R
b = 6356752.314245
pi = math.pi
e = math.e

e1 = (1.0 - (b / a) ** 2.0) ** 0.5
e2 = ((a / b) ** 2.0 - 1.0) ** 0.5
K = (a ** 2.0 / b) / (1.0 + e2 ** 2.0) ** 0.5
original_x = -1.0 * R * pi
original_y = R * pi


class Point:
	def __init__(self, x, y, srid):
		self.x = x
		self.y = y
		self.srid = srid

	def LonLat2WebMercator(self):
		if 4326 == self.srid:
			self.x = R * self.x * pi / 180.0
			self.y = R * math.log(math.tan(pi / 4 + self.y * pi / 360.0))
			self.srid = 3857
			return self
		else:
			print 'srid error'

	def WebMercator2LonLat(self):
		if 3857 == self.srid:
			self.x = float(self.x) / R * 180.0 / pi
			self.y = 360.0 * math.atan(e ** (self.y / R)) / pi - 90.0
			self.srid = 4326
			return self
		else:
			print 'srid error'

	def LonLat2Mercator(self):
		if 4326 == self.srid:
			self.x = K * self.x * pi / 180.0
			self.y = K * math.log(math.tan(pi / 4 + self.y * pi / 360.0) * (
			(1 - e1 * math.sin(self.y * pi / 180.0)) / (1 + e1 * math.sin(self.y * pi / 180.0))) ** (e1 / 2.0))
			self.srid = 3395
			return self
		else:
			print 'srid error'

	def WebMercator2TileId(self, level):
		if 3857 == self.srid:
			tile_x = math.floor((self.x - original_x) / (R * pi) * 2.0 ** (level - 1))
			tile_y = math.floor(abs((self.y - original_y)) / (R * pi) * 2.0 ** (level - 1))
			return int(tile_x), int(tile_y)
		else:
			print 'srid error'


	def LonLat2LambertTile(self, level):
		if 4326 == self.srid:
			tile_x = math.floor((self.x + 180.0) / 180.0 * 2.0 ** (level - 1))
			tile_y = math.floor((1.0-math.sin(self.y*pi/180.0)) * 2.0 ** (level - 1))
			return int(tile_x), int(tile_y)
		else:
			print 'srid error'


def get_map_tile_grid_point(tile_x, tile_y, level):
	min_x = R * pi / 2 ** (level - 1) * tile_x + original_x
	max_x = R * pi / 2 ** (level - 1) * (tile_x + 1) + original_x
	min_y = original_y - R * pi / 2 ** (level - 1) * (tile_y + 1)
	max_y = original_y - R * pi / 2 ** (level - 1) * tile_y
	return Point(min_x, min_y, 3857), Point(max_x, max_y, 3857)


def get_lambert_grid_point(tile_x, tile_y, level):
	min_x = 360.0 / 2**level * tile_x -180.0
	max_x = 360.0 / 2**level * (tile_x + 1) -180.0
	min_y = math.asin(1 - (1.0 / 2**(level - 1)) * (tile_y + 1)) * 180.0 / pi
	max_y = math.asin(1 - (1.0 / 2**(level - 1)) * tile_y) * 180.0 / pi
	return Point(min_x, min_y, 4326), Point(max_x, max_y, 4326)


def make_square(point1, point2):
	if point1.srid == point2.srid:
		min_x = str(min(point1.x, point2.x))
		max_x = str(max(point1.x, point2.x))
		min_y = str(min(point1.y, point2.y))
		max_y = str(max(point1.y, point2.y))
		p1 = (max_x, max_y)
		p2 = (max_x, min_y)
		p3 = (min_x, min_y)
		p4 = (min_x, max_y)
		string_line = ','.join(map(' '.join, (p1, p2, p3, p4, p1)))
		sql_geom = """public.ST_Polygon(public.ST_GeomFromText('LINESTRING(%s)'), %s)""" % (string_line, point1.srid)
		return sql_geom


def calc_map_tile_grids(point1, point2, level):
	if point1.srid == point2.srid:
		min_x = min(point1.x, point2.x)
		max_x = max(point1.x, point2.x)
		min_y = min(point1.y, point2.y)
		max_y = max(point1.y, point2.y)
		globe_min = Point(min_x, max_y, 3857) if 3857 == point1.srid else Point(min_x, max_y, 4326).LonLat2WebMercator()
		tile_x_min, tile_y_min = globe_min.WebMercator2TileId(level)
		globe_max = Point(max_x, min_y, 3857) if 3857 == point1.srid else Point(max_x, min_y, 4326).LonLat2WebMercator()
		tile_x_max, tile_y_max = globe_max.WebMercator2TileId(level)
		tiles = []
		for tile_x in range(tile_x_min, tile_x_max+1, 1):
			for tile_y in range(tile_y_min, tile_y_max+1, 1):
				tiles.append((tile_x, tile_y))
		return tiles


china_min = Point(73.50235488, 18.14259204, 4326)
china_max = Point(135.09567, 53.56362402, 4326)


def create_map_tile_grids(level, db):
	db = Database(db)
	sql_create_tmp = """CREATE TABLE public.creat_tile_grids_tmp (geom GEOMETRY, tile_x INTEGER, tile_y INTEGER);"""
	db.execute(sql_create_tmp)
	tiles = calc_map_tile_grids(china_min, china_max, level)
	sqls = []
	for tile in tiles:
		p_min, p_max = get_map_tile_grid_point(tile[0], tile[1], level)
		sql = """INSERT INTO public.creat_tile_grids_tmp (%s, %s, %s) VALUES (%s, %s, %s);""" % ('geom', 'tile_x', 'tile_y', make_square(p_min, p_max), tile[0], tile[1])
		print sql
		sqls.append(sql)
	db.execute(''.join(sqls))
	valid_grid_sql = """SELECT t1.geom, tile_x, tile_y INTO working.grid_%s FROM public.creat_tile_grids_tmp AS t1, working.china AS t2 WHERE st_intersects(t1.geom, t2.geom) IS TRUE;""" % level
	db.execute(valid_grid_sql)
	truncate_sql = """DROP TABLE public.creat_tile_grids_tmp;"""
	db.execute(truncate_sql)

