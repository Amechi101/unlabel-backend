from django.conf.urls import include, url,patterns
from rest_framework import routers
from .customer import views as customerViews
from .address import views as addressViews
from .catalogue import views as catalogueViews
from .influencer import views as influencerViews
from .utils import *


#####   customer urls   #####
urlpatterns = [

    url(r'testing_pushnotes/',
        customerViews.PushNotificationView.as_view(), name='push_notes'),
    url(r'testing_djangopush/',
        customerViews.DjangoPush().as_view(), name='django-push_notes'),
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
    url(r'^partner_follow/', catalogueViews.PartnerFollowView.as_view(),
        name='Partner_follow_view'),
    url(r'^influencer_reserve_product/',catalogueViews.InfluencerReserveProduct.as_view(),
        name='influencer_product_reserve'),
    url(r'^login/$', influencerViews.LoginView.as_view(), name='influencer-login'),
    url(r'^influencer_followed_partners/$',influencerViews.InfluencerFollowedBrands.as_view(),
        name='influencer_followed_brands'),
    url(r'^influencer_profile_update/$',influencerViews.InfluencerProfileUpdate.as_view(),
        name='influencer_profile_update'),
    url(r'^influencer_image_bio/',influencerViews.InfluencerPicAndBio.as_view(),name='influencer_image_bio'),
    url(r'^influencer_reserved_products/$',catalogueViews.InfluencerReservedProducts.as_view(),
        name='influencer_reserved_products'),
    url(r'^influencer_rented_products/$',catalogueViews.InfluencerRentedProducts.as_view(),
        name='influencer_rented_products'),
    url(r'^influencer_live_products/$',catalogueViews.InfluencerLiveProducts.as_view(),
        name='influencer_live_products'),
    url(r'^influencer_add_product_images/$',catalogueViews.InfluencerProductImagesView.as_view(),
        name='influencer_add_product_images'),
    url(r'^influencer_add_product_note/$',catalogueViews.InfluencerProductNote.as_view(),
        name='influencer_add_product_note'),
    url(r'^influencer_product_list/',
        catalogueViews.InfluencerBaseProductListView.as_view(),name='influencer_product_list_view'),
    url(r'^influencer_product_variants/$',catalogueViews.InfluencerChildProductsListView.as_view(),
        name='influencer_product_variants'),
    url(r'^influencer_product_go_live/$',catalogueViews.InfluencerProductGoLive.as_view(),
        name='influencer_product_go live'),
    url(r'^influencer_remove_product_image/$',catalogueViews.InfluencerRemoveProductImage.as_view(),
        name='influencer_remove product_images' ),
    url(r'^influencer_physical_attributes/$',influencerViews.PhysicalAttributesUpdate.as_view(),
        name='influencer_physical_attributes_serializer'),
    url(r'^influencer_profile_details/$',influencerViews.InfluencerProfileDetails.as_view(),
        name='Influencer_Profile_Details'),
    url(r'^influencer_brand_categories/$',catalogueViews.InfluencerBrandCategories.as_view(),
        name='influencer_brand_categories'),
    url(r'^influencer_brand_styles/$',catalogueViews.InfluencerBrandStyles.as_view(),
        name='influencer_brand_styles'),
    url(r'^influencer_brand_locations/$',addressViews.InfluencerBrandLocations.as_view(),
        name='influencer_brand_locations'),
    url(r'^influencer_current_locations/$',influencerViews.InfluencerCurrentLocationView.as_view(),
        name='influencer_current_locations'),
    url(r'^influencer_change_password/$',influencerViews.InfluencerChangePassword.as_view(),
        name='influencer_change_password'),
    # url(r'^get_influencer_device_id/$',influencerViews.InfluencerDeviceId.as_view(),
    #     name='get_influencer_device_id'),

]

##### address urls  #####

urlpatterns = urlpatterns + [
    url(r'add_address/',addressViews.AddAddressView.as_view(),name='add_address_view'),
]

#### front end requests
urlpatterns = urlpatterns + [
    url(r'get_countries',addressViews.GetCountriesView.as_view(), name='get_countries'),
    url(r'get_states',addressViews.GetStatesView.as_view(), name='get_countries'),
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