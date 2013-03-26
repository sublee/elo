Elo
===

the classic rating system

.. currentmodule:: elo

What's Elo?
~~~~~~~~~~~

Elo_ is the most famous rating system among game players. It was invented by
`Arpad Elo`_ for chess tournaments of USCF_. ::

   from elo import Rating, quality_1vs1, rate_1vs1
   alice, bob = Rating(1000), Rating(1400)  # assign Alice and Bob's ratings
   if quality_1vs1(alice, bob) < 0.50:
       print('This match seems to be not so fair')
   alice, bob = rate_1vs1(alice, bob)  # update the ratings after the match

.. _Elo: http://en.wikipedia.org/wiki/Elo_rating_system
.. _Arpad Elo: http://en.wikipedia.org/wiki/Arpad_Elo
.. _USCF: http://www.uschess.org/

Learning
~~~~~~~~

K-factor and rating extra data
------------------------------

Installing
~~~~~~~~~~

The package is available in `PyPI <http://pypi.python.org/pypi/elo>`_. To
install it in your system, use :command:`easy_install`:

.. sourcecode:: bash

   $ easy_install elo

Or check out developement version:

.. sourcecode:: bash

   $ git clone git://github.com/sublee/elo.git

API
~~~

.. autoclass:: Elo
   :members:

.. autoclass:: Rating
   :members:

.. autoclass:: CountedRating
   :members:

.. autoclass:: TimedRating
   :members:

Licensing and Author
~~~~~~~~~~~~~~~~~~~~

This project is licensed under BSD_. See LICENSE_ for the details.

I'm `Heungsub Lee`_, a game developer. I've also owned `the Python TrueSkill
project <http://trueskill.org/>`_. Any regarding questions or patches are
welcomed.

.. _BSD: http://en.wikipedia.org/wiki/BSD_licenses
.. _LICENSE: https://github.com/sublee/elo/blob/master/LICENSE
.. _Heungsub Lee: http://subl.ee/
