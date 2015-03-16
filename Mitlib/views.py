import datetime as dt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
import pdb
from Mitlib.models import Question, Choice
from Mitlib.simulator import Trader
import json
from dier import Dier
from MyForms import Myform
import re
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

def insertDT(input_list):
        to_be_sorted = copy.deepcopy(input_list)
        for order_piece in to_be_sorted:
            tickDT = dt.date(int(order_piece[0]),int(order_piece[1]),int(order_piece[2]))
            order_piece[0] = tickDT
        return to_be_sorted




def to_datetime(arg,str='/'):
    if not arg:
        return False
    else:
        split_list = re.split(str, arg)
        datetime_temp = dt.datetime(int(split_list[2]), int(split_list[0]), int(split_list[1]), 16, 00)
        return datetime_temp



class IndexView(generic.ListView):

    template_name = ('Mitlib/index.html')
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]




class ResultView(generic.DetailView):
    model = Question
    template_name = 'Mitlib/result.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'Mitlib/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def traderesult(request):

    # pdb.set_trace()
    if request.method == 'POST':

    #    form = Myform(request.POST)
             date_start = request.POST['date_start']
             date_end =   request.POST['date_end']
             cash = request.POST['cash']
             #datasource = request.POST['data_source']
             # if request.POST['event_type'] == 'threshold':
             #    event_type = rstrategy.find_events
             # else:
             #    event_type = rstrategy.find_events_wband
             DM = Trader('orders.csv', 'Yahoo', to_datetime(date_start), to_datetime(date_end), int(cash))
             DM.find_events()
             DM.process_data()
             DM.run()
             DM.computestats()
             sDaily_portfolio_return = json.dumps(DM.daily_portfolio_return.tolist())
             sDaily_fund_return = json.dumps(DM.daily_spy_return.tolist())
             return render(request, 'Mitlib/traderesult.html', {'daily_fund_return':sDaily_fund_return, 'daily_portfolio_return':sDaily_portfolio_return })
    else:

            form = Myform()
    return render(request, 'Mitlib/traderesult.html', {'form':form})


def result(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    re = requestContext(request, {'question': p})
    t = loader.get_template('Mitlib/result.html')
    return HttpResponse(t.render(re))


def votes(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.GET['choice'])
    except (KeyError, Choice.DoesNotExists):
        re = requestContext(request, {'question': p, 'error_message': 'You didn\'t select a choice'})
        t = loader.get_template('Mitlib/detail.html')
        return HttpResponse(t.render(re))
    # request, 'Mitlib/detail.html',
    # )
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('result', args=(p.id)))






