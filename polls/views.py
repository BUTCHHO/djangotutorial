from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.views import generic, View
from django.shortcuts import render

from common.constants import Message
from common.shortcuts import failure_json_response, success_json_response

from .models import Question, Choice
from .forms import ChoiceCreationForm, QuestionCreationForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    extra_context = {"no_polls_message": Message.POLLS_NO_POLLS_AVAILABLE}

    queryset_offset = 5

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")[:IndexView.queryset_offset]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    extra_context = {"no_choice_message": Message.POLLS_NO_CHOICE_AVAILABLE}

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
        model = Question
        template_name = "polls/results.html"

class VoteView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        try:
            choice_id = request.POST["choice"]
            choice = get_object_or_404(Choice, pk=choice_id)
            if choice.question.is_pub_date_future():
                return failure_json_response(Message.POLLS_NO_POLLS_AVAILABLE, status=404)
        except KeyError:
            return failure_json_response(Message.POLLS_NO_CHOICE_MADE)
        choice.votes = F("votes") + 1
        choice.save()
        return success_json_response()

class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        question_creation_form = QuestionCreationForm()
        choice_creation_form = ChoiceCreationForm()
        context_data={
            'question_form': question_creation_form,
            'choice_form': choice_creation_form
        }
        return render(request, 'polls/create_question.html', context=context_data)



