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
    name = forms.CharField(required=True, label="名前")
    department = forms.CharField(required=False, label="部署")
    username = forms.CharField(required=True, label="ユーザー名")
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

    # 名前の文字数のバリデーション
    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()  # 前後の空白を削除
        length = len(name)
        if length > 50:
            raise forms.ValidationError(
                f"名前は50文字以内で入力してください。（現在の文字数: {length}）"
            )
        return name

    # 部署の文字数のバリデーション
    def clean_department(self):
        department = self.cleaned_data.get("department", "").strip()  # 前後の空白を削除
        length = len(department)
        if length > 100:
            raise forms.ValidationError(
                f"部署は100文字以内で入力してください。（現在の文字数: {length}）"
            )
        return department

    # ユーザー名の文字数のバリデーション
    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()  # 前後の空白を削除
        length = len(username)
        if length > 50:
            raise forms.ValidationError(
                f"ユーザー名は50文字以内で入力してください。（現在の文字数: {length}）"
            )
        return username

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
    name = forms.CharField(required=True, label="名前")
    department = forms.CharField(required=False, label="部署")
    username = forms.CharField(required=True, label="ユーザー名")

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

    # 名前の文字数のバリデーション
    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()  # 前後の空白を削除
        length = len(name)
        if length > 50:
            raise forms.ValidationError(
                f"名前は50文字以内で入力してください。（現在の文字数: {length}）"
            )
        return name

    # 部署の文字数のバリデーション
    def clean_department(self):
        department = self.cleaned_data.get("department", "").strip()  # 前後の空白を削除
        length = len(department)
        if length > 100:
            raise forms.ValidationError(
                f"部署は100文字以内で入力してください。（現在の文字数: {length}）"
            )
        return department

    # ユーザー名の文字数のバリデーション
    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()  # 前後の空白を削除
        length = len(username)
        if length > 50:
            raise forms.ValidationError(
                f"ユーザー名は50文字以内で入力してください。（現在の文字数: {length}）"
            )
        return username

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
