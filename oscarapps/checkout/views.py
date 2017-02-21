import stripe
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.template import RequestContext

from oscarapps.checkout.models import Sale, Pay
from oscarapps.checkout.forms import SalePaymentForm
from users.models import User
from django.conf import settings


def charge(request):
    """
        making Payment
    """
    if request.method == "POST":
        form = SalePaymentForm(request.POST)

        if form.is_valid():
            print("Success! We've charged your card!")
            card_number = request.POST.get('number')
            amount = request.POST.get('amount')
            #g = Pay(pay=request.user, card_number=card_number, amount=amount)
            #request.user = "piyal.sayone@gmail.com"
            request.user = User.objects.get(email="piyal.sayone@gmail.com")
            g = Pay(pay=request.user, card_number=card_number, amount=amount)
            g.save()
            return render(request,'checkout/thankyou.html')
    else:
        form = SalePaymentForm()

    return render(request,'checkout/stripe.html', {'form': form})



# for the commissioning to other accounts

def transfer(request):
    """
        making transfer
    """

    stripe.api_key = settings.STRIPE_API_KEY
    # token = stripe.Token.create(
    #     bank_account={"country": 'US',
    #                   "currency": 'usd',
    #                   "routing_number": '110000000',
    #                   "account_number": '000123456789'
    #                   }
    # )
    #
    # print("one down")
    #
    # acct_id = token.id
    #
    # recipient = stripe.Recipient.create(
    #     name="John Doe",
    #     type="individual",
    #     email="binu.sayone@gmail.com",
    #     bank_account=acct_id
    # )
    #
    # print("two down")
    #
    # recip = recipient.id
    #
    # transfer = stripe.Transfer.create(
    #     amount=1000,  # amount in cents, again
    #     currency="usd",
    #     recipient=recip,
    #     bank_account=acct_id,
    #     statement_descriptor="November Salary"
    # )
    #
    # print("all down")




    acct = stripe.Account.create(managed=True, country='US', external_account={
            'object': 'bank_account',
            'country': 'US',
            'currency': 'usd',
            'routing_number': '110000000',
            'account_number': '000123456789',
            },
        tos_acceptance={
            'date': 1487229377,
            'ip': "103.194.69.3",
        },
    )

    acct_id = acct.id


    print(acct_id)

    print("one down successful")

    stripe.Charge.create(
        amount=1000,
        currency="usd",
        source={
            'object': 'card',
            'number': '4000000000000077',
            'exp_month': 2,
            'exp_year': 2018
        },
        destination=acct_id
    )

    print("two down successful")

    account = stripe.Account.retrieve(acct_id)
    account.legal_entity.dob.day = 10
    account.legal_entity.dob.month = 1
    account.legal_entity.dob.year = 1986
    account.legal_entity.first_name = "Jenny"
    account.legal_entity.last_name = "Rosen"
    account.legal_entity.type = "individual"
    account.save()

    print("fourth down successful")

    # Re-fetch the account to see what its status is.
    print(stripe.Account.retrieve(acct_id))

    print("fifth down successful")

    stripe.Transfer.create(
        amount=400,
        currency="usd",
        recipient="self",
        stripe_account=acct_id
    )

    print("seventh down successful")


    return render(request,'checkout/thankyou.html')
















