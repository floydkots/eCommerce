import stripe

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.utils.http import is_safe_url

from django.shortcuts import render

stripe.api_key = getattr(settings, 'STRIPE_API_KEY')
STRIPE_PUBLISHABLE_KEY = 'pk_test_Y8MMHpR0P7ynnNCmkP6gdFuw'


def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    return render(request, 'billing/payment-method.html',
                  {
                      'publish_key': STRIPE_PUBLISHABLE_KEY,
                      'next_url': next_url
                  })


def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        return JsonResponse({'message': 'Success! Your card was added.'})
    return HttpResponse('error', status=401)
