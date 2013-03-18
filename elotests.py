# -*- coding: utf-8 -*-
#http://elo.divergentinformatics.com/
import math

from almost import almost
from pytest import raises

from elo import *


def test_rating():
    assert isinstance(1.99, Rating)
    assert issubclass(float, Rating)
    assert Rating(100) == 100
    assert Rating(100) < 200
    assert Rating(100) <= 200
    assert not (Rating(100) == 200)
    assert not (Rating(100) > 200)
    assert not (Rating(100) >= 200)
    assert Rating(100) == Rating(100)
    assert Rating(100) != Rating(200)


def test_initial_rating():
    env = Elo(initial=1000)
    assert env.create_rating() == 1000


def test_custom_rating_class():
    class CustomRating(Rating): pass
    assert Elo(CustomRating(1989), rating_class=CustomRating)
    elo = Elo(1989, rating_class=CustomRating)
    assert isinstance(elo.create_rating(1989), CustomRating)


def test_mixed_rating_class():
    class MixedRating(CountedRating, TimedRating):
        pass
    env = Elo(rating_class=MixedRating)
    rating = env.create_rating(1000)
    assert hasattr(rating, 'times')
    assert hasattr(rating, 'rated_at')
    assert rating.times == 0
    assert rating.rated_at is None
    rating = env.rate(rating, [(WIN, 1000)])
    assert rating.times == 1
    assert rating.rated_at is not None


def test_mcleopold_example():
    """The example from `https://github.com/McLeopold/PythonSkills/blob/master
    /skills/testsuite/test_elo.py`_.
    """
    mcleopold = Elo(k_factor=25, initial=1200)
    assert almost(mcleopold.rate_1vs1(1200, 1400), 2) == (1218.99, 1381.01)


def test_uscf():
    """Described in `http://en.wikipedia.org/wiki/Elo_rating_system
    #Most_accurate_K-factor`_.
    """
    uscf = Elo(lambda r: 32 if r < 2100 else 24 if r < 2400 else 16)
    assert uscf.k_factor(2000) == 32
    assert uscf.k_factor(2200) == 24
    assert uscf.k_factor(3000) == 16
    rating = 1613
    series = [(LOSE, 1609), (DRAW, 1477), (WIN, 1388), (WIN, 1586),
              (LOSE, 1720)]
    assert round(uscf.rate(rating, series)) == 1601


def test_fide():
    """Described in `http://en.wikipedia.org/wiki/Elo_rating_system
    #Most_accurate_K-factor`_.
    """
    class FIDERating(CountedRating):
        stable = False
        def __init__(self, value, times=0, stable=None):
            super(FIDERating, self).__init__(value, times)
            if stable is None:
                self.rated(value)
            else:
                self.stable = stable
        @staticmethod
        def is_stable(value):
            return value >= 2400
        def rated(self, value):
            if self.is_stable(value):
                self.stable = True
            return super(FIDERating, self).rated(value)
    def fide_k_factor(rating):
        if rating.times < 30:
            return 30
        elif rating.value < 2400:
            return 15
        return 10
    fide = Elo(fide_k_factor, FIDERating)
    assert fide.k_factor(fide.create_rating(1500, 0)) == 30
    assert fide.k_factor(fide.create_rating(1500, 50)) == 15
    assert fide.k_factor(fide.create_rating(2500, 50)) == 10


def test_zookeeper():
    zookeeper = Elo(lambda r: 32 - math.pi / 2 * r.times, CountedRating)
    assert zookeeper.k_factor(zookeeper.create_rating(1500, 0)) == 32
