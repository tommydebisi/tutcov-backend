from django.urls import path
from .views import QuestionListApiView, QuestionDetailAPIView, CourseQuestions


urlpatterns = [
    path("all/", QuestionListApiView.as_view(), name="all-questions"),
    path("<uuid:uuid>/", QuestionDetailAPIView.as_view(), name='single-question'),
    path("courses/<str:course_code>/<str:session>/", CourseQuestions.as_view(), name="course-questions")

]