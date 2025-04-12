from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from api.models import Machine

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

def machine_info(request, mid):
    if request.user.is_authenticated:
        try:
            machine = Machine.objects.get(id=mid)
            context = {
                "machine": machine,
                "warnings": machine.current_warnings.all(),
                "cases": machine.machine.all(),  # Related cases
            }
            return render(request, "machine_info_page.html", context)
        except Machine.DoesNotExist:
            return redirect('machine:dashboard')  # Redirect if machine not found
    return redirect('machine:login')
