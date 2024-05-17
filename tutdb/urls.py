from django.urls import path
from .views import QuestionListApiView, QuestionDetailAPIView, CourseQuestions, EnrollStudentAPIView


urlpatterns = [
    path("questions/all/", QuestionListApiView.as_view(), name="all-questions"),
    path("enroll/<str:course_slug>/", EnrollStudentAPIView.as_view(), name="enroll-course"),
    path("<uuid:uuid>/", QuestionDetailAPIView.as_view(), name='single-question'),
    path("<str:session>/<str:course_code>/", CourseQuestions.as_view(), name="course-questions"), 

]