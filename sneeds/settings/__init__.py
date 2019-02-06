from .base import *

try:
    from .local import *

    print("Running local")

except:
    from .production import *

    print("Running production")
