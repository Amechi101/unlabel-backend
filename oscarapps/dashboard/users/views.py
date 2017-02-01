from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableMixin
from django.views.generic import View
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.models import Site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail.message import EmailMessage
from django.shortcuts import render, redirect

from oscar.apps.customer.utils import normalise_email
from oscar.core.compat import get_user_model
from oscar.core.loading import get_class, get_classes, get_model
from oscar.views.generic import BulkEditMixin

UserSearchForm, ProductAlertSearchForm, ProductAlertUpdateForm = get_classes(
    'dashboard.users.forms', ('UserSearchForm', 'ProductAlertSearchForm',
                              'ProductAlertUpdateForm'))
PasswordResetForm = get_class('customer.forms', 'PasswordResetForm')
UserTable = get_class('dashboard.users.tables', 'UserTable')
ProductAlert = get_model('customer', 'ProductAlert')
User = get_user_model()


class IndexView(BulkEditMixin, SingleTableMixin, FormMixin, TemplateView):
    template_name = 'dashboard/users/index.html'
    table_pagination = True
    model = User
    actions = ('make_active', 'make_inactive', )
    form_class = UserSearchForm
    table_class = UserTable
    context_table_name = 'users'
    desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
    description = ''

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Only bind search form if it was submitted.
        """
        kwargs = super(IndexView, self).get_form_kwargs()

        if 'search' in self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })

        return kwargs

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-date_joined')
        return self.apply_search(queryset)

    def apply_search(self, queryset):
        # Set initial queryset description, used for template context
        self.desc_ctx = {
            'main_filter': _('All users'),
            'email_filter': '',
            'name_filter': '',
        }
        if self.form.is_valid():
            return self.apply_search_filters(queryset, self.form.cleaned_data)
        else:
            return queryset

    def apply_search_filters(self, queryset, data):
        """
        Function is split out to allow customisation with little boilerplate.
        """
        if data['email']:
            email = normalise_email(data['email'])
            queryset = queryset.filter(email__istartswith=email)
            self.desc_ctx['email_filter'] \
                = _(" with email matching '%s'") % email
        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            if len(parts) == 2:
                condition = Q(first_name__istartswith=parts[0]) \
                    | Q(last_name__istartswith=parts[1])
            else:
                condition = Q(first_name__istartswith=data['name']) \
                    | Q(last_name__istartswith=data['name'])
            queryset = queryset.filter(condition).distinct()
            self.desc_ctx['name_filter'] \
                = _(" with name matching '%s'") % data['name']

        return queryset

    def get_table(self, **kwargs):
        table = super(IndexView, self).get_table(**kwargs)
        table.caption = self.desc_template % self.desc_ctx
        return table

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def make_inactive(self, request, users):
        return self._change_users_active_status(users, False)

    def make_active(self, request, users):
        return self._change_users_active_status(users, True)

    def _change_users_active_status(self, users, value):
        for user in users:
            if not user.is_superuser:
                user.is_active = value
                user.save()
        messages.info(self.request, _("Users' status successfully changed"))
        return redirect('dashboard:users-index')


class UserDetailView(DetailView):
    template_name = 'dashboard/users/detail.html'
    model = User
    context_object_name = 'customer'


class PasswordResetView(SingleObjectMixin, FormView):
    form_class = PasswordResetForm
    http_method_names = ['post']
    model = User

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(PasswordResetView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PasswordResetView, self).get_form_kwargs()
        kwargs['data'] = {'email': self.object.email}
        return kwargs

    def form_valid(self, form):
        # The PasswordResetForm's save method sends the reset email
        form.save(request=self.request)
        return super(PasswordResetView, self).form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, _("A password reset email has been sent"))
        return reverse(
            'dashboard:user-detail', kwargs={'pk': self.object.id}
        )


class ProductAlertListView(ListView):
    model = ProductAlert
    form_class = ProductAlertSearchForm
    context_object_name = 'alerts'
    template_name = 'dashboard/users/alerts/list.html'
    paginate_by = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
    base_description = _('All Alerts')
    description = ''

    def get_queryset(self):
        queryset = self.model.objects.all()
        self.description = self.base_description

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        if data['status']:
            queryset = queryset.filter(status=data['status']).distinct()
            self.description \
                += _(" with status matching '%s'") % data['status']

        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            if len(parts) >= 2:
                queryset = queryset.filter(
                    user__first_name__istartswith=parts[0],
                    user__last_name__istartswith=parts[1]
                ).distinct()
            else:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=parts[0]) |
                    Q(user__last_name__istartswith=parts[-1])
                ).distinct()
            self.description \
                += _(" with customer name matching '%s'") % data['name']

        if data['email']:
            queryset = queryset.filter(
                Q(user__email__icontains=data['email']) |
                Q(email__icontains=data['email'])
            )
            self.description \
                += _(" with customer email matching '%s'") % data['email']

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductAlertListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['queryset_description'] = self.description
        return context


class ProductAlertUpdateView(UpdateView):
    template_name = 'dashboard/users/alerts/update.html'
    model = ProductAlert
    form_class = ProductAlertUpdateForm
    context_object_name = 'alert'

    def get_success_url(self):
        messages.success(self.request, _("Product alert saved"))
        return reverse('dashboard:user-alert-list')


class ProductAlertDeleteView(DeleteView):
    model = ProductAlert
    template_name = 'dashboard/users/alerts/delete.html'
    context_object_name = 'alert'

    def get_success_url(self):
        messages.warning(self.request, _("Product alert deleted"))
        return reverse('dashboard:user-alert-list')


class InfluencerInviteView(View):
    """
    View for sending invitation email to user email,
    the generated link will be send to the user
    and will be redirected back to the same page.
    """

    def post(self,request,pk):
        invite_user=User.objects.get(id=pk)
        current_site = Site.objects.get_current()
        domain = current_site.domain
        invite_user=User.objects.get(id=pk)
        context = {
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(invite_user.pk)),
            'user': invite_user,
            'token': default_token_generator.make_token(invite_user),
            'protocol': 'http',
        }
        tosend = context['protocol']+'://'+context['domain']+'/influencers/influencer-sign-up/'+context['uid'].decode("utf-8")+'/'
        email = EmailMessage()
        email.subject = "Influencer inviattion from Unlabel"
        email.content_subtype = "html"
        email.body = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><META http-equiv='Content-Type' content='text/html; charset=utf-8'></head>
                        <body>
                        <br><br>
                        You're being invited as influencer at unlabel
                        <br><br>
                        Please fill the form provided at the link :
                        <br><br>
                        """+tosend+"""
                        <br><br>
                        Thank you for using our site!
                        <br/>
                        <br/>
                        <p style='font-size:11px;'><i>*** This is a system generated email; Please do not reply. ***</i></p>
                        </body>
                        </head>
                        </html>"""
        email.from_email = "Unlabel App"
        email.to = [invite_user.email]
        email.send()
        return HttpResponseRedirect("/oscar/dashboard/users/"+str(invite_user.id)+"/")
