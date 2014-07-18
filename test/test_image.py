#!/usr/bin/env python
# -*- coding: utf-8 -*-

# export PYTHONPATH=/z/workspace/airtest

import os
import pytest
import string

import airtest
from airtest import image

def test_image_locate_file_not_exists():
    with pytest.raises(IOError):
        image.locate_one_image('yy.png', 'zz.png')
    with pytest.raises(IOError):
        image.locate_one_image('testdata/yy.png', 'zz.png')

def test_locate_one_image():
    dirs = [p for p in os.listdir('testdata') if p.startswith('img1-')]
    for d in dirs:
        folder = os.path.join('testdata', d)

        EXPECT_FILE = os.path.join(folder, 'expect.txt')
        TRAIN_FILE = os.path.join(folder, 'train.png')

        #
        # format: <filename> <left-up> <right-bottom>
        # eg: q1.png 100 200 40 20
        #
        for line in open(EXPECT_FILE):
            line = line.strip()
            name, extra = string.split(line, maxsplit=1)
            query_file = os.path.join(folder, name)
            print 'TEST:', query_file, extra
            x0, y0, x1, y1 = map(int, extra.split())
            assert x0 < x1
            assert y0 < y1

            point = image.locate_one_image(TRAIN_FILE, query_file)
            assert point != None
            (x, y) = point
            assert x0 < x < x1
            assert y0 < y < y1

