#!/usr/bin/python

import re
import glob
from shapely.geometry import Point, Polygon
from pathlib import Path

mission_end_time = 1200.0


def create_poly(coords):
    return Polygon(coords)


poly0 = Polygon([(107, -101), (112, -106), (112, -113), (107, -118),
                 (100, -118), (95, -113), (95, -106), (100, -101)])
poly1 = Polygon([(50, -30), (53, -33), (53, -38), (50, -42),
                 (45, -42), (41, -38), (41, -33), (45, -30)])
poly2 = Polygon([(82, -65), (87, -70), (87, -76), (82, -81),
                 (76, -81), (71, -76), (71, -70), (76, -65)])
poly3 = Polygon([(59, -101), (64, -105), (64, -112), (59, -116),
                 (53, -116), (48, -112), (48, -105), (53, -101)])
poly4 = Polygon([(107, -38), (112, -43), (112, -49), (107, -54),
                 (100, -54), (96, -49), (96, -43), (100, -38)])

all_polys = [poly0, poly1, poly2, poly3, poly4]


def test_point_inside_shapes(x, y):
    p = Point(x, y)
    for poly in all_polys:
        if p.within(poly):
            print("VIOLATION DETECTED: Point " +
                  str(p) + " is inside " + str(poly))
            return 1
        else:
            return 0


def process_file(input_alog_file, output_filename):
    fout = open(output_filename, "w")
    with open(input_alog_file) as origin_file:
        for line in origin_file:
            m = re.search(r'X=(.+),Y=(.+),SPD=(.+),HDG=(.+),TYPE=', line)
            if (m and ("NODE_REPORT_LOCAL" in line)):
                time = float(line.split(" ")[0])
                if (time < mission_end_time):
                    x = float(m.group(1))
                    y = float(m.group(2))
                    speed = m.group(3)
                    violation = test_point_inside_shapes(x, y)
                    fout.write(str(time) + "," + str(x) + "," + str(y) +
                               "," + speed + "," + str(violation) + "\n")
    fout.close()


def process_files_for_vehicle(vehicle_name):
    i = 1
    for path in Path(".").rglob("*" + vehicle_name + "*.alog"):
        inname = str(path)
        outname = vehicle_name + "-path-" + str(i) + ".path"
        print("Processing " + inname + " to " + outname)
        i = i + 1
        process_file(inname, outname)


process_files_for_vehicle("GILDA")
process_files_for_vehicle("HENRY")
