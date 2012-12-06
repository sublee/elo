# -*- coding: utf-8 -*-
"""
    elo
    ~~~

    The Elo rating system.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
__version__  = '0.1.dev'
#__all__ = ['Elo', 'transform_ratings', 'match_quality',
#           'calc_draw_probability', 'calc_draw_margin', 'setup',
#           'MU', 'SIGMA', 'BETA', 'TAU', 'DRAW_PROBABILITY']

#: The actual score for win
WIN = 1.
#: The actual score for draw
DRAW = 0.5
#: The actual score for lose
LOSE = 0.

#: Default initial rating
INITIAL = 1500
#: Default K-factor
K_FACTOR = 10
#: The USCF has staggered the K-factor according to three main rating ranges
#: of:
#:
#: - Players below 2100 -> K-factor of 32 used.
#: - Players between 2100 and 2400 -> K-factor of 24 used.
#: - Players above 2400 -> K-factor of 16 used.
USCF_K_FACTOR = lambda r: 32 if r < 2100 else 24 if r < 2400 else 16


def expect(rating, other_rating):
    """The "E" function in Elo. It calculates the expected score of the first
    rating by the second rating.
    """
    return 1. / (1 + 10 ** ((other_rating - rating) / 400.))


def adjust(rating, series):
    """Calculates the adjustment value."""
    return sum(score - expect(rating, other_rating)
               for score, other_rating in series)


def rate(rating, series, k_factor=K_FACTOR):
    """Calculates new ratings by the game result series."""
    k = k_factor(rating) if callable(k_factor) else k_factor
    return rating + k * adjust(rating, series)


def rate_1vs1(rating1, rating2, drawn=False, k_factor=K_FACTOR):
    scores = (DRAW, DRAW) if drawn else (WIN, LOSE)
    return (rate(rating1, [(scores[0], rating2)], k_factor),
            rate(rating2, [(scores[1], rating1)], k_factor))


def quality_1vs1(rating1, rating2):
    return 2 * (0.5 - abs(0.5 - expect_score(rating1, rating2)))
