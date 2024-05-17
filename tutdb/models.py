from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


YEAR = (
    ("Year 1", "Year 1"),
    ("Year 2", "Year 2"),
    ("Year 3", "Year 3"),
    ("Year 4", "Year 4"),
    ("Year 5", "Year 5")
)

class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    year = models.CharField(choices=YEAR, max_length=100)
    code = models.CharField(max_length=100)
    code_slug = models.SlugField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Session(models.Model):
    session = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.session
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

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
    answer = models.CharField(max_length=1)
    question_number = models.IntegerField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.question
    

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
