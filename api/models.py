from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .initial_data import create_initial_data

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.status

class Case(models.Model):
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE, blank=True, null=True, related_name="machine")
    technician = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    technician_note = models.TextField()
    technician_image = models.ImageField(upload_to='image/', blank=True, null=True)
    repair_note = models.TextField()
    repair_image = models.ImageField(upload_to='image/', blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True)

class Warning(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.code}: {self.description}"

class Machine(models.Model):
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('warning', 'WARNING'),
        ('fault', 'FAULT')
    ]
    current_case = models.ForeignKey('Case', on_delete=models.CASCADE, blank=True, null=True, related_name="current_case")
    person = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='ok',
        verbose_name='status type')
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    last_service = models.DateField(default='2000-01-01')
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    unique_machine_id = models.CharField(max_length=100, unique=True)
    supported_warnings = models.ManyToManyField(Warning, related_name='supported_machines', blank=True)
    active_warnings = models.ManyToManyField(Warning, related_name='active_machines', blank=True)

    class Meta:
        ordering = ['name']

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, to_field='unique_machine_id', related_name='tasks')
    assigned_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    completed_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    def __str__(self):
        return f"Task created by {self.creator.username} for {self.machine.name} on {self.assigned_date} - Status: {self.status}"

@receiver(post_migrate)
def populate_initial_machines(sender, **kwargs):
    if sender.name == 'api':  # Ensure this runs only for the 'api' app
        create_initial_data()
        # Create groups based on ROLE_CHOICES
        for role, _ in Profile.ROLE_CHOICES:
            Group.objects.get_or_create(name=role)