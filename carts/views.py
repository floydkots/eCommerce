from django.shortcuts import render, redirect

from accounts.forms import LoginForm
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
    else:
        order_obj, order_created = Order.objects.get_or_create(cart=cart_obj)
    billing_profile = None
    login_form = LoginForm

    if request.user.is_authenticated():
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=request.user,
            email=request.user.email
        )
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form
    }
    return render(request, 'carts/checkout.html', context)
