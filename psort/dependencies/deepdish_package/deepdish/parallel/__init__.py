from __future__ import print_function, division, absolute_import

try:
    import mpi4py
    from .mpi import *
except ImportError:
    from .fallback import *

__all__ = ['rank', 'imap_unordered', 'imap',
           'starmap_unordered', 'starmap', 'main']
