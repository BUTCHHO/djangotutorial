from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.db.models import F
from django.views import generic

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
        model = Question
        template_name = "polls/results.html"

def vote(request, question_id):
    try:
        choice_id = request.POST["choice"]
    except KeyError:
        question = get_object_or_404(Question, pk=question_id)
        return render(request,"detail.html",{"question": question, "error_message":"You did not make choice"})
    choice = get_object_or_404(Choice, pk=choice_id)
    choice.votes = F("votes") + 1
    choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))