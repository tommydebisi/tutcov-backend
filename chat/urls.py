from . import views
from django.urls import path


app_name = 'chat'

urlpatterns = [
    path('room/<slug:department>/', views.faculty_chat_room, name='course_chat_room'),
]