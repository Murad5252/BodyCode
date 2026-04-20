from django.urls import path

from .views import program_result_view, quiz_form_view, quiz_view

app_name = "main"

urlpatterns = [
    path("", quiz_view, name="quiz"),
    path("quiz-form/", quiz_form_view, name="quiz_form"),
    path("program-result/", program_result_view, name="program_result"),
]
