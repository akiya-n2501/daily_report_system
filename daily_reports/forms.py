from django import forms

from .models import DailyReportComment, DailyReport


# 日報コメントフォーム
class DailyReportCommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,  # Django の標準必須バリデーションを無効化
        widget=forms.Textarea(attrs={"placeholder": "コメントを入力してください"}),
    )

    class Meta:
        model = DailyReportComment
        fields = ["comment"]

    # 外部からemployeeとdaily_reportをフォームのインスタンスから受け取れる設定
    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop("employee", None)
        self.daily_report = kwargs.pop("daily_report", None)
        super().__init__(*args, **kwargs)

    # コメントの文字数のバリデーション
    def clean_comment(self):
        comment = self.cleaned_data.get("comment", "").strip()  # 前後の空白を削除
        length = len(comment)
        if length < 1:
            raise forms.ValidationError("コメントは1文字以上で入力してください。")
        if length > 2000:
            raise forms.ValidationError(
                f"コメントは2000文字以内で入力してください。（現在の文字数: {length}）"
            )
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


# 日報一覧画面 日付範囲検索
class DailyReportSearchForm(forms.Form):
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"}), label="いつから"
    )
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"}), label="いつまで"
    )
    keyword = forms.CharField(required=False, label="キーワード")


# 日報新規登録画面
class DailyReportForm(forms.ModelForm):

    class Meta:
        model = DailyReport
        fields = ["employee_code","job_description","reported_on"]
        labels = {"employee_code": "名前",
                  "job_description": "業務内容",
                  "reported_on": "日付",
                  }


    # def clean_job_description(self):
    #      job_description = self.cleaned_data.get("job_description")
    #      if len(job_description) > 2000:
    #         raise forms.ValidationError("業務内容は2000文字以内で入力してください。")
    #      return job_description


    def save(self, commit=True):
        daily_report = super().save(commit=False)
        if commit:
            daily_report.save()
        return daily_report

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['job_description']
        labels = {"job_description": "業務内容"}
