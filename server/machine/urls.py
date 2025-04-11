from django.urls import path
from . import views # Import views from the current app

# Namespace for app-specific URL names
app_name = "machine"
urlpatterns = [
    path("", views.login, name="index"),
    path("login/", views.login, name='login'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
]