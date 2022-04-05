from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from account.forms import RegistrationForm

# authentication function
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def register(request):
    if request.user.is_authenticated:
        return HttpResponse('You have authenticated and redirect to base url')
    else:
        form = RegistrationForm()
        if request.method == 'post' or request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid:
                form.save()
                return HttpResponse("Your Account has been created!")

    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'account/register.html', context)


def customerLogin(request):
    if request.user.is_authenticated:
        return HttpResponse("You are Log in")
    else:
        if request.method == 'post' or request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(
                request, username=username, password=password)
            if customer is not None:
                login(request, customer)
                return HttpResponse("You are logged in successfull")
            else:
                HttpResponse("404")
    context = {
        'title': 'Log In'
    }
    return render(request, 'account/login.html', context)
