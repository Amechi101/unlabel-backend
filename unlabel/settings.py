from unlabel.base_settings import *

PRODUCTION = True

if PRODUCTION == True:
    from unlabel.production_settings import *
else:
    from unlabel.local_settings import *


