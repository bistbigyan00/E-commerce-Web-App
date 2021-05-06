from .base import *

from .production import *

#if any error in local, do not run the file
try:
    from .local import *
except:
    pass
