from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from .forms import ContactForm


def home_page(request):
    context = {
        "title": "Home",
        "content": "Welcome to the homepage",
    }
    if request.user.is_authenticated():
        context['premium_content'] = 'Premium Content'
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title": "About Page",
        "content": "Welcome to the about page"
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "Welcome to the contact page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == 'POST':
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, 'contact/view.html', context)
