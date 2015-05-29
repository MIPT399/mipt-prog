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
        equeue.put((method, name, self))
        return cpipe.recv()

    max_cnt = 300


    x, y = [0 for i in range(max_cnt)], [0 for i in range(max_cnt)]

    output_server("circle_animate")

    p = figure(x_range=[-300, 300], y_range=[-300, 300])

    p.circle(x, y, radius=3, color="red", name="cir")

    show(p)

    renderer = p.select(dict(name="cir"))
    ds = renderer[0].data_source

    #print(ds.data)

    cnt = 0

    while True:
        x = [random.randint(-300, 300) for i in range(max_cnt)]
        y = [random.randint(-300, 300) for i in range(max_cnt)]
        ds.data['x'] = x
        ds.data['y'] = y
        cursession().store_objects(ds)
        time.sleep(0.3)
