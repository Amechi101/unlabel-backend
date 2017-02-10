from django.conf.urls import include, url,patterns
from rest_framework import routers
from .customer import views as customerViews
from .address import views as addressViews
from .catalogue import views as catalogueViews
from .influencer import views as influencerViews
from .utils import *


#####   customer urls   #####
urlpatterns = [

    ###-------customer apis
    url(r'customer_register/',
        customerViews.CustomerRegisterView.as_view(),name='register_view'),

    url(r'customer_update_password/',
        customerViews.CustomerPasswordUpdateView.as_view(), name='password_update_view'),

    url(r'customer_forgot_password/',
        customerViews.CustomerForgotPassword.as_view(),name='customer_forgot_password_view'),

    url(r'customer_profile_update/',
        customerViews.CustomerProfileUpdateView.as_view(),name='customer_profile_update_view'),

    # url(r'^rest-auth/facebook/$',
    #     customerViews.FacebookLogin.as_view(), name='fb_login'),

    url(r'^customer_profile_deactivate/$',
        customerViews.CustomerProfileDeleteView.as_view(),name='customer_profile_delete_view'),

    ###-----product apis
    url(r'^product_list/',
        catalogueViews.ProductListView.as_view(),name='product_list_view'),

    url(r'^product_like/(?P<prod_id>[0-9]+)/',
        catalogueViews.ProductLikeView.as_view(),name='Product_like_view'),



    url(r'^partnerList/',catalogueViews.BrandListView.as_view(),name='brand_List_view'),

    url(r'^storeTypeList/',catalogueViews.StoreListView.as_view(),name='store_list_view'),


    ###-----Influencer APIS
    url(r'^influencer_forgot_password/',
        influencerViews.InfluencerForgotPassword.as_view(),name='influencer_forgot_password_view'),

    url(r'^Influencer_partnerList/',catalogueViews.InfluencerBrandListView.as_view(),name='influencer_brand_list_view'),


    url(r'^partner_follow/(?P<partner_id>[0-9]+)/', catalogueViews.PartnerFollowView.as_view(),name='Partner_follow_view'),

    url(r'^influencer_reserve_product/(?P<product_id>[0-9]+)/',catalogueViews.InfluencerReserveProduct.as_view(), name='influencer_product_reserve'),

    url(r'^influencer_product_list/',
        catalogueViews.InfluencerProductListView.as_view(),name='influencer_product_list_view'),

    url(r'^login/$', influencerViews.LoginView.as_view(), name='influencer-login'),

    url(r'^influencer_followed_partners/$',influencerViews.InfluencerFollowedBrands.as_view(),name='influencer_followed_brands'),

    url(r'^influencer_profile_update/$',influencerViews.InfluencerProfileUpdate,name='influencer_profile_update'),

    # url(r'influencer_live_products/')


]

##### address urls  #####

urlpatterns = urlpatterns + [

    url(r'add_address/',addressViews.AddAddressView.as_view(),name='add_address_view'),
]


#### front end requests

urlpatterns = urlpatterns + [
    url(r'get_states',addressViews.GetStatesView.as_view(),name='get_states')
]



urlpatterns = urlpatterns + patterns(
                'django.contrib.auth.views',
                url(r'^password-reset-done/$', 'password_reset_done',
                   {'template_name': 'profiles/password_reset_done.html',},name='password-reset-done'),
                url(r'^password/reset/confirm/(?P<uidb36>[0-9a-zA-Z]{1,13})-(?P<token>.+)/$',
                   'password_reset_confirm',
                   {'template_name': 'profiles/password_reset_confirm.html',},
                   name='password-reset-confirm'),
                url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                   'password_reset_confirm',{'template_name': 'accounts/password_reset_confirm.html',},
                   name='password_reset_confirm'),
                url(r'^password-reset-complete', 'password_reset_complete', {
                   'template_name': 'accounts/password_reset_complete.html',
                   }, name='password_reset_complete'),
               )