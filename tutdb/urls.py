from django.urls import path
from .views import QuestionListApiView


urlpatterns = [
    path("all/", QuestionListApiView.as_view(), name="all-questions")
]