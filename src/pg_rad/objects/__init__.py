# do not expose internal logger when running mkinit
__ignore__ = ["logger"]

from pg_rad.objects import detectors
from pg_rad.objects import objects
from pg_rad.objects import sources

from pg_rad.objects.detectors import (Detector,)
from pg_rad.objects.objects import (BaseObject,)
from pg_rad.objects.sources import (PointSource,)

__all__ = ['BaseObject', 'Detector', 'PointSource', 'detectors', 'objects',
           'sources']
