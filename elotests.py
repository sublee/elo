# -*- coding: utf-8 -*-
from attest import Tests, assert_hook, raises

from elo import *


suite = Tests()


@suite.test
def wikipedia_example():
    rating = 1613
    series = [(LOSE, 1609), (DRAW, 1477), (WIN, 1388), (WIN, 1586),
              (LOSE, 1720)]
    assert round(rate(rating, series, USCF_K_FACTOR)) == 1601
