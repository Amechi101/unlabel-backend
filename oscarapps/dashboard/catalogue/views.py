from django.contrib import messages
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from oscar.apps.customer.utils import normalise_email
from oscar.core.compat import get_user_model
from oscar.core.loading import get_classes, get_model
from oscar.views import sort_queryset










#style views

Style = get_model('partner', 'Style')
(
    StyleSearchForm, StyleCreateForm
) = get_classes(
    'dashboard.catalogue.forms',
    ['StyleSearchForm', 'StyleCreateForm'], 'oscarapps')


class StyleListView(generic.ListView):
    model = Style
    context_object_name = 'styles'
    template_name = 'dashboard/catalogue/style/style_list.html'
    form_class = StyleSearchForm

    def get_queryset(self):
        qs = self.model._default_manager.all()
        qs = sort_queryset(qs, self.request, ['name'])

        self.description = _("All Styles")

        # We track whether the queryset is filtered to determine whether we
        # show the search form 'reset' button.
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Styles matching '%s'") % data['name']
            self.is_filtered = True

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(StyleListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx


class StyleCreateView(generic.CreateView):
    model = Style
    template_name = 'dashboard/catalogue/style/style_form.html'
    form_class = StyleCreateForm
    success_url = reverse_lazy('dashboard:style-list')

    def get_context_data(self, **kwargs):
        ctx = super(StyleCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create new style')
        return ctx

    def get_success_url(self):
        messages.success(self.request,
                         _("Style '%s' was created successfully.") %
                         self.object.name)
        return reverse('dashboard:style-list')

#
class StyleManageView(generic.UpdateView):
    """
    This multi-purpose view renders out a form to edit the partner's details,
    the associated address and a list of all associated users.
    """
    template_name = 'dashboard/catalogue/style/style_manage.html'
    form_class = StyleCreateForm
    success_url = reverse_lazy('dashboard:style-list')

    def get_object(self, queryset=None):
        self.style = get_object_or_404(Style, pk=self.kwargs['pk'])
        style = self.style
        return style

    def get_initial(self):
        return {'name': self.style.name}

    def get_context_data(self, **kwargs):
        ctx = super(StyleManageView, self).get_context_data(**kwargs)
        ctx['partner'] = self.style
        ctx['title'] = self.style.name
        return ctx

    def form_valid(self, form):
        messages.success(
            self.request, _("Style '%s' was updated successfully.") %
            self.style.name)
        self.style.name = form.cleaned_data['name']
        self.style.save()
        return super(StyleManageView, self).form_valid(form)


class StyleDeleteView(generic.DeleteView):
    model = Style
    template_name = 'dashboard/catalogue/style/style_delete.html'

    def get_success_url(self):
        messages.success(self.request,
                         _("Style '%s' was deleted successfully.") %
                         self.object.name)
        return reverse('dashboard:style-list')






