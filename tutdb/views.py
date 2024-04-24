from tutdb.api.serializers import QuestionSerializer
from .models import Question
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema


class QuestionListApiView(APIView):
    serializer_class = QuestionSerializer
    # @swagger_auto_schema(operation_description="Displays all questions available in the system.")
    @extend_schema(responses=QuestionSerializer, description="Displays all questions available in the system.")
    def get(self, request, format=None):
        all_questions = Question.objects.all()
        serializer = QuestionSerializer(all_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)