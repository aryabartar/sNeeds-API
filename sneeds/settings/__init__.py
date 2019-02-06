# from .base import *


try:
    print("Running local")
    from .local import *
except:
    print("Running production")
    from .production import *

