from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from Mitlib.models import Question, Choice 
from Mitlib.forms import MyForm


class LoginRequiredMixin(object):
	@classmethod
	def as_view(cls, **initkwargs):
		view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
		return login_required(view)


@csrf_exempt
class MyFormView(View):
	initial = {'key':'value'}
	template_name = 'post/details.html'
	form_class = MyForm
	def get(self, request, *args, **kwargs):
		return HttpResponse('Hi')
#render(request, template_name, initial )
  
        
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
                
        	#if form.is_valid():
			#form processing
         		#return HttpResponseRedirect('/success/')
		return render(request, template_name, {'form':form})

def index(request):
	template_name = 'details.html'
	latest_questions  = Question.objects.all()
	context = {'latest_question_list':latest_questions}
        return render(request, template_name, context)


