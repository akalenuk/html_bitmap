html_bitmap
===========

This module lets you draw bitmaps as Python native lists and save them as HTML tables. I do functions plots and diagrams with it (see use_case_x.py). The module has no dependencies and works in pure Python. Current version is "modernized" to work in Python 3.x but there is a Python 2.x branch too.

This plot-in-HTML thing comes in handy if, like me, you enjoy working on obscure and underpowered machines with little or broken support for 3d-part dependencies such as matlplotlib.

All the capabilities are:

    to_hex(r, g, b)     # for making nice HTML hex color
    new_bitmap(w, h, col="")
    pixel_on(bitmap, x, y, col="")
    rect_on(bitmap, x, y, w, h, col="")
    line_on(bitmap, x1, y1, x2, y2, col="", width=1)
    circle_on(bitmap, cx, cy, r, col="", width=1)
    to_html(bitmap)

