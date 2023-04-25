# Elo, the classic rating system

by [Heungsub Lee](http://subl.ee/)

Elo is a rating system used in many games such as chess
and was originally developed by [Arpad Elo](https://en.wikipedia.org/wiki/Arpad_Elo).

This project is a Python implementation of Elo:

    import elo

    env = elo.Elo()
    alice = env.create_rating()
    bob = env.create_rating()

    # Update Alice & Bob's ratings (winner is first)
    alice, bob = env.rate_1vs1(alice, bob)


See the related [Trueskill](https://trueskill.org/) module.


## Installation

The package is available in [PyPI](https://pypi.org/project/elo/):

    pip install elo


## Usage

The default values are sensible for many games, but they can be customized.

    import elo

    # Larger K factors are more sensitive to recent events
    # Smaller Ks respond slowly to changes in player skill
    env = elo.Elo(initial=1200.0, k_factor=10)

For an example with a variable K factor based on the games played,
see `elopopulars.py`.


### Handling draws

In Elo, draws still update each player's ratings:

    alice, bob = env.rate_1vs1(alice, bob, drawn=True)


### Expected win probability

Given two ratings, the expected win percentage can be inferred.
A player with a 200 rating advantage is expected to ~76% of the time.
With a 100 rating advantage, a player should win ~64% of the time.
These percentages ignore the chances of draws.

    alice = env.create_rating(1400)
    bob = env.create_rating()  # 1200 by default
    env.expect(alice, bob)  # 0.7597
