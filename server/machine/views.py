from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout

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

def logout_view(request):
    logout(request)
    return redirect('machine:login')

def dashboard(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == 'Manager':
            template = "manager_dashboard.html"
        else:
            template = "gen_dashboard.html"
        return render(request, template)  # Ensure this renders the correct template
    return redirect('machine:login')

def new_machine(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == 'Manager':
        return render(request, "new_machine.html")
    return redirect('machine:login')
