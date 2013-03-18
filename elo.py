# -*- coding: utf-8 -*-
"""
    elo
    ~~~

    The Elo rating system.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from abc import ABCMeta
from datetime import datetime


__version__  = '0.1.dev'
#__all__ = ['Elo',


#: The actual score for win
WIN = 1.
#: The actual score for draw
DRAW = 0.5
#: The actual score for lose
LOSE = 0.

#: Default K-factor
K_FACTOR = 10
#: Default rating class
RATING_CLASS = float
#: Default initial rating
INITIAL = 1500
#: Default Beta value
BETA = 200


class Rating(object):

    __metaclass__ = ABCMeta

    value = None

    def __init__(self, value):
        self.value = value

    def rated(self, value):
        self.value = value
        return self

    def before_rate(self):
        pass

    def after_rated(self):
        pass

    def __int__(self):
        """Type-casting to ``int``."""
        return int(self.value)

    def __float__(self):
        """Type-casting to ``float``."""
        return float(self.value)

    def __nonzero__(self):
        """Type-casting to ``bool``."""
        return bool(int(self))

    # Python 3 accepts __bool__ instead of __nonzero__
    __bool__ = __nonzero__

    def __eq__(self, other):
        return float(self) == float(other)

    def __lt__(self, other):
        """Is Rating < number.

        :param other: the operand
        :type other: number
        """
        return self.value < other

    def __le__(self, other):
        """Is Rating <= number.

        :param other: the operand
        :type other: number
        """
        return self.value <= other

    def __gt__(self, other):
        """Is Rating > number.

        :param other: the operand
        :type other: number
        """
        return self.value > other

    def __ge__(self, other):
        """Is Rating >= number.

        :param other: the operand
        :type other: number
        """
        return self.value >= other

    def __iadd__(self, other):
        """Rating += number.

        :param other: the operand
        :type other: number
        """
        self.value += other
        return self

    def __isub__(self, other):
        """Rating -= number.

        :param other: the operand
        :type other: number
        """
        self.value -= other
        return self


class CountedRating(Rating):

    times = None

    def __init__(self, value, times=0):
        self.times = times
        super(CountedRating, self).__init__(value)

    def rated(self, value):
        self.times += 1
        return super(CountedRating, self).rated(value)

    def copy(self, value):
        return type(self)(value, self.rated)

    def after_rated(self):
        self.rated += 1
        super(CountedRating, self).after_rated()


class TimedRating(Rating):

    rated_at = None

    def __init__(self, value, rated_at=None):
        self.rated_at = rated_at
        super(TimedRating, self).__init__(value)

    def rated(self, value):
        self.rated_at = datetime.utcnow()
        return super(TimedRating, self).rated(value)


Rating.register(float)


class Elo(object):

    def __init__(self, k_factor=K_FACTOR, rating_class=RATING_CLASS,
                 initial=INITIAL, beta=BETA):
        self.k_factor = k_factor
        self.rating_class = rating_class
        self.initial = initial
        self.beta = beta

    def expect(self, rating, other_rating):
        """The "E" function in Elo. It calculates the expected score of the
        first rating by the second rating.
        """
        # http://www.chess-mind.com/en/elo-system
        diff = float(other_rating) - float(rating)
        f_factor = 2 * self.beta  # rating disparity
        return 1. / (1 + 10 ** (diff / f_factor))

    def adjust(self, rating, series):
        """Calculates the adjustment value."""
        return sum(score - self.expect(rating, other_rating)
                   for score, other_rating in series)

    def rate(self, rating, series):
        """Calculates new ratings by the game result series."""
        rating = self.ensure_rating(rating)
        k = self.k_factor(rating) if callable(self.k_factor) else self.k_factor
        new_rating = float(rating) + k * self.adjust(rating, series)
        if hasattr(rating, 'rated'):
            new_rating = rating.rated(new_rating)
        return new_rating

    def adjust_1vs1(self, rating1, rating2, drawn=False):
        return self.adjust(rating1, [(DRAW if drawn else WIN, rating2)])

    def rate_1vs1(self, rating1, rating2, drawn=False):
        scores = (DRAW, DRAW) if drawn else (WIN, LOSE)
        return (self.rate(rating1, [(scores[0], rating2)]),
                self.rate(rating2, [(scores[1], rating1)]))

    def quality_1vs1(self, rating1, rating2):
        return 2 * (0.5 - abs(0.5 - self.expect(rating1, rating2)))

    def create_rating(self, value=None, *args, **kwargs):
        if value is None:
            value = self.initial
        return self.rating_class(value, *args, **kwargs)

    def ensure_rating(self, rating):
        if isinstance(rating, self.rating_class):
            return rating
        return self.rating_class(rating)


def adjust(rating, series):
    return global_env().adjust(rating, series)


def rate(rating, series):
    return global_env().rate(rating, series)


def adjust_1vs1(rating1, rating2, drawn=False):
    return global_env().adjust_1vs1(rating1, rating2, drawn)


def rate_1vs1(rating1, rating2, drawn=False):
    return global_env().rate_1vs1(rating1, rating2, drawn)


def setup(k_factor=K_FACTOR, rating_class=RATING_CLASS,
          initial=INITIAL, beta=BETA, env=None):
    if env is None:
        env = Elo(k_factor, rating_class, initial, beta)
    global_env.__elo__ = env
    return env


def global_env():
    """Gets the global Elo environment."""
    try:
        global_env.__elo__
    except AttributeError:
        # setup the default environment
        setup()
    return global_env.__elo__
