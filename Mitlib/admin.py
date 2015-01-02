from django.contrib import admin
from Mitlib.models import Question
from Mitlib.models import Choice


class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
          (None,               {'fields':['question_text']}), 
          ('Date information', {'fields':['pub_date'], 
             'classes':['collapse']}),
]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)


