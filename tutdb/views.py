from tutdb.api.serializers import QuestionSerializer, QuestionDetailSerializer, OptionsSerializer
from .models import Question
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


class CourseQuestions(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, course_code, session, format=None):
        print(session)
        course_questions = Question.objects.filter(session__slug=session, course__code_slug=course_code)
        serializer = QuestionSerializer(course_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionListApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer
    # @swagger_auto_schema(operation_description="Displays all questions available in the system.")
    @extend_schema(responses=QuestionSerializer, description="Displays all questions available in the system.")
    def get(self, request, format=None):
        all_questions = Question.objects.all()
        serializer = QuestionSerializer(all_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class QuestionDetailAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = QuestionDetailSerializer

    def get(self, request, uuid, format=None):
        question = Question.objects.get(uuid=uuid)
        serializer = QuestionDetailSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, uuid, format=None):
        score = 0 
        question = Question.objects.get(uuid=uuid)
        serializer = OptionsSerializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        picked_answer = serializer.validated_data['answer']
        if picked_answer == question.answer:
            score += 1

        return Response({"Sucess": "Answer Saved",
                         "score": score}, status=status.HTTP_200_OK)