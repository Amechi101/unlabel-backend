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
from oscar.apps.customer.views import ChangePasswordView as CoreChangePasswordView
from oscar.apps.customer.views import AddressCreateView as CoreAddressCreateView


PageTitleMixin, RegisterUserMixin = get_classes(
    'customer.mixins', ['PageTitleMixin', 'RegisterUserMixin'])

UserBrandLike = get_model('customer','UserBrandLike')
UserInfluencerLike = get_model('customer','UserInfluencerLike')
Partner = get_model('partner','Partner')
Influencers = get_model('influencers','Influencers')
Product = get_model('catalogue','Product')
UserProductLike = get_model('customer','UserProductLike')
Bankcard = get_model('payment','Bankcard')

class BrandView(PageTitleMixin, generic.ListView):
    """
    My account followed brands view
    """
    context_object_name = "brands"
    template_name = 'customer/brands.html'
    paginate_by = settings.ITEMS_PER_PAGE
    model = Partner
    page_title = _('Followed Brands')
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
    """
    My account followed brands delete view
    """

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
            return HttpResponseRedirect(reverse('customer:followed-brands'))
        self.message = "Brand "+ brand.name +" Unfollowed"
        messages.success(self.request,self.message )
        return HttpResponseRedirect(reverse('customer:followed-brands'))


class InfluencerView(PageTitleMixin, generic.ListView):

    def get(self, request, *args, **kwargs):
        return super(InfluencerView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user_followed_creators = UserInfluencerLike.objects.filter(user=self.request.user).values_list('influencer',flat=True)
        qs = self.model._default_manager.filter(pk__in=user_followed_creators)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super(InfluencerView, self).get_context_data(*args, **kwargs)
        return ctx



class InfluencerUnfollowView(generic.View):

    def get(self,request,*args,**kwargs):
        brand_id = kwargs.get('pk')
        try:
            influencer = Influencers.objects.get(id=brand_id)
        except:
            self.message = "Influencer not found"
        try:
            follow_obj = UserInfluencerLike.objects.get(user=request.user,influencer=influencer)
            follow_obj.delete()
        except:
            self.message = "Influencer not found"
            return HttpResponseRedirect(reverse('customer:followed-creators'))
        self.message = "Influencer "+ influencer.users.get_full_name() +" Unfollowed"
        messages.success(self.request,self.message )
        return HttpResponseRedirect(reverse('customer:followed-creators'))


class ProductsView(PageTitleMixin, generic.ListView):
    """
    Customer order history
    """
    context_object_name = "products"
    template_name = 'customer/products.html'
    paginate_by = settings.ITEMS_PER_PAGE
    model = Product
    page_title = _('Liked Products')
    active_tab = 'products'

    def get(self, request, *args, **kwargs):

        return super(ProductsView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user_followed_brands = UserProductLike.objects.filter(user=self.request.user).values_list('product_like',flat=True)
        qs = self.model._default_manager.filter(pk__in=user_followed_brands)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProductsView, self).get_context_data(*args, **kwargs)
        return ctx


class ChangePasswordView(CoreChangePasswordView):
    active_tab = 'password'



class BankcardView(PageTitleMixin, generic.ListView):
    context_object_name = "bankcards"
    template_name = 'customer/profile/payments.html'
    paginate_by = settings.ITEMS_PER_PAGE
    model = Bankcard
    page_title = _('My payments')
    active_tab = 'payments'

    def get(self, request, *args, **kwargs):
        return super(BankcardView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model._default_manager.filter(user=self.request.user)

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super(BankcardView, self).get_context_data(*args, **kwargs)
        return ctx


class BankcardDeleteView(PageTitleMixin, generic.View):

    def get(self,request,*args,**kwargs):
        card_id = kwargs.get('pk')
        try:
            bankcard = Bankcard.objects.get(id=card_id)
            bankcard.delete()
        except:
            self.message = "Bankcard not found"
            return HttpResponseRedirect(reverse('customer:my-payments'))
        self.message = "Bankcard Deleted."
        messages.success(self.request,self.message )
        return HttpResponseRedirect(reverse('customer:my-payments'))



