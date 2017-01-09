from .forms import NewUserForm, ExistingUserForm
from oscar.apps.dashboard.partners.forms import UserEmailForm
from django.contrib.auth.models import Permission
from oscar.apps.customer.utils import normalise_email
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from oscar.views import sort_queryset
from django.core.urlresolvers import reverse, reverse_lazy
from oscar.core.compat import get_user_model
User = get_user_model()

# ================
# Influencer views
# ================


from oscar.core.loading import get_classes, get_model
Influencers = get_model('influencers', 'Influencers')
(
    InfluencerSearchForm, InfluencerCreateForm
) = get_classes(
    'dashboard.influencers.forms',
    ['InfluencerSearchForm', 'InfluencerCreateForm'], 'oscarapps')


class InfluencerListView(generic.ListView):
    model = Influencers
    context_object_name = 'influencers'
    template_name = 'influencers/influencer_list.html'
    form_class = InfluencerSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])

        self.description = _("All influencers")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Influencers matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx



class InfluencerCreateView(generic.CreateView):
    model = Influencers
    template_name = 'influencers/influencer_form.html'
    form_class = InfluencerCreateForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new influencer')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Influencer '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:influencer-list')


class InfluencerManageView(generic.UpdateView):

    template_name = 'influencers/influencer_manage.html'
    form_class = InfluencerCreateForm
    success_url = reverse_lazy('dashboard:influencer-list')

    def get_object(self, queryset=None):
        self.influencer = get_object_or_404(Influencers, pk=self.kwargs['pk'])
        return self.influencer

    def get_initial(self):

        return {'name': self.influencer.name}

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerManageView, self).get_context_data(**kwargs)
        ctx['influencer'] = self.influencer
        ctx['title'] = self.influencer.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Influencer '%s' was updated successfully.") %
            self.influencer.name)
        self.influencer.name = form.cleaned_data['name']
        self.influencer.save()
        return super(InfluencerManageView, self).form_valid(form)


class InfluencerDeleteView(generic.DeleteView):
    model = Influencers
    template_name = 'influencers/influencer_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Influencer '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:influencer-list')


# =============
# Influencer users
# =============


class InfluencerUserCreateView(generic.CreateView):
    model = User
    template_name = 'influencers/influencer_user_form.html'
    form_class = NewUserForm

    def dispatch(self, request, *args, **kwargs):
        self.influencer = get_object_or_404(
            Influencers, pk=kwargs.get('influencer_pk', None))
        return super(InfluencerUserCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerUserCreateView, self).get_context_data(**kwargs)
        ctx['influencer'] = self.influencer
        ctx['title'] = _('Create user')
        return ctx

    def get_form_kwargs(self):
        kwargs = super(InfluencerUserCreateView, self).get_form_kwargs()
        kwargs['influencer'] = self.influencer
        return kwargs

    def get_success_url(self):
        name = self.object.get_full_name() or self.object.email
        messages.success(self.request,
                         _("User '%s' was created successfully.") % name)
        return reverse('dashboard:influencer-list')


class InfluencerUserSelectView(generic.ListView):
    template_name = 'influencers/influencer_user_select.html'
    form_class = UserEmailForm
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):

        self.influencer = get_object_or_404(
            Influencers, pk=kwargs.get('influencer_pk', None))
        return super(InfluencerUserSelectView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = None
        if 'email' in request.GET:
            data = request.GET
        self.form = self.form_class(data)
        return super(InfluencerUserSelectView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerUserSelectView, self).get_context_data(**kwargs)
        ctx['influencer'] = self.influencer
        ctx['form'] = self.form
        return ctx

    def get_queryset(self):
        if self.form.is_valid():
            email = normalise_email(self.form.cleaned_data['email'])
            return User.objects.filter(email__icontains=email)
        else:
            return User.objects.none()


class InfluencerUserLinkView(generic.View):

    def get(self, request, user_pk, influencer_pk):
        # need to allow GET to make Undo link in PartnerUserUnlinkView work
        return self.post(request, user_pk, influencer_pk)

    def post(self, request, user_pk, influencer_pk):
        user = get_object_or_404(User, pk=user_pk)
        name = user.get_full_name() or user.email
        influencer = get_object_or_404(Influencers, pk=influencer_pk)
        if self.link_user(user, influencer):
            messages.success(
                request,
                _("User '%(name)s' was linked to '%(influencer_name)s'")
                % {'name': name, 'influencer_name': influencer.name})
        else:
            messages.info(
                request,
                _("User '%(name)s' is already linked to '%(influencer_name)s'")
                % {'name': name, 'influencer_name': influencer.name})
        return redirect('dashboard:influencer-manage', pk=influencer_pk)

    def link_user(self, user, influencer):

        if influencer.users.filter(pk=user.pk).exists():
            return False
        influencer.users.add(user)
        if not user.is_staff:
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access',
                content_type__app_label='influencer')
            user.user_permissions.add(dashboard_access_perm)
        return True


