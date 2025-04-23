from django import forms
from django.contrib.auth.models import User

from .models import Employee


class EmployeeUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
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


# TODO 編集用フォームを作成
