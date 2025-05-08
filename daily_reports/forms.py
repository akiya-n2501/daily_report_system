from django import forms


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="いつから"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="いつまで"
    )
