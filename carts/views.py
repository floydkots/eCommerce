from django.shortcuts import render, redirect

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
