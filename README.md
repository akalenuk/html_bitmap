html_bitmap
===========

This module lets you draw some primitive on pythons jagged lists and then write it to the big HTML table.

All the capabilities are:

    to_hex(r, g, b)     # for making nice HTML hex color
    new_bitmap(w, h, col="")
    pixel_on(bitmap, x, y, col="")
    rect_on(bitmap, x, y, w, h, col="")
    line_on(bitmap, x1, y1, x2, y2, col="", width=1)
    circle_on(bitmap, cx, cy, r, col="", width=1)
    to_html(bitmap)
