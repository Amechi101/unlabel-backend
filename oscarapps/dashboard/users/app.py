from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class UserManagementApplication(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    index_view = get_class('dashboard.users.views', 'IndexView')
    user_detail_view = get_class('dashboard.users.views', 'UserDetailView')
    password_reset_view = get_class('dashboard.users.views',
                                    'PasswordResetView')
    alert_list_view = get_class('dashboard.users.views',
                                'ProductAlertListView')
    alert_update_view = get_class('dashboard.users.views',
                                  'ProductAlertUpdateView')
    alert_delete_view = get_class('dashboard.users.views',
                                  'ProductAlertDeleteView')
    influencer_invite_view = get_class('dashboard.users.views',
                                    'InfluencerInviteView')

    def get_urls(self):
        urls = [
            url(r'^$', self.index_view.as_view(), name='users-index'),
            url(r'^(?P<pk>-?\d+)/$',
                self.user_detail_view.as_view(), name='user-detail'),
            url(r'^(?P<pk>-?\d+)/password-reset/$',
                self.password_reset_view.as_view(),
                name='user-password-reset'),

            # Alerts
            url(r'^alerts/$',
                self.alert_list_view.as_view(),
                name='user-alert-list'),
            url(r'^alerts/(?P<pk>-?\d+)/delete/$',
                self.alert_delete_view.as_view(),
                name='user-alert-delete'),
            url(r'^alerts/(?P<pk>-?\d+)/update/$',
                self.alert_update_view.as_view(),
                name='user-alert-update'),
            url(r'^(?P<pk>-?\d+)/influencer-invite/$',
                self.influencer_invite_view.as_view(),
                name='influencer-invite'),
        ]
        return self.post_process_urls(urls)


application = UserManagementApplication()
