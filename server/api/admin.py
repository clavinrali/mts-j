from django.contrib import admin
from .models import Profile,Machine,Task,Warning,Case


admin.site.register(Profile)
admin.site.register(Machine)
admin.site.register(Warning)
admin.site.register(Case)
admin.site.register(Task)