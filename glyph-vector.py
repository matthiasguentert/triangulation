#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
#  - The code is incomplete and over-simplified, as it ignores the 3rd order
#    bezier curve bit and always intepolate between off-curve points.
#    This is only correct for truetype fonts (which only use 2nd order bezier curves).
#  - Also it seems to assume the first point is always on curve; this is
#    unusual but legal.
#
# -----------------------------------------------------------------------------
'''
Show how to access glyph outline description.
'''
from freetype import *

if __name__ == '__main__':
    import numpy
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import matplotlib.patches as patches

    face = Face("C:\Windows\Fonts\Arial.ttf")
    face.set_char_size(48*64)
    face.load_char('Q')
    slot = face.glyph

    outline = slot.outline
    points = numpy.array(outline.points, dtype=[('x', float), ('y', float)])
    x, y = points['x'], points['y']

    figure = plt.figure(figsize=(8, 10))
    axis = figure.add_subplot(111)
    #axis.scatter(points['x'], points['y'], alpha=.25)
    start, end = 0, 0

    VERTS, CODES = [], []
    # Iterate over each contour
    for i in range(len(outline.contours)):
        end = outline.contours[i]
        points = outline.points[start:end+1]
        points.append(points[0])
        tags = outline.tags[start:end+1]
        tags.append(tags[0])

        segments = [[points[0], ], ]
        for j in range(1, len(points)):
            segments[-1].append(points[j])
            if tags[j] & (1 << 0) and j < (len(points)-1):
                segments.append([points[j], ])
        verts = [points[0], ]
        codes = [Path.MOVETO, ]
        for segment in segments:
            if len(segment) == 2:
                verts.extend(segment[1:])
                codes.extend([Path.LINETO])
            elif len(segment) == 3:
                verts.extend(segment[1:])
                codes.extend([Path.CURVE3, Path.CURVE3])
            else:
                verts.append(segment[1])
                codes.append(Path.CURVE3)
                for i in range(1, len(segment)-2):
                    A, B = segment[i], segment[i+1]
                    C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                    verts.extend([C, B])
                    codes.extend([Path.CURVE3, Path.CURVE3])
                verts.append(segment[-1])
                codes.append(Path.CURVE3)
        VERTS.extend(verts)
        CODES.extend(codes)
        start = end+1

    # Draw glyph lines
    path = Path(VERTS, CODES)
    glyph = patches.PathPatch(path, facecolor='.75', lw=1)

    # Draw "control" lines
    for i, code in enumerate(CODES):
        if code == Path.CURVE3:
            CODES[i] = Path.LINETO
    path = Path(VERTS, CODES)
    patch = patches.PathPatch(path, ec='.5', fill=False, ls='dashed', lw=1)

    axis.add_patch(patch)
    axis.add_patch(glyph)

    axis.set_xlim(x.min()-100, x.max()+100)
    plt.xticks([])
    axis.set_ylim(y.min()-100, y.max()+100)
    plt.yticks([])
    plt.show()
