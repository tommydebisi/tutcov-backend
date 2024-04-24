from django.urls import path
from .views import QuestionListApiView, QuestionDetailAPIView


urlpatterns = [
    path("all/", QuestionListApiView.as_view(), name="all-questions"),
    path("<uuid:uuid>/", QuestionDetailAPIView.as_view(), name='single-question')
]