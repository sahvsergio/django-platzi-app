

# Create your views here.
from django.http import HttpResponse#execeute an http response
from django.shortcuts import render#renders the template
from django.shortcuts import get_object_or_404
from .models import Question

def index(request):
    latest_question_list= Question.objects.all()
    return render(request,'polls/index.html',{'latest_question_list':latest_question_list
        })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html",{
        "question": question
    } )

def results(request, question_id):
    return HttpResponse(f'Estás viendo los resultados de la pregunta número {question_id}')


def vote(request, question_id):
    return HttpResponse(f'Estás viendo los votos número {question_id}')
