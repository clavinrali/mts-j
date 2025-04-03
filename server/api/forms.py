from django import forms
from .models import Case, Machine

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['technician', 'machine', 'title', 'technician_note', 'technician_image']

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'priority', 'location', 'model', 'last_service', 'warnings']