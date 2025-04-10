from django.shortcuts import render

# Create your views here.

def login(request):
    """Render the login page. Redirect authenticated users to the home page."""
    ctx = {
    }
    return render(request, "login.html", context=ctx)

def manager_dashboard(request):
    """Render the manager dashboard."""
    ctx = {
    }
    return render(request, "manager_dashboard.html", context=ctx)
