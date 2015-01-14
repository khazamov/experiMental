__author__ = 'okhaz'

from Mitlib.models import Question, Choice
from django.test import TestCase
import datetime
from django.utils import timezone
from django.test import Client
from django.test.utils import setup_test_environment

setup_test_environment()


def createquestion(_question_text, _days):
    q = Question(question_text = _question_text, pub_date = timezone.now() + datetime.timedelta(days = _days))
    return q





class QuestionTest(TestCase):

 client = Client()

 def TestIndexViewWithOutQuestions(self):
     response = self.client.get(reverse('index'))
     self.assertEqual(response.status_code,200)
     self.assertContains(response, 'no questions')
     self.assertQuerysetEqual(response.context['latest_question_list'])


 def TestIndexViewWithPastQuestion(self):
     question =  createquestion("Coney Island Baby, kapish?",-30)
     response = self.client.get(reverse('index'))
     self.assertEqual(response.status_code,200)
     self.assertEqual(response.context['latest_question_list'],['<Coney Island Baby, kapish?>'])



 def TestIndexViewWithFutureQuestion(self):
    quest = createquestion("Future questions?", 30)
    response = self.client.get(reverse('index'))
    self.assertEqual(quest.context['latest_question_list'], [])




 def TestDetailViewWithFutureQuestion(self):
    quest = createquestion("Future questions?", 30)
    response = self.client.get(reverse('detail'))
    self.assertQuerySetEqual(response['latest_question_list'], [])






