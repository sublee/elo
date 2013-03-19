# -*- coding: utf-8 -*-
import math

from almost import Approximate
from pytest import raises

from elo import *
from elopopulars import *


class almost(Approximate):

    def normalize(self, value):
        if isinstance(value, Rating) and not isinstance(value, float):
            return self.normalize(float(value))
        elif isinstance(value, (list, tuple)):
            try:
                if isinstance(value[0], Rating):
                    # flatten transformed ratings
                    value = tuple(map(float, value))
            except (TypeError, IndexError):
                pass
        return super(almost, self).normalize(value)


def test_rating():
    if type(Rating) is not type:
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


def test_fide():
    """Described in `http://en.wikipedia.org/wiki/Elo_rating_system
    #Most_accurate_K-factor`_.
    """
    # less than 30 games
    assert fide25.k_factor(fide25.create_rating(2500, 0)) == 25
    assert fide25.k_factor(fide25.create_rating(5000, 10)) == 25
    assert fide25.k_factor(fide25.create_rating(1000, 20)) == 25
    # 30 or more games but rating below 2400
    assert fide25.k_factor(fide25.create_rating(2000, 30)) == 15
    assert fide25.k_factor(fide25.create_rating(2399, 31)) == 15
    # reaching rating 2400 (stable=True) and thereafter remains or goes below
    assert fide25.k_factor(fide25.create_rating(3000, stable=True)) == 10
    assert fide25.k_factor(fide25.create_rating(2400, stable=True)) == 10
    assert fide25.k_factor(fide25.create_rating(1200, stable=True)) == 10
    assert fide25.k_factor(fide25.create_rating(800, stable=True)) == 10


def test_uscf():
    """Described in `http://en.wikipedia.org/wiki/Elo_rating_system
    #Most_accurate_K-factor`_.
    """
    assert uscf.k_factor(2000) == 32
    assert uscf.k_factor(2200) == 24
    assert uscf.k_factor(3000) == 16
    rating = 1613
    series = [(LOSS, 1609), (DRAW, 1477), (WIN, 1388), (WIN, 1586),
              (LOSS, 1720)]
    assert round(uscf.rate(rating, series)) == 1601


def test_mcleopold():
    """The example from `https://github.com/McLeopold/PythonSkills/blob/master
    /skills/testsuite/test_elo.py`_.
    """
    mcleopold = Elo(k_factor=25, initial=1200)
    assert almost(mcleopold.quality_1vs1(1200, 1400)) == 0.4805
    assert almost(mcleopold.rate_1vs1(1200, 1400), 2) == (1218.99, 1381.01)


def test_zookeeper():
    zookeeper = Elo(lambda r: 32 - math.pi / 2 * r.times, CountedRating)
    assert zookeeper.k_factor(zookeeper.create_rating(1500, 0)) == 32


def test_moserware():
    """The test cases is from `https://github.com/moserware/Skills`_."""
    f25 = fide25
    # FideProvisionalEloCalculatorTests
    assert almost(f25.rate_1vs1(1200, 1500), 1) == (1221.3, 1478.8)
    assert almost(f25.rate_1vs1(1500, 1200), 1) == (1503.8, 1196.3)
    assert almost(f25.rate_1vs1(1200, 1500, drawn=True), 1) == (1208.8, 1491.3)
    # FideNonProvisionalEloCalculatorTests
    _1200 = f25.create_rating(1200, 30)  # k = 15
    _2500 = f25.create_rating(2500, stable=True)  # k = 10
    _2600 = f25.create_rating(2600, stable=True)  # k = 10
    assert almost(f25.rate_1vs1(_1200, _1200)) == (1207.5, 1192.5)
    assert almost(f25.rate_1vs1(_1200, _1200, drawn=True)) == (1200, 1200)
    assert almost(f25.rate_1vs1(_2600, _2500)) == (2603.6, 2496.4)
    assert almost(f25.rate_1vs1(_2500, _2600)) == (2506.4, 2593.6)
    assert almost(f25.rate_1vs1(_2600, _2500, drawn=True)) == (2598.6, 2501.4)


def test_based_multiplayer_elo_calculator():
    """The expectation is from `http://elo.divergentinformatics.com/`_."""
    elo = Elo(10)
    # 1 vs 1
    r1 = 1200
    r2 = 800
    assert almost(elo.expect(r1, r2)) == 0.909091
    assert almost(elo.expect(r2, r1)) == 0.090909
    assert almost(elo.rate_1vs1(r2, r1)) == (809.091, 1190.909)
    # 1 vs 1 vs 1
    r1 = 1500
    r2 = 1000
    r3 = 2000
    assert almost(rate(r1, [(WIN, r2), (WIN, r3)])) == 1510.000
    assert almost(rate(r2, [(LOSS, r1), (WIN, r3)])) == 1009.436
    assert almost(rate(r3, [(LOSS, r1), (LOSS, r2)])) == 1980.564
    # 1 vs 1 on FIDE (25, 15 & 10)
    r1 = fide25.create_rating(1200, 0)
    r2 = fide25.create_rating(800, 0)
    assert fide25.k_factor(r1) == 25
    assert fide25.k_factor(r2) == 25
    assert almost(map(float, fide25.rate_1vs1(r2, r1))) == (822.727, 1177.273)
    # stabled 1 vs 1 on FIDE (25, 15 & 10)
    r1 = fide25.create_rating(1200, 40)
    r2 = fide25.create_rating(800, 40)
    assert fide25.k_factor(r1) == 15
    assert fide25.k_factor(r2) == 15
    assert almost(map(float, fide25.rate_1vs1(r2, r1))) == (813.636, 1186.364)
