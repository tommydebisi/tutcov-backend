from tutdb.api.serializers import QuestionSerializer
from .models import Question
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class QuestionListApiView(APIView):
    def get(self, request, format=None):
        all_questions = Question.objects.all()
        serializer = QuestionSerializer(all_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)