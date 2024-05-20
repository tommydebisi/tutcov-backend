from typing import Iterable
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()
from django.conf import settings
from authapp.models import Faculty as MyFaculty, Department as MyDepartment


YEAR = (
    ("Year 1", "Year 1"),
    ("Year 2", "Year 2"),
    ("Year 3", "Year 3"),
    ("Year 4", "Year 4"),
    ("Year 5", "Year 5")
)

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Faculty(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

TAG_CHOICES = (
    ("New", "New"),
    ("Stale", "Stale")
)

class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    year = models.CharField(choices=YEAR, max_length=100)
    tag = models.CharField(choices=TAG_CHOICES, max_length=100, default="New")
    faculty = models.ForeignKey(MyFaculty, on_delete=models.CASCADE)
    department = models.ForeignKey(MyDepartment, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    code_slug = models.SlugField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Session(models.Model):
    session = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.session
    

    
class Choice(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Question(models.Model):
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to="question_images", blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    picked_answer = models.CharField(max_length=1, blank=True)
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.question


    

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return self.course.code


class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    # def save(self, *args, **kwargs):
    #     if self.selected_choice:
    #         if self.selected_choice == self.question.answer:
    #             self.is_correct = True
    #     super().save(*args, **kwargs)

class UserScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
