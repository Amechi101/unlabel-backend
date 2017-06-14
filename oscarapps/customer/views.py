from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from oscar.apps.customer.utils import get_password_reset_url,Dispatcher
from oscar.core.compat import get_user_model, user_is_authenticated
from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)
from oscar.core.utils import safe_referrer
from oscar.views.generic import PostActionMixin

PageTitleMixin, RegisterUserMixin = get_classes(
    'customer.mixins', ['PageTitleMixin', 'RegisterUserMixin'])

UserBrandLike = get_class('customer.models','UserBrandLike')
Partner = get_class('partner.models','Partner')


class BrandView(PageTitleMixin, generic.ListView):
    """
    Customer order history
    """
    context_object_name = "brands"
    template_name = 'customer/brands.html'
    paginate_by = settings.OSCAR_ORDERS_PER_PAGE
    model = Partner
    page_title = _('Brand Follows')
    active_tab = 'brands'

    def get(self, request, *args, **kwargs):

        return super(BrandView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user_followed_brands = UserBrandLike.objects.filter(user=self.request.user).values_list('brand',flat=True)
        qs = self.model._default_manager.filter(pk__in=user_followed_brands)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super(BrandView, self).get_context_data(*args, **kwargs)
        return ctx



class BrandUnfollowView(generic.View):


    model = UserBrandLike
    template_name = 'customer/brands.html'
    active_tab = 'brands'
    context_object_name = 'brand'
    success_url = reverse_lazy('customer:followed-brands')

    def get(self,request,*args,**kwargs):
        brand_id = kwargs.get('pk')
        try:
            brand = Partner.objects.get(id=brand_id)
        except:
            self.message = "Brand not found"
        try:
            follow_obj = UserBrandLike.objects.get(user=request.user,brand=brand)
            follow_obj.delete()
        except:
            self.message = "Brand not found"
            return HttpResponseRedirect(reverse('followed-brands'))
        self.message = "Brand "+ brand.name +" Unfollowed"
        user_followed_brands = UserBrandLike.objects.filter(user=self.request.user).values_list('brand',flat=True)
        qs = self.model._default_manager.filter(pk__in=user_followed_brands)
        messages.success(self.request,self.message )
        return HttpResponseRedirect(reverse('customer:followed-brands'))



    # def get_queryset(self):
    #     user_followed_brands = UserBrandLike.objects.filter(user=self.request.user).values_list('brand',flat=True)
    #     qs = self.model._default_manager.filter(pk__in=user_followed_brands)
    #     return qs
    #
    # def get_success_url(self):
    #     messages.success(self.request,
    #                      _("Address '%s' deleted") % self.object.summary)
    #     return super(BrandUnfollowView, self).get_success_url()



    # model = UserBrandLike
    # template_name = 'customer/brands.html'
    # active_tab = 'brands'
    # context_object_name = 'brand'
    # # success_url = reverse_lazy('customer:followed-brands')
    #
    # def get(self, request, *args, **kwargs):
    #     brand_id = kwargs.get('pk')
    #     try:
    #         brand = Partner.objects.get(id=brand_id)
    #     except:
    #         self.message = "Brand not found"
    #     follow_obj = UserBrandLike.objects.get(user=request.user,brand=brand)
    #     follow_obj.delete()
    #     self.message = "Brand "+ brand.name +" Unfollowed"
    #     return super(BrandUnfollowView, self).get(request, *args, **kwargs)
    #
    # def get_queryset(self):
    #     user_followed_brands = UserBrandLike.objects.filter(user=self.request.user).values_list('brand',flat=True)
    #     qs = self.model._default_manager.filter(pk__in=user_followed_brands)
    #     return qs
    #
    # def get_success_url(self):
    #     messages.success(self.request,
    #                      _("brand '%s' unfollowed") % self.object.summary)
    #     return super(BrandUnfollowView, self).get_success_url()

