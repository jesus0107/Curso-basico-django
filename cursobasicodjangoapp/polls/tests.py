import datetime


from django.test import TestCase
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):


    def setUp(self):
        self.question = Question(question_text="Quien es el mejor CD de platzi?")


    def test_was_published_recently_with_future_questions(self):
        """Was_published_recently returns False for question whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = self.question
        future_question.pub_date = time
        # future_question = Question(question_text = "Quien es el mejor CD de platzi", pub_date = time)
        self.assertIs(future_question.was_recently_published(), False)

    
    def test_was_published_recently_with_old_question(self):
        """was_published_recently returns False for question whose pub_date is older than 1 day"""
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = self.question
        old_question.pub_date = time
        self.assertIs(old_question.was_recently_published(), False)


    def test_was_published_recently_with_present_question(self):
        """was_published_recently returns True for question whose pub_date is not older than 1 day"""
        time = timezone.now()
        self.question.pub_date= time - datetime.timedelta(days=0, seconds=59, minutes=59, hours=23)
        self.assertIs(self.question.was_recently_published(), True)


class QuestionIndexViewTests(TestCase):
    pass

