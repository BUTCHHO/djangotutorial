from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.db.models import F

def index(request):
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = {'latest_question_list': latest_questions}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    choices = question.choice_set.all()
    result = dict()
    for choice in choices:
        result[choice.choice_text] = choice.votes
    return HttpResponse(f"The results of question with id {question_id}. {result}")

def vote(request, question_id):
    try:
        choice_id = request.POST["choice"]
    except KeyError:
        try:
            question = Question.objects.get(question_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request,"detail.html",{"question": question, "error_message":"You did not make choice"})
    try:
        choice = Choice.objects.get(pk=choice_id)
    except Choice.DoesNotExist:
        raise Http404("Choice does not exist")
    choice.votes = F("votes") + 1
    choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))