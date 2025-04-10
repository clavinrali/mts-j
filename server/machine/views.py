from django.shortcuts import render, redirect
from api.models import Profile
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('machine:dashboard')
        else:
            return render(request, "login.html", {'error': 'Invalid username or password'})
    return render(request, "login.html")

def dashboard(request):
    ctx = {
    }
    return render(request, "manager_dash.html", context=ctx)
