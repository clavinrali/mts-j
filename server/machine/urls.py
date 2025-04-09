from django.urls import path
from . import views # Import views from the current app

# Namespace for app-specific URL names
app_name = "machine"
urlpatterns = [
    # GENERAL PAGES

    # Login page (renders the login form)
    path("", views.login, name="login"),
    path("login.html", views.login, name="login"),
    # Main dashboard/home page
    path("dashboard/manager_dashboard.html", views.manager_dashboard, name="manager_dashboard"),
]