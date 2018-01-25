from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }

    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    print(next_get, next_post, redirect_path)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request,
                            username=username,
                            password=password)
        # print(request.user.is_authenticated())
        if user is not None:
            # print(request.user.is_authenticated())
            login(request, user)
            print(redirect_path)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            # Return an 'invalid login' error message.
            print('Error')

    return render(request, 'accounts/login.html', context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        context['form'] = RegisterForm()
        user = get_user_model()
        new_user = user.objects.create_user(username, email, password)
        print(new_user)
    return render(request, 'accounts/register.html', context)
