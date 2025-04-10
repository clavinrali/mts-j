def create_initial_data():
    from .models import Machine, Warning  # Moved imports here to avoid circular import

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
        {"status": "oil low"},
        {"status": "no yarn"},
        {"status": "needle blunt"},
    ]
    for warning_data in initial_warnings:
        Warning.objects.get_or_create(**warning_data)
