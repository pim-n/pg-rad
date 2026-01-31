# do not expose internal logger when running mkinit
__ignore__ = ["logger"]

from pg_rad.isotopes import isotope

from pg_rad.isotopes.isotope import (Isotope,)

__all__ = ['Isotope', 'isotope']
