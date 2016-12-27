from unlabel.base_settings import *

PRODUCTION = False

if PRODUCTION == True:
    from unlabel.production_settings import *
else:
    from unlabel.local_settings import *


