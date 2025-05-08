from django import forms
from django.contrib.auth.models import User

from .models import Employee


class EmployeeUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Employee
        fields = ["name", "email", "department", "username", "password"]

    def save(self, commit=True):
        employee = super().save(commit=False)
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = User.objects.create_user(username=username, password=password)
        employee.user = user
        if commit:
            employee.save()
        return employee


class EmployeeUserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Employee
        fields = ["name", "email", "department", "username", "password"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username

    def save(self, commit=True):
        employee = super().save(commit=False)
        user = employee.user
        user.username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
            employee.save()
        return employee
