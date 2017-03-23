from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class
from oscar.apps.dashboard.ranges.app import RangeDashboardApplication as CoreRangeDashboardApplication

class RangeDashboardApplication(CoreRangeDashboardApplication):
    permissions_map = _map = {
        'range-list': (['is_staff'], ['partner.dashboard_access']),
        'range-create': (['is_staff'], ['partner.dashboard_access']),
        'range-update': (['is_staff'], ['partner.dashboard_access']),
        'range-delete': (['is_staff'], ['partner.dashboard_access']),
        'range-products': (['is_staff'], ['partner.dashboard_access']),
        'range-reorder': (['is_staff'], ['partner.dashboard_access']),
    }

    def get_urls(self):
        urlpatterns = [
            url(r'^$', self.list_view.as_view(), name='range-list'),
            url(r'^create/$', self.create_view.as_view(), name='range-create'),
            url(r'^(?P<pk>\d+)/$', self.update_view.as_view(),
                name='range-update'),
            url(r'^(?P<pk>\d+)/delete/$', self.delete_view.as_view(),
                name='range-delete'),
            url(r'^(?P<pk>\d+)/products/$', self.products_view.as_view(),
                name='range-products'),
            url(r'^(?P<pk>\d+)/reorder/$', self.reorder_view.as_view(),
                name='range-reorder'),
        ]
        return self.post_process_urls(urlpatterns)


application = RangeDashboardApplication()
