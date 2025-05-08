from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Employee


# パスワード用のバリデーション regex: 正規表現
password_validator = RegexValidator(
    regex=r"^(?=.*[a-zA-Z])(?=.*\d).{8,}$",
    message="パスワードは英数字を含む8文字以上にしてください。",
)


class EmployeeUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50, required=True, label="ユーザー名")
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        validators=[password_validator],  # バリデーション適用
        label="パスワード",
    )

    class Meta:
        model = Employee
        fields = ["name", "email", "department", "username", "password"]
        labels = {
            "name": "名前",
            "email": "メールアドレス",
            "department": "部署",
        }

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
    username = forms.CharField(max_length=50, required=True, label="ユーザー名")
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        validators=[password_validator],  # バリデーション適用
        label="パスワード",
    )

    class Meta:
        model = Employee
        fields = ["name", "email", "department", "username", "password"]
        labels = {
            "name": "名前",
            "email": "メールアドレス",
            "department": "部署",
        }

    # userをformのインスタンスに追加するための設定
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

        # パスワードが空の場合はパスワードを更新しない
        if password:
            user.set_password(password)
        if commit:
            user.save()
            employee.save()
        return employee
