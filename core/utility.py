from PyQt5.QtGui import QColor, QVector2D, QPainterPath
from PyQt5.QtCore import QPointF
import sys

def simple_max_contrasting_color(color):
    return QColor(
        0 if color.red() > 127 else 255,
        0 if color.green() > 127 else 255,
        0 if color.blue() > 127 else 255,
        color.alpha())


def closest_point_on_path(point:QPointF, path:QPainterPath) -> QPointF:
    if path.isEmpty():
        return point

    vec = QVector2D(point)
    poly = path.toFillPolygon()
    minDist = sys.float_info.max

    for k in range(poly.count()):
        p = QVector2D(poly.at(k))
        if k == poly.count() - 1:
            k = -1 
        q = QVector2D(poly.at(k+1))
        v = q - p
        u = v.normalized()
        d = QVector2D.dotProduct(u, vec - p)

        if d < 0.0:
            d = (vec - p).lengthSquared()
            if d < minDist:
                minDist = d
                minVec = p
        elif d*d > v.lengthSquared():
            d = (vec - q).lengthSquared()
            if d < minDist:
                minDist = d
                minVec = q
        else:
            u *= d
            u += p
            d = (vec - u).lengthSquared()
            if d < minDist:
                minDist = d
                minVec = u

    if minDist >= sys.float_info.max:
        return point

    return minVec.toPointF()
