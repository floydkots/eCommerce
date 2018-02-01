import stripe

from django.conf import settings

from django.shortcuts import render

stripe.api_key = getattr(settings, 'STRIPE_API_KEY')
STRIPE_PUBLISHABLE_KEY = 'pk_test_Y8MMHpR0P7ynnNCmkP6gdFuw'


def payment_method_view(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'billing/payment-method.html', {
        'publish_key': STRIPE_PUBLISHABLE_KEY
    })
