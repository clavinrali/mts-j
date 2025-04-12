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
            Case.objects.get_or_create(**case_data)

    # Initial warnings
    initial_warnings = [
        {"status": "Low Paint Level"},
        {"status": "Blade Misalignment"},
        {"status": "Overheating"},
        {"status": "Maintenance Required"},
    ]
    warning_objects = {}
    for warning_data in initial_warnings:
        warning, _ = Warning.objects.get_or_create(**warning_data)
        warning_objects[warning.status] = warning

    # Assign warnings to machines with status "warning"
    for machine in Machine.objects.filter(status="warning"):
        if machine.unique_machine_id == "SM-004":  # Example: Shaping Machine
            machine.current_warnings.add(warning_objects["Maintenance Required"])
        # Add other conditions for specific machines if needed
        machine.save()
