from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("statistic/", views.statistic, name="statistic"), # Statistics page
    path("create_user/", views.create_user, name="create_user"), # Create User Page ***
    path("employees/", views.get_employees, name="get_employees"), # Select Employee
    path("employees/by_role/", views.get_employees_by_role, name="get_employees_by_role"), # Fetch employees by role
    path("machine/", views.get_machines, name="get_machines"), # Manager Dashboard Page
    path("machine/create/", views.create_machine, name="create_machine"), # New machine creation page
    path("machine/user/<int:uid>/", views.get_machines_by_user, name="get_machines_by_user"), # Technician Dashboard Page
    path("machine/<int:mid>/", views.machine_details, name="machine_details"), # Machine Info Page
    path("machine/<int:mid>/case/", views.get_machine_cases, name="get_machine_cases"), # Machine Info Page
    path("machine/<int:mid>/delete/", views.delete_machine, name="delete_machine"), # Machine Delete page ***
    path("machine/<int:mid>/set_warning/", views.set_warning, name="set_warning"), # Machine Info Page
    path("machine/<int:mid>/delete_warning/<int:wid>/", views.delete_warning, name="delete_warning"), # Machine Info Page
    path("machine/<int:mid>/set_employee/<int:eid>/", views.set_employee, name="set_employee"), # Select Employee
    path("machine/<int:mid>/active_warnings/", views.active_warnings, name="active_warnings"), # Fetch active warnings
    path("machine/<int:mid>/change_status/", views.change_machine_status, name="change_machine_status"), # Change Machine Status
    path("case/", views.get_cases, name="get_cases"), # Case History Page
    path("case/create/", views.create_case, name="create_case"), # Case Creation Page
    path("case/<int:cid>/", views.case_details, name="case_details"), # Case Display dashboard
    path("case/<int:cid>/close/", views.case_close, name="case_close"), #
    path("case/<int:cid>/add_comment/", views.add_comment, name="add_comment"), # Add Comment Page ***
    path("task/set/", views.set_task, name="set_task"), # Assign Task
    path("tasks/assigned/", views.get_assigned_tasks, name="get_assigned_tasks"), # Fetch tasks assigned to current user
]