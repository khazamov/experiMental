from django import forms

class MyForm(forms.Form):

	content = forms.CharField(max_length = 256)
	date_start = forms.DateField()
	date_end   = forms.DateField()
	event =  forms.CharField(max_length = 256)



