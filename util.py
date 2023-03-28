from math import floor
from random import random

def rnd(max: int):
    return floor(random()*max)

def opposite_dir(dir: int) -> int:
    return dir ^ 0b10

def sign(x) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0