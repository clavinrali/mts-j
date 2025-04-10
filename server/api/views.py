from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .models import Case, Machine, Comment

def index(request):
    ctx = {}
    return render(request, "index.html", context=ctx)

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        # get data from request
        # check if request is JSON
        data = json.loads(request.body)

        # check if data is empty
        if not data:
            return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

        # get username and password
        username = data.get("username")
        password = data.get("password")

        # try to authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful"}, status=200)
        else:
            return JsonResponse({"success": False, "message": "Invalid username or password"}, status=401)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def user_logout(request):
    return logout(request)

def statistic(request):
    if request.method == 'GET':
        # get all machines
        total_machines = Machine.objects.all().count()
        machines_ok = Machine.objects.filter(status="ok").count()
        machines_warn = Machine.objects.filter(status="warning").count()
        machines_fault = Machine.objects.filter(status="fault").count()
        # format statistics
        statistic = {
            "total_machines": total_machines,
            "machines_ok": machines_ok,
            "machines_warn": machines_warn,
            "machines_fault": machines_fault
        }
        return JsonResponse({"success": True, "message": statistic}, safe=False, status=200)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        is_staff = data.get("is_manager")

        # check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already exists"}, status=400)

        # create user
        user = User.objects.create_user(username=username, password=password, email=email, is_staff=is_staff)
        user.save()

        return JsonResponse({"success": True, "message": "User created successfully"}, status=201)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def get_employees(request):
    if request.method == 'GET':
        # get person employees
        employees = User.objects.filter(is_staff=False, is_superuser=False)
        employee_list = [{"id": employee.user.id, "username": employee.user.username} for employee in employees]
        return JsonResponse({"success": False, "message": employee_list}, safe=False, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def get_machines(request):
    if request.method == 'GET':
        # get all machines
        machines = Machine.objects.all()
        # format the machine list
        machine_list = [{"name": machine.name,
                         "last_service": machine.last_service,
                         "location": machine.location,
                         "priority": machine.priority,
                         "assigned": machine.person if machine.person else None,
                         "status": machine.status} for machine in machines]
        return JsonResponse({"success": True, "message": machine_list}, safe=False, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def create_machine(request):
    if request.method == 'POST':
        # get data from request
        data = json.loads(request.body)
        name = data.get("name")
        priority = data.get("priority")
        location = data.get("location")
        model = data.get("model")
        last_service = data.get("last_service")

        # check if machine already exists
        if Machine.objects.filter(name=name).exists():
            return JsonResponse({"success": False, "message": "Machine already exists"}, status=400)

        # create machine
        machine = Machine.objects.create(name=name, priority=priority, location=location, model=model, last_service=last_service)
        machine.save()

        return JsonResponse({"success": True, "message": "Machine created successfully"}, status=201)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def get_machines_by_user(request, uid):
    if request.method == 'GET':
        # get machines by user
        machines = Machine.objects.filter(person=uid)
        # format the machine list
        machine_list = [{"name": machine.name,
                         "last_service": machine.last_service,
                         "location": machine.location,
                         "priority": machine.priority,
                         "assigned": machine.person if machine.person else None,
                         "status": machine.status,
                         "current_case": machine.current_case if machine.current_case else None,
                         } for machine in machines]
        return JsonResponse({"success": True, "message": machine_list}, safe=False, status=200)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def machine_details(request, mid):
    if request.method == 'GET':
        # get machine
        machine = Machine.objects.get(id=mid)
        return JsonResponse({"success": True, "message": machine}, status=200)

def get_machine_cases(request, cid):
    if request.method == 'GET':
        # get machine cases
        machine = Machine.objects.get(id=cid)
        # format the machine cases
        case_list = [{"title": case.title,
                      "technician_note": case.technician_note,
                      "repair_note": case.repair_note,
                      "comments": case.comments.all(),
                      } for case in machine.current_case.all()]
        return JsonResponse({"success": True, "message": case_list}, safe=False, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def delete_machine(request, mid):
    if request.method == 'DELETE':
        # get machine
        machine = Machine.objects.get(id=mid)
        # delete machine
        machine.delete()

        return JsonResponse({"success": True, "message": "Machine deleted successfully"}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def add_warning(request, mid):
    if request.method == 'POST':
        # get machine
        machine = Machine.objects.get(id=mid)
        # create warning
        data = json.loads(request.body)
        status = data.get("status")

        # check if warning already exists
        if Warning.objects.filter(status=status).exists():
            return JsonResponse({"success": False, "message": "Warning already exists"}, status=400)

        # create warning
        warning = Warning.objects.create(status=status)
        machine.warnings.add(warning)
        # set machine status to warning
        machine.status = "warning"
        machine.save()

        return JsonResponse({"success": True, "message": "Warning added successfully"}, status=201)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def delete_warning(request, mid, wid):
    if request.method == 'DELETE':
        # get machine
        machine = Machine.objects.get(id=mid)
        # get warning
        warning = Warning.objects.get(id=wid)
        # delete warning
        machine.warnings.remove(warning)

        # check if machine has warnings
        if (machine.warnings.count() > 0):
            # set machine status to warning
            machine.status = "warning"
        else:
            # set machine status to ok
            machine.status = "ok"
        machine.save()

        return JsonResponse({"success": True, "message": "Warning deleted successfully"}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def set_employee(request, mid, eid):
    if request.method == 'POST':
        # get machine
        machine = Machine.objects.get(id=mid)
        # get employee
        employee = User.objects.get(id=eid)
        # set employee to machine
        machine.person = employee
        machine.save()

        return JsonResponse({"success": True, "message": "Employee set successfully"}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def get_cases(request):
    if request.method == 'GET':
        # get all cases
        cases = Case.objects.all()
        # format the case list
        case_list = [{"id": case.id} for case in cases]
        return JsonResponse({"success": True, "message": case_list}, safe=False, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def create_case(request):
    if request.method == 'POST':
        # get data from request
        data = json.loads(request.body)
        id_technician = data.get("id_technician")
        id_machine = data.get("id_machine")
        title = data.get("title")
        technician_note = data.get("technician_note")
        technician_image = data.get("technician_image")

        # check if case already exists
        if Case.objects.filter(title=title).exists():
            return JsonResponse({"success": False, "message": "Case already exists"}, status=400)

        # get person and machine
        person = User.objects.get(id=id_technician)
        machine = Machine.objects.get(id=id_machine)

        # create case
        case = Case.objects.create(person=person, machine=machine, title=title, technician_note=technician_note, technician_image=technician_image)
        case.active = True
        case.save()

        # set machine current case
        machine.current_case = case
        # set machine status to fault
        machine.status = "fault"
        machine.save()

        return JsonResponse({"success": True, "message": "Case created successfully"}, status=201)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def case_details(request, cid):
    if request.method == 'GET':
        # get case
        case = Case.objects.get(id=cid)
        return JsonResponse({"success": True, "message": case}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def case_close(request, cid):
    if request.method == 'POST':
        # get case
        case = Case.objects.get(id=cid)
        # close case
        case.active = False
        case.save()

        # update machine status
        machine = case.machine

        if (machine.warnings.count() > 0):
            # set machine status to warning
            machine.status = "warning"
        else:
            # set machine status to ok
            machine.status = "ok"
        machine.current_case = None
        machine.person = None
        machine.save()

        return JsonResponse({"success": True, "message": "Case closed successfully"}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def add_comment(request, cid):
    if request.method == 'POST':
        # get case
        case = Case.objects.get(id=cid)
        # create comment
        data = json.loads(request.body)
        user = User.objects.get(id=data.get("user"))
        text = data.get("text")

        comment = Comment.objects.create(user=user, text=text)
        case.comments.add(comment)
        case.save()

        return JsonResponse({"success": True, "message": "Comment added successfully"}, status=201)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)