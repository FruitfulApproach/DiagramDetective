from PyQt5.QtGui import QColor


def simple_max_contrasting_color(color):
    return QColor(
        0 if color.red() > 127 else 255,
        0 if color.green() > 127 else 255,
        0 if color.blue() > 127 else 255,
        color.alpha())