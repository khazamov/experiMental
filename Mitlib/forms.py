from django import forms
class MyForm(forms.Form):
	content = forms.CharField(max_length = 256)

