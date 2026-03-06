from django.test import TestCase
from django.utils import timezone

from datetime import timedelta

from .models import Question


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
