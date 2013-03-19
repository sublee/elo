# -*- coding: utf-8 -*-
from elo import CountedRating, Elo


__all__ = ['fide30', 'fide25', 'fide', 'uscf']


class FIDERating(CountedRating):

    stable = False

    def __init__(self, value=None, times=0, stable=None):
        if stable is not None:
            self.stable = stable
            if stable:
                times = max(30, times)
        super(FIDERating, self).__init__(value, times)
        if stable is None:
            self.stable = self._should_stable()

    def _should_stable(self):
        return self.times >= 30 and self.value >= 2400

    def rated(self, value):
        rated = super(FIDERating, self).rated(value)
        if rated._should_stable():
            rated.stable = True
        return rated


def make_fide_k_factor(scarce_games, too_low_rating, stabled):
    def fide_k_factor(rating):
        if rating.times < 30:
            return scarce_games
        elif rating.stable:
            assert rating.times >= 30
            return stabled
        assert rating < 2400
        assert rating.times >= 30
        return too_low_rating
    return fide_k_factor


#: The new FIDE rating regulations which using 30, 15 & 10 K-factor. FIDE is
#: using this `since July 1, 2011 <http://www.fide.com/component/content/
#: article/1-fide-news/5421-changes-to-rating-regulations.html>`_.
fide30 = Elo(make_fide_k_factor(30, 15, 10), FIDERating)

#: The old FIDE rating regulations which using 25, 15 & 10 K-factor.
fide25 = Elo(make_fide_k_factor(25, 15, 10), FIDERating)

#: The shortcut to :data:`fide30`.
fide = fide30

#: The USCF rating regulations. The initial rating is 1300 but USCF defined
#: more complex rule. See `the paper <http://www.glicko.net/ratings/
#: rating.system.pdf>`_ of Prof. Mark E. Glickman.
uscf = Elo(lambda r: 32 if r < 2100 else 24 if r < 2400 else 16, initial=1300)
