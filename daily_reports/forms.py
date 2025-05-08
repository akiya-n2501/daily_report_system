from django import forms


class DailyReportSearchForm(forms.Form):
    # キーワード検索
    keyword = forms.CharField(label="キーワード", required=False)
    # 日付指定
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="いつから"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="いつまで"
    )
