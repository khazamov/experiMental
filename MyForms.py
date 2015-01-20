__author__ = 'okhaz'


from django import forms

class Myform(forms.Form):
    date_trader = forms.CharField( label='date_trader', max_length = 100 )

