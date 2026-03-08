from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Question, Choice
from django.db.models import F
from django.views import generic, View

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    no_polls_message = "No polls available."

    extra_context = {"no_polls_message": no_polls_message}

    queryset_offset = 5

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")[:IndexView.queryset_offset]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    no_choice_message = "No choices available for this question"
    extra_context = {"no_choice_message": no_choice_message}

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
        model = Question
        template_name = "polls/results.html"

class VoteView(View):
    vote_future_question_message = "Cant vote for future question."
    no_choice_made_message = 'You did not make choice'
    def post(self, request, question_id):
        try:
            choice_id = request.POST["choice"]
            choice = get_object_or_404(Choice, pk=choice_id)
            if choice.question.is_pub_date_future():
                return HttpResponse(VoteView.vote_future_question_message)
        except KeyError:
            question = get_object_or_404(Question, pk=question_id)
            return render(request,"polls/detail.html",{"question": question, "error_message":VoteView.no_choice_made_message})
        choice.votes = F("votes") + 1
        choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


