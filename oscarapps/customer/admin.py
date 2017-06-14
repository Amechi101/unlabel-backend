from oscar.apps.customer.admin import *  # noqa
from .models import UserProductLike,UserBrandLike,UserInfluencerLike


admin.site.register(UserProductLike)
admin.site.register(UserBrandLike)
admin.site.register(UserInfluencerLike)