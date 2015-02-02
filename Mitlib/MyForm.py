from django import forms


class Myform(forms.Form):
	date_start = forms.CharField()
    date_end = forms.CharField()

