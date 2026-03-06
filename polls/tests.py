from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse
from .views import IndexView

from datetime import timedelta

from .models import Question

def create_question(question_text, days):
    date = timezone.now() + timedelta(days=days)
    return Question.objects.create(text=question_text, pub_date=date)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_recent_question(self):
        recent_date = timezone.now() - timedelta(hours=5)
        question = Question(text="test question", pub_date = recent_date)
        self.assertIs(question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        old_date = timezone.now() - timedelta(days=Question.recent_days+1)
        question = Question(text="test question", pub_date=old_date)
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        future_date = timezone.now() + timedelta(days=30)
        question = Question(text="test question", pub_date = future_date)
        self.assertIs(question.was_published_recently(), False)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, IndexView.no_polls_message)

    def test_future_questions_not_displayed(self):
        create_question("future_question", 10)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, IndexView.no_polls_message)

    def test_past_question_displayed(self):
        past_question = create_question("past_question", -1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [past_question])

    def test_past_and_future_questions(self):
        past_question = create_question("past_question", -1)
        create_question("future question", 1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [past_question])

    def test_lot_past_questions_displayed_within_offset(self):
        """checks if displayed less or equal questions within offset. Not more than offset"""
        questions_amount = 10
        offset = IndexView.queryset_offset
        questions = []
        for i in range(questions_amount):
            question = create_question(f"past question {i}", days=-i)
            questions.append(question)
        response = self.client.get(reverse("polls:index"))
        response_question_list = response.context["latest_question_list"]
        self.assertLessEqual(len(response_question_list), offset)



