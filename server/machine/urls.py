from django.urls import path
from . import views

# Namespace for app-specific URL names
app_name = "machine"
urlpatterns = [
    path("", views.login, name="index"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("new_machine/", views.new_machine, name="new_machine"),
    path("machine/<int:mid>/info/", views.machine_info, name="machine_info"),  # Machine Info Page
]