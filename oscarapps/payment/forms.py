from oscar.apps.payment.forms import BillingAddressForm as CoreBillingAddressForm



class BillingAddressForm(CoreBillingAddressForm):

    def __init__(self, *args, **kwargs):
        super(BillingAddressForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['line1'].required = False
        self.fields['line2'].required = False
        self.fields['line3'].required = False
        self.fields['state'].required = False
        self.fields['postcode'].required = False
        self.fields['country'].required = False

