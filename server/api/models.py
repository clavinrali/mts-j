from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    WARNINGS_CHOICES = [
        ('oil low', 'Oil Low'),
        ('no yarn', 'No Yarn'),
        ('needle blunt', ' Needle Blunt')
    ]
    status = models.CharField(
        max_length=100,
        choices=WARNINGS_CHOICES,
        verbose_name='status type')

    def __str__(self):
        return self.status


class Machine(models.Model):
    STATUS_CHOICES = [
        ('ok', 'OK'),
        ('warning', 'WARNING'),
        ('fault', 'FAULT')
    ]
    current_case = models.ForeignKey('Case', on_delete=models.CASCADE, blank=True, null=True, related_name="current_case")
    technician = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='ok',
        verbose_name='status type')
    warnings = models.ManyToManyField(Warning, blank=True)
    name = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    last_service = models.DateField(default='2000-01-01')

    class Meta:
        ordering = ['name']