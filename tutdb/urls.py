from django.urls import path
from .views import QuestionListApiView, ListStudentEnrollment, QuestionDetailAPIView, CourseQuestions, UpdateQuestionResponseAPIView, QuestionResponseCreateAPIView,EnrollStudentAPIView


urlpatterns = [
    path("dashboard/", )
    path("questions/all/", QuestionListApiView.as_view(), name="all-questions"),
    path("questions/<str:session>/<str:course_slug>/", QuestionResponseCreateAPIView.as_view(), name="quiz"),
    path("questions/<str:session>/<str:course_slug>/change/", UpdateQuestionResponseAPIView.as_view(), name="quiz-update"),
    path("my-courses/", ListStudentEnrollment.as_view(), name="my-enrollments"),
    path("enroll/<str:course_slug>/", EnrollStudentAPIView.as_view(), name="enroll-course"),
    path("questions/<uuid:uuid>/", QuestionDetailAPIView.as_view(), name='single-question'),
    path("questions/all/<str:session>/<str:course_slug>/", CourseQuestions.as_view(), name="course-questions"), 

]