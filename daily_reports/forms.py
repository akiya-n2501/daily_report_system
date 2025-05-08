from django import forms
from .models import DailyReportComment


class DailyReportCommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,  # Django の標準必須バリデーションを無効化
        widget=forms.Textarea(attrs={"placeholder": "コメントを入力してください"}),
    )

    class Meta:
        model = DailyReportComment
        fields = ['comment']

    # 外部からemployeeとdaily_reportをフォームのインスタンスから受け取れる設定
    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee', None)
        self.daily_report = kwargs.pop('daily_report', None)
        super().__init__(*args, **kwargs)

    # コメントの文字数のバリデーション
    def clean_comment(self):
        comment = self.cleaned_data.get('comment', "").strip()  # 前後の空白を削除
        if len(comment) < 1:
            raise forms.ValidationError("コメントは1文字以上で入力してください。")
        if len(comment) > 2000:
            raise forms.ValidationError("コメントは2000文字以内で入力してください。")
        return comment

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.employee:
            instance.employee_code = self.employee
        if self.daily_report:
            instance.daily_report_code = self.daily_report
        if commit:
            instance.save()
        return instance
