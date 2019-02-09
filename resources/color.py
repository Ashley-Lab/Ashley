from discord import Colour
from random import randint


def random_color():
    R, G, B = randint(0, 255), randint(0, 255), randint(0, 255)
    return Colour.from_rgb(R, G, B)
