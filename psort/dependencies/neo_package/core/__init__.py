# -*- coding: utf-8 -*-
"""
:mod:`neo.core` provides classes for storing common electrophysiological data
types.  Some of these classes contain raw data, such as spike trains or
analog signals, while others are containers to organize other classes
(including both data classes and other container classes).

Classes from :mod:`neo.io` return nested data structures containing one
or more class from this module.

Classes:

.. autoclass:: Block
.. autoclass:: Segment
.. autoclass:: ChannelIndex
.. autoclass:: Unit

.. autoclass:: AnalogSignal
.. autoclass:: IrregularlySampledSignal

.. autoclass:: Event
.. autoclass:: Epoch

.. autoclass:: SpikeTrain
.. autoclass:: ImageSequence

.. autoclass:: RectangularRegionOfInterest
.. autoclass:: CircularRegionOfInterest
.. autoclass:: PolygonRegionOfInterest

"""

# needed for python 3 compatibility
from __future__ import absolute_import, division, print_function

from .block import Block
from .segment import Segment
from .channelindex import ChannelIndex
from .unit import Unit

from .analogsignal import AnalogSignal
from .irregularlysampledsignal import IrregularlySampledSignal

from .event import Event
from .epoch import Epoch

from .spiketrain import SpikeTrain

from .imagesequence import ImageSequence
from .regionofinterest import RectangularRegionOfInterest, CircularRegionOfInterest, PolygonRegionOfInterest

# Block should always be first in this list
objectlist = [Block, Segment, ChannelIndex,
              AnalogSignal, IrregularlySampledSignal,
              Event, Epoch, Unit, SpikeTrain, ImageSequence,
              RectangularRegionOfInterest, CircularRegionOfInterest,
              PolygonRegionOfInterest]

objectnames = [ob.__name__ for ob in objectlist]
class_by_name = dict(zip(objectnames, objectlist))
