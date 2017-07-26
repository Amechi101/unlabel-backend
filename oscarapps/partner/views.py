import datetime

from oscarapps.address.models import Locations
from oscarapps.partner.forms import PartnerSignUpForm
from oscarapps.partner.models import PartnerInvite, Partner
from oscarapps.catalogue.models import Product
from users.models import User
from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)
from oscar.core.compat import get_user_model, user_is_authenticated

from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import utc
from django.views.generic import View, ListView
from django.conf import settings

UserBrandLike = get_model('customer','UserBrandLike')


class PartnerSignUpView(View):
    """
        View for Partner Signup
    """
    def get(self, request, code, *args, **kwargs):
        try:
            partner_invite = PartnerInvite.objects.get(code=code)
        except:
            return HttpResponse("sorry link is used already")
        brands_list = Partner.objects.all().order_by('-created')[:3]
        context = {'brands':brands_list,'user_form': PartnerSignUpForm}
        return render(request, 'common/partner_register.html', context)

    def post(self, request, code, *args, **kwargs):

        partner_form = PartnerSignUpForm(data=request.POST)

        # try:
        partner_invite = PartnerInvite.objects.get(code=code)
        check_date = datetime.datetime.utcnow().replace(tzinfo=utc)
        sent_date = partner_invite.date_sent
        if (((check_date - sent_date).total_seconds())/60)/60 < 24 and partner_invite.is_used == False:
                if partner_form.is_valid():
                    partner_user = User()
                    partner_user.email = partner_form.cleaned_data['email']
                    partner_user.first_name = partner_form.cleaned_data['first_name']
                    partner_user.last_name = partner_form.cleaned_data['last_name']
                    partner_user.is_influencer = False
                    partner_user.is_brand = True
                    partner_user.contact_number = partner_form.cleaned_data['contact_number']
                    partner_user.gender = partner_form.cleaned_data['gender']
                    partner_user.save()
                    partner_user.set_password(partner_form.cleaned_data['password1'])
                    partner_user.save()

                    dashboard_access_perm = Permission.objects.get(
                        codename='dashboard_access', content_type__app_label='partner')
                    partner_user.user_permissions.add(dashboard_access_perm)
                    partner_user.save()
                    location = str(partner_form['loc'].value()).split(', ')
                    city = ", ".join(str(x) for x in location[:-2])
                    state = str(location[-2:-1][0])
                    if str(location[-1:][0]) == "United States":
                        country = "USA"
                    else:
                        country = str(location[-1:][0])
                    partner_location = Locations.objects.create(city=city,
                                                                state=state,
                                                                country=country,
                                                                is_brand_location=True,
                                                                )
                    partner_location.save()
                    partner_brand = Partner()
                    partner_brand.name = partner_form.cleaned_data['name']
                    email = partner_form.cleaned_data['email']
                    partner_user = User.objects.get(email=email)
                    partner_brand.save()
                    partner_brand.users.add(partner_user)
                    partner_brand.name = partner_form.cleaned_data['name']
                    partner_brand.description = partner_form.cleaned_data['description']
                    partner_brand.image = partner_form.cleaned_data['image']
                    partner_brand.location = partner_location
                    # partner_brand.style = partner_form.cleaned_data['style']
                    partner_brand.category = partner_form.cleaned_data['category']
                    partner_brand.sub_category = partner_form.cleaned_data['sub_category']
                    partner_brand.save()
                    partner_invite.is_used = True
                    partner_invite.save()

                    return HttpResponse("Partner successfully registered.")
                else:
                    brands_list = Partner.objects.all().order_by('-created')[:3]
                    context = {'brands':brands_list,'user_form': partner_form}
                    return render(request, 'common/partner_register.html', context)
                    # return render(request, 'common/partner_register.html', {'user_form': partner_form})
        else:
            return HttpResponse("The link is expired")
        # except:
        #     return HttpResponse("sorry link is used already.")


class BrandListView(ListView):
    """
    List the brands
    """
    context_object_name = "brands"
    template_name = 'brand/brand_list.html'
    model = Partner
    page_title = 'Brands'
    paginate_by = settings.PAGE_SIZE

    def get(self, request, *args, **kwargs):

        return super(BrandListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        products_type = self.request.GET.get('products_category')
        location = self.request.GET.get('location')
        qs = Partner.objects.all()
        if products_type != 'all' and products_type == 'Menswear':
            qs = qs.filter(category__name='Menswear')
        elif products_type != 'all' and products_type == 'Womenswear':
            qs = qs.filter(category__name='Womenswear')
        if location:
            qs = qs.filter(location__country=location)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super(BrandListView, self).get_context_data(*args, **kwargs)
        temp = [b.location.country for b in ctx['brands']]
        ctx['locations'] = []
        for i in temp:
            if i not in ctx['locations']:
                ctx['locations'].append(i)
        ctx['styles'] = ['all', 'Menswear', 'Womenswear'] # Make this list dynamic
        return ctx


class BrandDetailView(View):
    """
    Detail view of brand
    """
    context_object_name = "brand"
    template_name = 'brand/brand_detail.html'
    model = Partner
    page_title = 'Brands'

    def get(self, request, *args, **kwargs):
        partner_slug = self.kwargs['slug']
        qs = Partner.objects.get(slug=partner_slug)
        data = {'brand': qs}
        try:
            brand_followed = UserBrandLike.objects.get(user=request.user,brand=qs)
            data.update({'brand_followed':True})
        except:
            data.update({'brand_followed':False})
        products = Product.objects.filter(brand=qs)
        data.update({'products': products})
        data.update({'follow_count':UserBrandLike.objects.filter(brand=qs).count()})
        data.update({'filters': ['all', 'Menswear', 'Womenswear']}) # Make this list dynamic

        return render(request, self.template_name, data)
