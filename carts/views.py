from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart


def cart_home(request):
    cart, new = Cart.objects.new_or_get(request)

    return render(request, 'carts/home.html', {'cart': cart})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone")
            return redirect('cart:home')
        cart, new = Cart.objects.new_or_get(request)
        if product in cart.products.all():
            cart.products.remove(product)
        else:
            cart.products.add(product)
        request.session['cart_items'] = cart.products.count()
    return redirect('cart:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')

    billing_profile = None

    login_form = LoginForm
    guest_form = GuestForm
    guest_email_id = request.session.get('guest_email_id')

    if request.user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=request.user,
            email=request.user.email
        )
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(
            email=guest_email_obj.email
        )
    else:
        pass

    order_obj = None
    if billing_profile is not None:
        order_qs = Order.objects.filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True
        )
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            old_order_qs = Order.objects.exclude(
                billing_profile=billing_profile
            ).filter(
                cart=cart_obj,
                active=True
            )
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj = Order.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj
            )

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form
    }
    return render(request, 'carts/checkout.html', context)
