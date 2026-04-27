from django.urls import path

from .views import quiz_view, animated_quiz_view, bench_press_guide_view

app_name = "main"

urlpatterns = [
    path("", quiz_view, name="quiz"),
    path("animated/", animated_quiz_view, name="animated_quiz"),
    path("guides/bench-press/", bench_press_guide_view, name="guide_bench_press"),
]
