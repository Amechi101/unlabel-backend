from oscarapi.app import RESTApiApplication
from django.conf.urls import url


class MyRESTApiApplication(RESTApiApplication):

    def get_urls(self):
        # urls = [url(
        #    r'^products/$',
        #    views.ProductList.as_view(), name='product-list')]

        urls=[]

        return urls + super(MyRESTApiApplication, self).get_urls()

application = MyRESTApiApplication()