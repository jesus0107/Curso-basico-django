from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Question, Choice



# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list
#     })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """Return the last five published question"""
        response = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        return response


# def details(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/details.html", {
#         "question": question,
#     })

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

    def get_queryset(self):
        """Excludes any question arent published yet"""
        response = Question.objects.filter(pub_date__lte=timezone.now())
        return response

        
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {
        "question": question
    })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # 
    except (KeyError, Choice.DoesNotExist) as err:
        return render(request, "polls/details.html",{            
            "question": question,
            "error_message": "Porfavor selecciona un opcion"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))