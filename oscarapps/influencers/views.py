from __future__ import unicode_literals
import datetime

from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import utc

from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from oscarapps.catalogue.models import Product
from .models import InfluencerProductReserve


from users.models import User
from oscarapps.influencers.models import Influencers,InfluencerInvite
from oscarapps.influencers.forms import InfluencerSignUpForm
from oscarapps.address.models import Locations, States, Country

from rest_framework import pagination
from oscar.core.loading import (
    get_class, get_classes, get_model, get_profile_class)

from users.models import User
import operator
from functools import reduce
from rest_framework import generics
from rest_framework.response import Response
from .forms import InfluencerSearchFilterForm
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from oscarapps.partner.models import Category, Style
import json

UserInfluencerLike = get_model('customer','UserInfluencerLike')

class InfluencerFilterView(generics.ListAPIView):

    pagination_class = pagination.LimitOffsetPagination
    http_method_names = ('get',)

    def get_queryset(self, *args, **kwargs):
        style_selected = self.request.GET.get('style',None)
        location_selected = self.request.GET.get('location',None)
        gender_selected = self.request.GET.get('gender',None)
        order = self.request.GET.get('order')

        influencers_list = Influencers.objects.all()

        print("======== ",style_selected,"===========",location_selected,"============",gender_selected)

        if gender_selected:
            gender_selected = gender_selected.split(',')
            influencers_list = influencers_list.filter(users__gender__in=gender_selected)
        if style_selected:
            style_selected = style_selected.split(',')
            styles = Style.objects.filter(id__in=style_selected)
            influencers_list = influencers_list.filter(styles__in=styles)
        if location_selected:
            location_selected = location_selected.split(',')
            location_citys = Locations.objects.filter(id__in=location_selected).values_list('city',flat=True)
            locations = Locations.objects.filter(city__in=location_citys)
            influencers_list = influencers_list.filter(location__in=locations)

        return influencers_list

        # print(">>>>>>>>>>>>>>>>>> ",influencers_list)
        # paginator = Paginator(influencers_list, 2) # Show 25 contacts per page
        # page = request.GET.get('page')
        # try:
        #     influencers = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer, deliver first page.
        #     influencers = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range (e.g. 9999), deliver last page of results.
        #     influencers = paginator.page(paginator.num_pages)
        #
        #
        # renderedString = render_to_string("influencers/influencer_filter_list.html",{'influencers':influencers})
        # return Response({'html':renderedString})



class InfluencerListView(View):
    template_name = 'influencers/influencers.html'
    model = Influencers

    def get(self,request,*args,**kwargs):
        influencers_list = Influencers.objects.filter(users__is_active=True).order_by('-created')

        paginator = Paginator(influencers_list, 2) # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            influencers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            influencers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            influencers = paginator.page(paginator.num_pages)


        data = {'influencers':influencers,'styles':Style.objects.all(),
                'locations':Locations.objects.all().distinct('city') }
        return render(request, self.template_name , data)



class InfluencerDetailView(SingleObjectMixin, ListView):
    model = Influencers

    template_name = 'influencers/influencer_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Influencers.objects.all())

        return super(InfluencerDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerDetailView, self).get_context_data(**kwargs)

        ctx['influencer'] = self.object

        return ctx

    def get_queryset(self, **kwargs):
        return self.object


class InfluencerSignUpView(View):

    def get(self, request, code, *args, **kwargs):
        try:
            influencer_invite = InfluencerInvite.objects.get(code=code,is_used=False)
        except ObjectDoesNotExist:
            return HttpResponse("sorry invalid invite request.")
        if influencer_invite.is_used is True:
            return HttpResponse("sorry, The link is already used")
        elif influencer_invite.is_used is False:
            influencer_list = Influencers.objects.all()[:3]
            context = {'influencers': influencer_list, 'user_form': InfluencerSignUpForm}
            return render(request, 'influencers/influencer_register.html', context)

    def post(self, request, code, *args, **kwargs):
        influencer_form = InfluencerSignUpForm(data=request.POST)
        try:
            influencer_invite = InfluencerInvite.objects.get(code=code, is_used=False)
            check_date = datetime.datetime.utcnow().replace(tzinfo=utc)
            sent_date = influencer_invite.date_sent
            if (((check_date - sent_date).total_seconds())/60)/60 < 24 and influencer_invite.is_used == False:
                if influencer_form.is_valid():
                    influencer_user = User()
                    influencer_user.email = influencer_form.cleaned_data['email']
                    influencer_user.first_name = influencer_form.cleaned_data['first_name']
                    influencer_user.last_name = influencer_form.cleaned_data['last_name']
                    influencer_user.is_influencer = True
                    influencer_user.contact_number = influencer_form.cleaned_data['contact_number']
                    influencer_user.gender = influencer_form.cleaned_data['gender']
                    influencer_user.save()
                    influencer_user.set_password(influencer_form.cleaned_data['password1'])
                    influencer_user.save()
                    location = str(influencer_form['loc'].value()).split(', ')
                    city = ", ".join(str(x) for x in location[:-2])
                    state = str(location[-2:-1][0])
                    if str(location[-1:][0]) == "United States":
                        country = "USA"
                    else:
                        country = str(location[-1:][0])
                    influencer_location = Locations.objects.create(city=city,
                                                                   state=state,
                                                                   country=country,
                                                                   is_influencer_location=True)
                    influencer_location.save()
                    print(influencer_location)
                    influencer_profile = Influencers()
                    influencer_profile.bio = influencer_form.cleaned_data['bio']
                    influencer_profile.image = influencer_form.cleaned_data['image']
                    influencer_profile.chest_or_bust = influencer_form.cleaned_data['chest_or_bust']
                    influencer_profile.height = influencer_form.cleaned_data['height']
                    influencer_profile.hips = influencer_form.cleaned_data['hips']
                    influencer_profile.waist = influencer_form.cleaned_data['waist']
                    influencer_profile.users = influencer_user
                    influencer_profile.location = influencer_location
                    influencer_profile.save()
                    influencer_invite.is_used = True
                    influencer_invite.save()

                    return HttpResponse("Influencer successfully registered.")
                else:
                    influencer_list = Influencers.objects.all()[:3]
                    context = {'influencers': influencer_list, 'user_form': InfluencerSignUpForm}
                    return render(request, 'influencers/influencer_register.html', context)
            else:
                return HttpResponse("The page you requested is expired.")
        except:
            return HttpResponse("Sorry, The sign up link you requested is already used.")


class UccDetail(View):
    """
    Detail view of ucc
    """
    context_object_name = "influencer"
    template_name = 'influencers/ucc_detail.html'
    model = Influencers
    page_title = 'Influencer'

    def get(self, request, *args, **kwargs):
        influencer_id = self.kwargs['id']
        try:
            qs = Influencers.objects.get(pk=influencer_id)
            data = {'influencer': qs}
            p = InfluencerProductReserve.objects.filter(influencer=influencer_id, is_live=True).values_list('product',
                                                                                                            flat=True)
            products = Product.objects.filter(id__in=p)
            data.update({'products': products})
            try:
                followed = UserInfluencerLike.objects.get(user=request.user,influencer=qs)
                data.update({'ucc_followed':True})
            except:
                data.update({'ucc_followed':False})
            data.update({'follow_count':UserInfluencerLike.objects.filter(influencer=qs).count()})
        except:
            return render(request,'404.html', {})

        return render(request,self.template_name,data)
