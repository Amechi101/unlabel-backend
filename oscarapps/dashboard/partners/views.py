import uuid

from django.core.exceptions import PermissionDenied

from oscarapps.address.models import States, Country, Locations
from oscarapps.dashboard.partners.forms import PartnerCreateForm, PartnerManageForm, PartnerRentalInfoForm
from oscarapps.partner.models import Partner
from oscarapps.partner.models import PartnerInvite
from oscarapps.partner.models import Style, Category, SubCategory
from users.models import User

from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import Context
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic import FormView
from oscar.apps.dashboard.partners.forms import PartnerSearchForm
from oscar.apps.dashboard.partners.views import PartnerDeleteView as CorePartnerDeleteView
from oscar.apps.dashboard.partners.views import PartnerListView as CorePartnerListView
from oscar.apps.dashboard.partners.views import PartnerManageView as CorePartnerManageView
from oscar.apps.dashboard.partners.views import PartnerUserUpdateView as CorePartnerUserUpdateView

from oscar.core.loading import get_classes, get_model
from oscar.core.utils import slugify
from oscar.views import sort_queryset
from django.contrib.auth.models import Permission

# =======
#Partner views
#=======

class PartnerListView(CorePartnerListView):


    def post(self, request, *args, **kwargs):

        invite_email = request.POST.get("invite_email")
        if invite_email is not None and invite_email!="":
            current_site = Site.objects.get_current()
            domain = current_site.domain
            context = {
                'domain': domain,
                'verify_code' : str(uuid.uuid1()).replace('-','').upper()[0:10],
                'user': invite_email,
                'protocol': 'http',
            }
            invite_sent = PartnerInvite()
            invite_sent.email = context['user']
            invite_sent.code = context['verify_code']
            tosend = context['protocol'] + '://' + context['domain'] + '/partners/partner-sign-up/' + context['verify_code'] + '/'
            email = EmailMessage()
            email.subject = "Partner invitation from Unlabel"
            email.content_subtype = "html"
            tem = loader.get_template('dashboard/partners/partner_email_body.html')
            context = Context({'tosend':tosend})
            body = tem.render(context)
            email.body = body
            email.from_email = "Unlabel App"
            email.to = [invite_email]
            email.send()

            messages.success(
            self.request, "An invitation email was successfully sent to '%s' " %invite_sent.email)
            invite_sent.save()
            return HttpResponseRedirect("/dashboard/partners/")
        else:
            return HttpResponseRedirect("/dashboard/partners/")


    def get_queryset(self):

        if not self.request.user.is_staff:
            qs = self.model._default_manager.filter(users=self.request.user)
        else:
            qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All brands")
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Brands matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(PartnerListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_staff'] = self.request.user.is_staff
        ctx['is_filtered'] = self.is_filtered
        return ctx


class PartnerCreateView(generic.View):
    model = Partner
    template_name = 'dashboard/partners/partner_form.html'
    form_class = PartnerCreateForm
    success_url = reverse_lazy('dashboard:partner-list')

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/partners/partner_form.html', {'form': PartnerCreateForm})

    def post(self, request, *args, **kwargs):
        partner_form = PartnerCreateForm(data=request.POST)
        if partner_form.is_valid():
            partner_user = User.objects.create(email=partner_form['email'].value(),
                                                 password=partner_form['password1'].value(),
                                                 first_name=partner_form['first_name'].value(),
                                                 last_name=partner_form['last_name'].value(),
                                                 is_brand = True,
                                                 is_influencer = False
                                                 )
            partner_user.save()
            partner_user.set_password(partner_form['password1'].value())
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
            partner_profile = Partner.objects.create(name=partner_form['name'].value(),
                                                    description=partner_form['description'].value(),
                                                    location = partner_location,
                                                    slug=slugify(partner_form['name'].value())
                                                    )
            partner_profile.users.add(partner_user)
            partner_profile.style.add(*list(Style.objects.filter(pk__in=partner_form['style'].value())))
            partner_profile.category.add(*list(Category.objects.filter(pk__in=partner_form['category'].value())))
            partner_profile.sub_category.add(*list(SubCategory.objects.filter(pk__in=partner_form['sub_category'].value())))
            if 'image' in request.FILES:
                partner_profile.image = request.FILES['image']

            partner_profile.save()

            return HttpResponseRedirect("/dashboard/partners/")

        else:
            return render(request, 'dashboard/partners/partner_form.html', {'form': partner_form})


class PartnerManageView(CorePartnerManageView, FormView):
    form_class = PartnerManageForm

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        if self.request.user.is_brand:
            if self.partner.users.all().first() != self.request.user:
                raise PermissionDenied
        return self.partner

    def get_initial(self):

      return {
            # 'city': self.partner.location.city,
            # 'state': self.partner.location.state,
            # 'country': self.partner.location.country,
            'loc': self.partner.location,
            'email': self.partner.users.all().first().email,
            'password': self.partner.users.all().first().password,
            'first_name': self.partner.users.all().first().first_name,
            'last_name': self.partner.users.all().first().last_name,
            'is_active': self.partner.is_active
      }

    def get_context_data(self, **kwargs):
        ctx = super(PartnerManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Brand '%s' was updated successfully.") %
            self.partner.name)
        return super(PartnerManageView, self).form_valid(form)



class PartnerRentalInfoManageView(generic.UpdateView):
    template_name = 'dashboard/partners/partner_rental_info_manage.html'
    form_class = PartnerRentalInfoForm

    def get_success_url(self):
        return reverse_lazy('dashboard:partner-manage', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        self.partner = get_object_or_404(Partner, pk=self.kwargs['pk'])
        address = self.partner.rental_info
        if self.request.user.is_brand:
            if self.partner.users.all().first() != self.request.user:
                raise PermissionDenied
        return address

    def get_initial(self):
        days = []
        try:
            location_name = self.partner.rental_info.city+", "+ self.partner.rental_info.state+", "+self.partner.rental_info.country
            rental_days = self.partner.rental_info.rental_time.all()

            for day in rental_days:
                days.append(day.day)
        except:
            location_name = ""
            rental_days = ""
        result = {'name': self.partner.name,
                  'loc': location_name}
        if days:
            result['day'] = [days[0]]
            for i, day in enumerate(rental_days):
                result['day_'+str(i+1)] = [days[i]]
                result['start_time_'+str(i+1)] = day.start_time
                result['start_time_period_'+str(i+1)] = day.start_time_period
                result['end_time_'+str(i+1)] = day.end_time
                result['end_time_period_'+str(i+1)] = day.end_time_period

        return result

    def get_context_data(self, **kwargs):

        ctx = super(PartnerRentalInfoManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.partner
        ctx['title'] = self.partner.name
        ctx['users'] = self.partner.users.all()
        # ctx['states'] = stateList
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Address of brand '%s' was updated successfully.") %
            self.partner.name)

        self.partner.rental_info = form.save()
        self.partner.save()
        # locationForm=form.save()
        # locationForm.save()
        return super(PartnerRentalInfoManageView, self).form_valid(form)


class PartnerDeleteView(CorePartnerDeleteView):
    model = Partner
    template_name = 'dashboard/partners/partner_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:partner-list')


class PartnerFilterView(generic.ListView):

    model = Partner
    context_object_name = 'partners'
    template_name = 'dashboard/partners/partner_list.html'
    form_class = PartnerSearchForm

    def get(self, request, *args, **kwargs):
        return super(PartnerFilterView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.all()

        is_active = self.request.GET.get('active')
        created_date = self.request.GET.get('created_date')
        modified_date = self.request.GET.get('modified_date')

        if is_active:
            queryset = queryset.filter(is_active=True)

        if created_date:
            queryset = queryset.filter(created__regex=created_date)

        if modified_date:
            queryset = queryset.filter(modified__regex=modified_date)

        self.description = _("All brands")
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)

        if not self.form.is_valid():
            return queryset
        data = self.form.cleaned_data

        if data['name']:
            queryset = queryset.filter(name__icontains=data['name'])
            self.description = _("Brands matching '%s'") % data['name']
            self.is_filtered = True

        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(PartnerFilterView, self).get_context_data(**kwargs)
        is_active = self.request.GET.get('active')
        created_date = self.request.GET.get('created_date')
        modified_date = self.request.GET.get('modified_date')
        if is_active:
            ctx['active'] = True
        if created_date:
            ctx['created_date'] = created_date
        if modified_date:
            ctx['modified_date'] = modified_date
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class PartnerUserUpdateView(CorePartnerUserUpdateView):
    def get_form_kwargs(self):
        kwargs = super(PartnerUserUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


#=========================
#Brand Categories Views
#==========================


BrandCategories = get_model('partner', 'Category')
(
    BrandCategorySearchForm, BrandCategoryCreateForm
) = get_classes(
    'dashboard.partners.forms',
    ['BrandCategorySearchForm', 'BrandCategoryCreateForm'], 'oscarapps')


class BrandCategoryListView(generic.ListView):
    model = BrandCategories
    context_object_name = 'brand_categories'
    template_name = 'dashboard/partners/brand_categories/brand_category_list.html'
    form_class = BrandCategorySearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Store Types")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Store Types matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BrandCategoryListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class BrandCategoryCreateView(generic.CreateView):
    model = BrandCategories
    template_name = 'dashboard/partners/brand_categories/brand_category_form.html'
    form_class = BrandCategoryCreateForm
    success_url = reverse_lazy('dashboard:brand-category-list')

    def get_context_data(self, **kwargs):
        ctx = super(BrandCategoryCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new Store Type')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Store Type '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-category-list')


class BrandCategoryManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/partners/brand_categories/brand_category_manage.html'
    form_class = BrandCategoryCreateForm
    success_url = reverse_lazy('dashboard:brand-category-list')

    def get_object(self, queryset=None):
        self.brand_category = get_object_or_404(BrandCategories, pk=self.kwargs['pk'])
        return self.brand_category

    def get_initial(self):
        return {'name': self.brand_category.name}

    def get_context_data(self, **kwargs):
        ctx = super(BrandCategoryManageView, self).get_context_data(**kwargs)
        ctx['brand_category'] = self.brand_category
        ctx['title'] = self.brand_category.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Store Type '%s' was updated successfully.") %
            self.brand_category.name)
        self.brand_category.name = form.cleaned_data['name']
        self.brand_category.save()
        return super(BrandCategoryManageView, self).form_valid(form)


class BrandCategoryDeleteView(generic.DeleteView):
    model = BrandCategories
    template_name = 'dashboard/partners/brand_categories/brand_category_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Store Type '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-category-list')


#=========================
#Brand Styles Views
#==========================


BrandStyle = get_model('partner', 'Style')
(
    BrandStyleSearchForm, BrandStyleCreateForm
) = get_classes(
    'dashboard.partners.forms',
    ['BrandStyleSearchForm', 'BrandStyleCreateForm'], 'oscarapps')


class BrandStyleListView(generic.ListView):
    model = BrandStyle
    context_object_name = 'brand_styles'
    template_name = 'dashboard/partners/brand_styles/brand_style_list.html'
    form_class = BrandStyleSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Brand Styles")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs
        data = self.form.cleaned_data
        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Brand style matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BrandStyleListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class BrandStyleCreateView(generic.CreateView):
    model = BrandStyle
    template_name = 'dashboard/partners/brand_styles/brand_style_form.html'
    form_class = BrandStyleCreateForm
    success_url = reverse_lazy('dashboard:brand-style-list')

    def get_context_data(self, **kwargs):
        ctx = super(BrandStyleCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new brand style')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand style '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-style-list')


class BrandStyleManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/partners/brand_styles/brand_style_manage.html'
    form_class = BrandStyleCreateForm
    success_url = reverse_lazy('dashboard:brand-style-list')

    def get_object(self, queryset=None):
        self.brand_style = get_object_or_404(BrandStyle, pk=self.kwargs['pk'])
        return self.brand_style

    def get_initial(self):
        return {'name': self.brand_style.name}

    def get_context_data(self, **kwargs):
        ctx = super(BrandStyleManageView, self).get_context_data(**kwargs)
        ctx['brand_style'] = self.brand_style
        ctx['title'] = self.brand_style.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Brand style '%s' was updated successfully.") %
            self.brand_style.name)
        self.brand_style.name = form.cleaned_data['name']
        self.brand_style.save()
        return super(BrandStyleManageView, self).form_valid(form)


class BrandStyleDeleteView(generic.DeleteView):
    model = BrandStyle
    template_name = 'dashboard/partners/brand_styles/brand_style_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand style '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-style-list')



#=========================
#Brand SubCategory Views
#==========================


BrandSubCategory = get_model('partner', 'SubCategory')
(
    SubCategorySearchForm, SubCategoryCreateForm
) = get_classes(
    'dashboard.partners.forms',
    ['SubCategorySearchForm', 'SubCategoryCreateForm'], 'oscarapps')


class BrandSubCategoryListView(generic.ListView):
    model = BrandSubCategory
    context_object_name = 'brand_sub_categories'
    template_name = 'dashboard/partners/brand_sub_categories/sub_category_list.html'
    form_class = SubCategorySearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Brand Specializations")
        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs
        data = self.form.cleaned_data
        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Brand Specializations matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(BrandSubCategoryListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class BrandSubCategoryCreateView(generic.CreateView):
    model = BrandSubCategory
    template_name = 'dashboard/partners/brand_sub_categories/sub_category_form.html'
    form_class = SubCategoryCreateForm
    success_url = reverse_lazy('dashboard:brand-sub-category-list')

    def get_context_data(self, **kwargs):
        ctx = super(BrandSubCategoryCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new brand specialization')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand specialization '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-sub-category-list')


class BrandSubCategoryManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/partners/brand_sub_categories/sub_category_manage.html'
    form_class = SubCategoryCreateForm
    success_url = reverse_lazy('dashboard:brand-sub-category-list')

    def get_object(self, queryset=None):
        self.sub_category = get_object_or_404(BrandSubCategory, pk=self.kwargs['pk'])
        return self.sub_category

    def get_initial(self):
        return {'name': self.sub_category.name}

    def get_context_data(self, **kwargs):
        ctx = super(BrandSubCategoryManageView, self).get_context_data(**kwargs)
        ctx['sub_category'] = self.sub_category
        ctx['title'] = self.sub_category.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Brand specialization '%s' was updated successfully.") %
            self.sub_category.name)
        self.sub_category.name = form.cleaned_data['name']
        self.sub_category.save()
        return super(BrandSubCategoryManageView, self).form_valid(form)


class BrandSubCategoryDeleteView(generic.DeleteView):
    model = BrandSubCategory
    template_name = 'dashboard/partners/brand_sub_categories/sub_category_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Brand specialization '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:brand-sub-category-list')