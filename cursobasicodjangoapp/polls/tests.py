import datetime


from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, days):
    """Create a question with de given "question_text", and published the given 
    number of days offset to now (negative for questions published in the past, positive dor question that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date = time)


class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """ If no questiuons exists, an appropriate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avalible")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_dont_show_future_question(self):
        """Dont show questions with pub_date is in the future"""
        future_question = create_question("Quien es el mejor Cd de platzi?", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avalible")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self):
        """Show questions with pub_date is in the past"""
        past_question = create_question("Quien es el mejor Cd de platzi?", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])

    def test_two_past_questions(self):
        """The questions index page may display multiple questions """
        past_q1= create_question("Question 1", days=-10)
        past_q2= create_question("Question 2", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_q1, past_q2])

    def test_future_and_past_questions(self):
        """Even if both past and future questions exist, only past questions are displayed"""
        past_q= create_question("Question 1", days=-10)
        future_q= create_question("Question 2", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_q])

    def test_two_future_questions(self):
        future_q1= create_question("Question 1", days=10)
        future_q2= create_question("Question 2", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avalible")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """ The detail view of a question with pub_date in the future returns a 404 error not found"""
        future_question= create_question("Future Question", days=10)
        url = reverse("polls:details", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """The detail view with a questiond with a pub_date in the past displays the question text"""
        past_question= create_question("Past Question", days=-10)
        url = reverse("polls:details", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        self.assertEqual(response.status_code, 200)

        