from dataclasses import dataclass

@dataclass
class Color:
    """Color palette"""
    background = (62, 80, 113)
    medium = (141,167,190)
    light = (205,230,245)
    highlight = (133,196,106)
    warning = (244,162,97)
    pearl = (4,231,98)
    flesh = (255,185,151)