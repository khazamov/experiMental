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
from MyForms import Myform
import hotshot
import os
import time
import settings
import tempfile
import re

ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']



try:
    PROFILE_LOG_BASE = settings.BASE_DIR + settings.PROFILE_LOG_BASE
except:
    PROFILE_LOG_BASE = tempfile.gettempdir()




def profile(log_file):
    """Profile some callable.

    This decorator uses the hotshot profiler to profile some callable (like
    a view function or method) and dumps the profile data somewhere sensible
    for later processing and examination.

    It takes one argument, the profile log name. If it's a relative path, it
    places it under the PROFILE_LOG_BASE. It also inserts a time stamp into the
    file name, such that 'my_view.prof' become 'my_view-20100211T170321.prof',
    where the time stamp is in UTC. This makes it easy to run and compare
    multiple trials.
    """

    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def _outer(f):
        def _inner(*args, **kwargs):
            # Add a timestamp to the profile output when the callable
            # is actually called.
            (base, ext) = os.path.splitext(log_file)
            base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
            final_log_file = base + ext

            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()
            return ret

        return _inner
    return _outer

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



def index(request):

    return render(request,'Mitlib/index.html')


class ResultView(generic.DetailView):
    model = Question
    template_name = 'Mitlib/result.html'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'Mitlib/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

#@profile("traderesult.prof")
def traderesult(request):

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
             DM = Trader('Yahoo', to_datetime(date_start), to_datetime(date_end), int(cash))
             DM.find_events_wband()
             DM.process_data()
             DM.run()
             DM.computestats()
             sDaily_portfolio_return = json.dumps(DM.daily_portfolio_return.tolist())
             sDaily_fund_return = json.dumps(DM.daily_spy_return.tolist())
             sOutput_dates = json.dumps(DM.output_dates())
             return render(request, 'Mitlib/traderesult.html', {'daily_fund_return':sDaily_fund_return, 'daily_portfolio_return':sDaily_portfolio_return, 'output_dates':sOutput_dates })
    else:

            form = Myform()
    return render(request, 'Mitlib/traderesult.html', {'form':form})


def result(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    re = requestContext(request, {'question': p})
    t = loader.get_template('Mitlib/result.html')
    return HttpResponse(t.render(re))








