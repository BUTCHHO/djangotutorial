from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Question


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
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404(f"Question with id {question_id} does not exist")
    return HttpResponse(f"The voting page for question {question} with id {question_id}")