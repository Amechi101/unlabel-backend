from django.forms import RadioSelect
from django import forms
from oscar.core.loading import get_class, get_classes, get_model
from oscar.apps.checkout.forms import ShippingAddressForm as CoreShippingAddressForm





class InvoiceAddressForm(CoreShippingAddressForm):

    def __init__(self, *args, **kwargs):
        # self.fields['title'].widget=RadioSelect
        super(InvoiceAddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = get_model('order', 'shippingaddress')
        fields = [
            'title', 'first_name', 'last_name',
            'line1', 'line2', 'line3', 'line4',
            'state', 'postcode', 'country',
            'phone_number',
        ]