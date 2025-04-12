def create_initial_data():
    from .models import Machine, Warning, Case, User  # Moved imports here to avoid circular import

    # Initial machines
    initial_machines = [
        {
            "name": "Paint Machine",
            "priority": 1,
            "model": "CAT",
            "location": "Warehouse A",
            "last_service": "2023-01-01",
            "status": "fault",
            "manufacturer": "Caterpillar Inc.",
            "unique_machine_id": "PM-001"
        },
        {
            "name": "Cutting Machine",
            "priority": 2,
            "model": "Komatsu",
            "location": "Site B",
            "last_service": "2023-02-01",
            "status": "ok",
            "manufacturer": "Komatsu Ltd.",
            "unique_machine_id": "CM-002"
        },
        {
            "name": "Fire Machine",
            "priority": 3,
            "model": "Liebherr",
            "location": "Site C",
            "last_service": "2023-03-01",
            "status": "fault",
            "manufacturer": "Liebherr Group",
            "unique_machine_id": "FM-003"
        },
        {
            "name": "Shaping Machine",
            "priority": 4,
            "model": "Toyota",
            "location": "Warehouse B",
            "last_service": "2023-04-01",
            "status": "warning",
            "manufacturer": "Toyota Industries",
            "unique_machine_id": "SM-004"
        },
    ]
    for machine_data in initial_machines:
        Machine.objects.get_or_create(**machine_data)

    # Initial warnings
    initial_warnings = [
        {"code": "LOW_PAINT", "description": "Low Paint Level"},
        {"code": "BLADE_MISALIGN", "description": "Blade Misalignment"},
        {"code": "OVERHEAT", "description": "Overheating"},
        {"code": "MAINT_REQ", "description": "Maintenance Required"},
    ]
    warning_objects = {}
    for warning_data in initial_warnings:
        warning, _ = Warning.objects.get_or_create(**warning_data)
        warning_objects[warning.code] = warning

    # Assign supported warnings to machines
    for machine in Machine.objects.all():
        if machine.unique_machine_id == "PM-001":  # Paint Machine
            machine.supported_warnings.add(warning_objects["LOW_PAINT"])
        elif machine.unique_machine_id == "CM-002":  # Cutting Machine
            machine.supported_warnings.add(warning_objects["BLADE_MISALIGN"])
        elif machine.unique_machine_id == "FM-003":  # Fire Machine
            machine.supported_warnings.add(warning_objects["OVERHEAT"])
        elif machine.unique_machine_id == "SM-004":  # Shaping Machine
            machine.supported_warnings.add(warning_objects["MAINT_REQ"])
        machine.save()

    # Assign active warnings to machines
    for machine in Machine.objects.filter(status="warning"):
        if machine.unique_machine_id == "SM-004":  # Example: Shaping Machine
            machine.active_warnings.add(warning_objects["MAINT_REQ"])
        machine.save()

    # Initial cases
    initial_cases = [
        {
            "title": "Paint Machine Repair",
            "technician_note": "Replace paint nozzle.",
            "repair_note": "Nozzle replaced successfully.",
            "active": True,
            "technician_id": User.objects.filter(username="technician1").first().id if User.objects.filter(username="technician1").exists() else None,  # Check user existence
            "machine_id": Machine.objects.filter(unique_machine_id="PM-001").first().id if Machine.objects.filter(unique_machine_id="PM-001").exists() else None,  # Check machine existence
        },
        {
            "title": "Cutting Machine Maintenance",
            "technician_note": "Check blade alignment.",
            "repair_note": "Blade aligned properly.",
            "active": False,
            "technician_id": User.objects.filter(username="technician2").first().id if User.objects.filter(username="technician2").exists() else None,  # Check user existence
            "machine_id": Machine.objects.filter(unique_machine_id="CM-002").first().id if Machine.objects.filter(unique_machine_id="CM-002").exists() else None,  # Check machine existence
        },
    ]
    for case_data in initial_cases:
        if case_data["technician_id"] and case_data["machine_id"]:  # Ensure both IDs are valid
            Case.objects.get_or_create(
                title=case_data["title"],
                technician_id=case_data["technician_id"],
                machine_id=case_data["machine_id"],
                defaults={
                    "technician_note": case_data["technician_note"],
                    "repair_note": case_data["repair_note"],
                    "active": case_data["active"],
                }
            )
