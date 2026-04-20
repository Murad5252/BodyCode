from django.shortcuts import redirect, render

from .forms import QuizForm
from .program_generator import generate_program


def quiz_view(request):
    return render(request, "main/quiz.html")


def quiz_form_view(request):
    form = QuizForm()
    return render(request, "main/quiz_form.html", {"form": form})


def program_result_view(request):
    if request.method != "POST":
        return redirect("main:quiz_form")

    form = QuizForm(request.POST)
    if not form.is_valid():
        return render(request, "main/quiz_form.html", {"form": form})

    program = generate_program(form.cleaned_data)
    return render(request, "main/program_result.html", {"program": program})
