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
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.contrib.auth.decorators import login_required
from Mitlib.models import Question, Choice
from Mitlib.forms import MyForm
from django.utils import timezone
from django.test import client


class IndexView(generic.ListView):
	template_name = ('polls/index.html')
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]


class ResultView(generic.DetailView):
	model = Question
	template_name = 'polls/result.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())



# def index(request):
# latest_question_list  = Question.objects.order_by('-pub_date')[:5]
#	template = loader.get_template('polls/index.html')
#	context = RequestContext(request, {'latest_question_list':latest_question_list})
#	return HttpResponse(template.render(context))


#@csrf_exempt
#def detail(request,question_id):
#	p = get_object_or_404(Question, pk = question_id)
#	choice = get_object_or_404(Choice)
#	return render(request, 'polls/detail.html',{'question':p})


#@csrf_exempt
#def result(request, question_id):
#	question = get_object_or_404(Question, pk = question_id)#
#	return render(request, 'polls/result.html', {'question':question})

@csrf_exempt
def votes(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExists):
		return render(request, 'polls/detail.html',
					  {'question': p, 'error_message': 'You didn\'t select a choice'})
	else:

		selected_choice.votes += 1
		selected_choice.save()
	return HttpResponseRedirect(reverse('result', args=(p.id)))
