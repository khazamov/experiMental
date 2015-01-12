from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.generic.base import TemplateView
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404,render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from Mitlib.models import Question, Choice 
from Mitlib.forms import MyForm




def index(request):
	return HttpResponse("So awesome you came here!")	






def detail(request,question_id):
	p = get_object_or_404(Question, pk = question_id)
	return HttpResponse('This is question number %s detail' %question_id)



def results(request, question_id):
	response = "You are looking at the results of question %s. "
	return HttpResponse(response %question_id)


@csrf_exempt
def votes(request, vote_id):
	response = "You are looking at vote %s"
        return HttpResponse(response %vote_id)


