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
from rest_framework.response import Response
from rest_framework.views import APIView

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
UserProductLike = get_model('customer','UserProductLike')

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
    context_object_name = "creators"
    template_name = 'customer/creators.html'
    paginate_by = settings.ITEMS_PER_PAGE
    model = Partner
    page_title = _('Followed Creators')
    active_tab = 'creators'

    def get(self, request, *args, **kwargs):
        return super(InfluencerView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        user_followed_creators = UserInfluencerLike.objects.filter(user=self.request.user).values_list('influencer',flat=True)
        qs = Influencers.objects.filter(pk__in=user_followed_creators)

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


class NotificationsSettingsView(PageTitleMixin, generic.TemplateView):
    active_tab = 'notifications'
    template_name = 'customer/notifications/settings.html'


class BrandFollowUnfollowView(APIView):

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated():
            brand_id = kwargs.get('pk')
            try:
                brand = Partner.objects.get(id=brand_id)
                try:
                    follow_obj = UserBrandLike.objects.get(user=request.user,brand=brand)
                    follow_obj.delete()
                    brand.follows = int(brand.follows) - 1
                    brand.save()
                    message = "Brand unfollowed"
                    followed = False
                except:
                    follow_obj = UserBrandLike(user=request.user,brand=brand)
                    follow_obj.save()
                    brand.follows = int(brand.follows) + 1
                    brand.save()
                    message = "Brand followed"
                    followed = True
            except:
                message = "Brand not found"
            respone_dict = {'followed':followed, 'message':message, 'follow_count':brand.follows }
            return Response(respone_dict)
        else:
            return Response({})


class UccFollowUnfollowView(APIView):

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated():
            influencer_id = kwargs.get('pk')
            try:
                influencer = Influencers.objects.get(id=influencer_id)
                try:
                    follow_obj = UserInfluencerLike.objects.get(user=request.user,influencer=influencer)
                    follow_obj.delete()
                    influencer.follows = int(influencer.follows)-1
                    influencer.save()
                    message = "Influencer unfollowed"
                    followed = False
                except:
                    follow_obj = UserInfluencerLike(user=request.user,influencer=influencer)
                    follow_obj.save()
                    influencer.follows = int(influencer.follows)+1
                    influencer.save()
                    message = "Influencer followed"
                    followed = True
            except:
                message = "Influencer not found"
            respone_dict = {'followed':followed, 'message':message, 'follow_count':influencer.follows }
            return Response(respone_dict)
        else:
            return Response({})


class ProductLikeUnlikeView(APIView):

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated():
            product_id = kwargs.get('pk')

            try:
                product = Product.objects.get(pk=product_id)
                try:
                    like_obj = UserProductLike.objects.get(user=request.user,product_like=product)
                    like_obj.delete()
                    product.likes = product.likes - 1
                    product.save()
                    message = "Product disliked"
                    liked = False
                except:
                    like_obj = UserProductLike(user=request.user,product_like=product)
                    like_obj.save()
                    product.likes = product.likes + 1
                    product.save()
                    message = "Product liked"
                    liked = True
            except:
                message = "Product not found"
            respone_dict = {'liked':liked, 'message':message, 'follow_count':product.likes }

            return Response(respone_dict)
        else:
            return Response({})