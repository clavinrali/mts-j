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
    path("machine/<int:mid>/info/", views.machine_info_page, name="machine_info_page"),  # Update to point to the correct view
    path("case_creation/<int:mid>/", views.case_creation_page, name="case_creation_page"),
    path("statistics/", views.statistics_page, name="statistics"),
]