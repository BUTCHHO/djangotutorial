from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse
from .views import IndexView, DetailView, VoteView

from datetime import timedelta

from .models import Question, Choice

from accounts.models import User

from common.utils.test.login_client import login_client
from common.constants import Message, Result


def create_question(question_text, days):
    date = timezone.now() + timedelta(days=days)
    return Question.objects.create(text=question_text, pub_date=date, author=User.get_testificate_user())

def create_choice(question, text, votes):
     return Choice.objects.create(question=question, choice_text=text, votes=0)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_recent_question(self):
        recent_date = timezone.now() - timedelta(hours=5)
        question = Question(text="test question", pub_date = recent_date)
        self.assertTrue(question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        old_date = timezone.now() - timedelta(days=Question.recent_days+1)
        question = Question(text="test question", pub_date=old_date)
        self.assertFalse(question.was_published_recently())

    def test_was_published_recently_with_future_question(self):
        future_date = timezone.now() + timedelta(days=30)
        question = Question(text="test question", pub_date = future_date)
        self.assertFalse(question.was_published_recently())



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Message.POLLS_NO_POLLS_AVAILABLE)

    def test_future_questions_not_displayed(self):
        create_question("future_question", 10)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, Message.POLLS_NO_POLLS_AVAILABLE)

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

class QuestionDetailViewTests(TestCase):
    def test_future_question_details_not_displayed(self):
        future_question = create_question("future question", 10)
        response = self.client.get(reverse("polls:detail", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question_displayed(self):
        past_question = create_question("past_question", -10)
        response = self.client.get(reverse("polls:detail", args=(past_question.id,)))
        self.assertContains(response, past_question.text)

    def test_no_choice_message_displayed_if_no_choice(self):
        question = create_question("past question", -10)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, Message.POLLS_NO_CHOICE_AVAILABLE)
        self.assertIs(response.context['question'].choice_set.exists(), False)

    def test_choices_displayed_without_no_choice_message(self):
        question = create_question("past question", -10)
        choice_1 = create_choice(question, 'choice 1', 0)
        choice_2 = create_choice(question, "choice 2", 0)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertNotContains(response, Message.POLLS_NO_CHOICE_AVAILABLE)
        self.assertContains(response, choice_1.choice_text)
        self.assertContains(response, choice_2.choice_text)

class QuestionVoteViewTests(TestCase):
    def test_votes_increment(self):
        question = create_question('question', -10)
        choice = create_choice(question, 'choice', 0)
        login_client(self.client)
        self.client.post(reverse('polls:vote', args=(question.id,)),data={"choice":choice.id})
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 1)

    def test_votes_dont_increment_for_future_questions(self):
        question = create_question('question', 10)
        choice = create_choice(question, 'choice', 0)
        login_client(self.client)
        response = self.client.post(reverse('polls:vote', args=(question.id,)),data={"choice":choice.id})
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)
        self.assertContains(response, Message.POLLS_NO_POLLS_AVAILABLE, status_code=404)

    def test_error_message_is_displayed_if_no_choice_made(self):
        question = create_question("question", -1)
        choice = create_choice(question, 'choice', 0)
        login_client(self.client)
        response = self.client.post(reverse('polls:vote', args=(question.id,)))
        choice.refresh_from_db()
        self.assertEqual(choice.votes, 0)
        self.assertContains(response, Message.POLLS_NO_CHOICE_MADE)

    def test_unauthorized_error_message_if_vote_while_logged_out(self):
        question = create_question('question', -1)
        choice = create_choice(question, 'choice,', 0)
        response = self.client.post(reverse('polls:vote', args=(question.id,)),data={"choice":choice.id})
        choice.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(choice.votes, 0)
        response_after_redirect = self.client.get(response.url)
        self.assertContains(response_after_redirect, 'login')

class PollCreateViewTests(TestCase):
    def test_poll_is_created_if_fields_filled_correctly(self):
        question_text='smells like ...'
        choice_1_text='teen spirit'
        choice_2_text='lost cherry'
        data = {
            'text': question_text,
            'choice_text': [choice_1_text, choice_2_text]
        }

        login_client(self.client)
        response = self.client.post(reverse('polls:create'),data=data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {Result(): Result.SUCCESS})

        question = Question.objects.get(text=question_text)
        self.assertEqual(question.choice_set.count(), 2)

    def test_poll_is_not_created_if_question_text_unfilled(self):
        choices = []
        for i in range(Question.min_choices):
            choices.append(f"choice{i}")
        data = {
            'text': '',
            'choice_text': choices
        }
        login_client(self.client)
        response = self.client.post(reverse('polls:create'), data=data)
        self.assertJSONEqual(response.content, {Result():Result.FAILURE, Message(): Message.POLLS_INVALID_QUESTION_FIELD})
        self.assertIsNone(Choice.objects.filter(choice_text=choices[0]).first())
        self.assertIsNone(Choice.objects.filter(choice_text=choices[1]).first())


    def test_poll_is_not_created_if_not_enough_choices(self):
        choices_amount = Question.min_choices-1
        choices = []
        for i in range(choices_amount):
            choices.append(f"choice{i}")
        question_text = 'super question'
        data = {
            "text": question_text,
            "choice_text": choices
        }
        login_client(self.client)
        response = self.client.post(reverse('polls:create'), data=data)
        self.assertJSONEqual(response.content, {Result():Result.FAILURE, Message():Message.POLLS_LESS_THAN_ALLOWED_CHOICES})
        self.assertIsNone(Question.objects.filter(text=question_text).first())

