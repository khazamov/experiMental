__author__ = 'okhaz'

from Mitlib.models import Question, Choice

from django.test import TestCase

import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test import Client
from django.test.utils import setup_test_environment

setup_test_environment()


def createquestion(_question_text, _days):
    q = Question(question_text = _question_text, pub_date = timezone.now() + datetime.timedelta(days = _days))
    return q





class QuestionTest(TestCase):

    client = Client()

    def test_IndexViewWithOutQuestions(self):
        quest = createquestion("Future questions?", 30)
        quest.save()
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'No questions')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])


    #def test_IndexViewWithPastQuestion(self):
    #    question =  createquestion("Coney Island Baby",-30)
    #    response = self.client.get(reverse('index'), question.id)
    #    self.assertEqual(response.status_code,200)
    #    self.assertQuerysetEqual(response.context['latest_question_list'],['Coney Island Baby'])



    def test_IndexViewWithFutureQuestion(self):
        quest = createquestion("Future questions?", 30)
        quest.save()
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[])




    def test_DetailViewWithFutureQuestion(self):
         quest = createquestion("Future questions?", 30)
         quest.save()
         response = self.client.get(reverse('detail', args  = (quest.id,)))
         self.assertEqual(response.status_code, 404)
