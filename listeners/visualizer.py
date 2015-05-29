# The plot server must be running
# Go to http://localhost:5006/bokeh to view this plot

import time

import random

import numpy as np

from bokeh.plotting import cursession, figure, show, output_server

from json import loads

from structures.game import AttrDict


def main(equeue, name, cpipe):
    def getField():
        equeue.put(('getField', '', name))
        return cpipe.recv()

    max_cnt = 300
    fs = 300
    out = 500
    base_radius = 10
    unit_radius = 3

    colors = ["red", "blue", "green", "magenta"]

    x, y = [out for i in range(max_cnt)], [out for i in range(max_cnt)]

    output_server("circle_animate")

    p = figure(x_range=[-fs, fs], y_range=[-fs, fs])

    p.circle(x, y, radius=[3 for i in range(max_cnt)], color=["white" for i in range(max_cnt)], name="cir")

    show(p)

    renderer = p.select(dict(name="cir"))
    ds = renderer[0].data_source

    #print(ds.data)

    while True:
        x = [out for i in range(max_cnt)]
        y = [out for i in range(max_cnt)]
        c = ["white" for i in range(max_cnt)]
        r = [1 for i in range(max_cnt)]
        cnt = 0

        def add(xs, ys, col, rad):
            global x, y, c, r, cnt
            x[cnt] = xs
            y[cnt] = ys
            c[cnt] = col
            r[cnt] = rad
            cnt += 1

        field = getField()

        for i in range(len(field)):
            cur = field[i]
            add(cur.base.position.x, cur.base.position.y, colors[i], 10)

            for u in cur.units:
                add(u.position.x, u.position.y, colors[i], 3)


        ds.data['x'] = x
        ds.data['y'] = y
        ds.data['radius'] = r
        ds.data['fill_color'] = c
        cursession().store_objects(ds)
        time.sleep(0.3)
