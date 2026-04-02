from django import forms
from django.contrib.auth.forms import AuthenticationForm

# 🔐 Login Form (ADD THIS)
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))

# 🚗 Your Existing Form (KEEP THIS)
class AccidentForm(forms.Form):
    VEHICLE_CHOICES = [
        ('', '-- Enter vehicle type --'),
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Truck', 'Truck'),
    ]

    FACTOR_CHOICES = [
        ('', '-- Enter accident factor --'),
        ('Speeding', 'Speeding'),
        ('Road Condition', 'Road Condition'),
        ('Road Bumps', 'Road Bumps'),
        ('Human Error', 'Human Error'),
    ]

    SEVERITY_CHOICES = [
        ('', '-- Enter severity --'), 
        ('Injury', 'Injury'),
        ('Death', 'Death'),
    ]

    TIME_CHOICES = [
        ('', '-- Enter time of accident --'),
        ('Day', 'Day'),
        ('Night', 'Night'),
    ]

    vehicle = forms.ChoiceField(
    choices=VEHICLE_CHOICES,
    widget=forms.Select(attrs={'class': 'form-control'})
)

    factor = forms.ChoiceField(choices=FACTOR_CHOICES)
    severity = forms.ChoiceField(choices=SEVERITY_CHOICES)
    time = forms.ChoiceField(choices=TIME_CHOICES)