class InfluencerUserUnlinkView(generic.View):

    def unlink_user(self, user, influencer):
        """
        Unlinks a user from a partner, and removes the dashboard permission
        if they are not linked to any other partners.

        Returns False if the user was not linked to the partner; True
        otherwise.
        """
        if not influencer.users.filter(pk=user.pk).exists():
            return False
        influencer.users.remove(user)
        if not user.is_staff and not user.influencers.exists():
            dashboard_access_perm = Permission.objects.get(
                codename='dashboard_access',
                content_type__app_label='influencer')
            user.user_permissions.remove(dashboard_access_perm)
        return True

    def post(self, request, user_pk, influencer_pk):
        user = get_object_or_404(User, pk=user_pk)
        name = user.get_full_name() or user.email
        influencer = get_object_or_404(Influencers, pk=influencer_pk)
        if self.unlink_user(user, influencer):
            msg = render_to_string(
                'influencers/influencer_user_unlinked.html',
                {'user_name': name,
                 'influencer_name': influencer.name,
                 'user_pk': user_pk,
                 'influencer_pk': influencer_pk})
            messages.success(self.request, msg, extra_tags='safe noicon')
        else:
            messages.error(
                request,
                _("User '%(name)s' is not linked to '%(influencer_name)s'") %
                {'name': name, 'influencer_name': influencer.name})
        return redirect('dashboard:influencer-manage', pk=influencer_pk)


# =====
# Users
# =====


class InfluencerUserUpdateView(generic.UpdateView):
    template_name = 'influencers/influencer_user_form.html'
    form_class = ExistingUserForm

    def get_object(self, queryset=None):
        self.influencer = get_object_or_404(Influencers, pk=self.kwargs['influencer_pk'])
        return get_object_or_404(User,
                                 pk=self.kwargs['user_pk'],
                                 influencers__pk=self.kwargs['influencer_pk'])

    def get_context_data(self, **kwargs):
        ctx = super(InfluencerUserUpdateView, self).get_context_data(**kwargs)
        name = self.object.get_full_name() or self.object.email
        ctx['influencer'] = self.influencer
        ctx['title'] = _("Edit user '%s'") % name
        return ctx

    def get_success_url(self):
        name = self.object.get_full_name() or self.object.email
        messages.success(self.request,
                         _("User '%s' was updated successfully.") % name)
        return reverse('dashboard:influencer-list')




#=========================
#Industry Preferences Views
#==========================
Industries = get_model('influencers', 'Industry')
(
    IndustrySearchForm, IndustryCreateForm
) = get_classes(
    'dashboard.influencers.forms',
    ['IndustrySearchForm', 'IndustryCreateForm'], 'oscarapps')


class IndustryListView(generic.ListView):
    model = Industries
    context_object_name = 'industries'
    template_name = 'industries/industry_list.html'
    form_class = IndustrySearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All Industry Preferences")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Industry preferences matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(IndustryListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class IndustryCreateView(generic.CreateView):
    model = Industries
    template_name = 'industries/industry_form.html'
    form_class = IndustryCreateForm
    success_url = reverse_lazy('dashboard:industry-list')

    def get_context_data(self, **kwargs):
        ctx = super(IndustryCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new industry preference')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Industry preference '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:industry-list')


class IndustryManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'industries/industry_manage.html'
    form_class = IndustryCreateForm
    success_url = reverse_lazy('dashboard:industry-list')

    def get_object(self, queryset=None):
        self.industry = get_object_or_404(Industries, pk=self.kwargs['pk'])
        return self.industry

    def get_initial(self):
        return {'name': self.industry.name}

    def get_context_data(self, **kwargs):
        ctx = super(IndustryManageView, self).get_context_data(**kwargs)
        ctx['industry'] = self.industry
        ctx['title'] = self.industry.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Industry preference '%s' was updated successfully.") %
            self.industry.name)
        self.industry.name = form.cleaned_data['name']
        self.industry.save()
        return super(IndustryManageView, self).form_valid(form)


class IndustryDeleteView(generic.DeleteView):
    model = Industries
    template_name = 'industries/industry_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Industry Preference '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:industry-list')

