from tutdb.serializers import QuestionSerializer, DashboardSerializer, UpdateQuestionResponseSerializer, UserResponseSerializer, QuestionResponseSerializer, MyEnrollmentSerializer, EnrollmentSerializer, QuestionDetailSerializer, OptionsSerializer
from .models import Question, UserResponse, Choice, Course, Enrollment, Session
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListAPIView
from authapp.models import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        user = request.user
        serializer = DashboardSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CoursesAPIView(APIView):
    def get(self, request, format=None, **kwargs):
        user = request.user
        all_enrollments = User.objects.get(user=user).enrollments.all()
        all_faculty_courses = Course.objects.filter(faculty=user)


class CourseQuestions(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, course_slug, session, format=None):
        print(session)
        course_questions = Question.objects.filter(session__slug=session, course__slug=course_slug)
        serializer = QuestionSerializer(course_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionListApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination

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



# LOGIC FOR ENROLLING FOR A COURSE
class ListStudentEnrollment(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user_id = User.objects.get(email=self.request.user)
        all_enrollments = Enrollment.objects.filter(user=self.request.user)
        serializer = MyEnrollmentSerializer(all_enrollments, many=True)
        data = {"Number of Enrolled Courses": Enrollment.objects.filter(user_id=user_id).count()}
        data.update({"enrollments": serializer.data})
        return Response(data, status=status.HTTP_200_OK)

class EnrollStudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_slug):
        # Get the course object
        try:
            course = Course.objects.get(slug=course_slug).id
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user is already enrolled in the course
        if Enrollment.objects.filter(user=request.user, course=course).exists():
            return Response({"error": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

        # Create enrollment
        enrollment_data = {'user': request.user.id, 'course': course}
        serializer = EnrollmentSerializer(data=enrollment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# LOGIC FOR QUIZ
class QuestionResponseCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionResponseSerializer
        return QuestionSerializer

    def get_queryset(self):
        session_year= self.kwargs['session']
        print(self.kwargs['session'])
        session = Session.objects.get(slug=session_year)
        course_slug = self.kwargs['course_slug']
        course = Course.objects.get(slug=course_slug)
        return Question.objects.filter(course=course, session=session)


class UpdateQuestionResponseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None, **kwargs):
        user = request.user
        session_year = self.kwargs['session']
        session = Session.objects.get(slug=session_year)
        course_slug = self.kwargs['course_slug']
        course = Course.objects.get(slug=course_slug)

        serializer = UpdateQuestionResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_items_data = serializer.validated_data.get('items', [])
        print(serializer_items_data)

        for item in serializer_items_data:
            try:
                question = Question.objects.get(id=item['question_id'])
                selected_choice = item.get('selected_choice')
                print(selected_choice, question, course, session)
                user_response = UserResponse.objects.get(user=user, question=question, course=course, session=session)
                selected_choice_id = Choice.objects.get(text=selected_choice)
                user_response.selected_choice = selected_choice_id
                if user_response.selected_choice == user_response.question.answer:
                    user_response.is_correct = True
                else:
                    user_response.is_correct = False
                user_response.save()
            except UserResponse.DoesNotExist:  # Catch specific exception
                user_response = UserResponse.objects.create(user=user, question=question, selected_choice_id=selected_choice_id, course=course, session=session)
        user_responses = UserResponse.objects.filter(user=user, course=course, session=session)
        new_serializer = UserResponseSerializer(user_responses, many=True)
        return Response(new_serializer.data, status=status.HTTP_200_OK)

    
    # def delete(self, request, format=None, **kwargs):
    #     cart_id = kwargs.get("cart_id")
    #     cartitems = Cartitems.objects.filter(cart=cart_id)
    #     serializer = CreateItemsSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer_items_data = serializer.validated_data.get('items', [])
    #     for item in serializer_items_data:
    #         try:
    #             food = Food.objects.get(id=item['food_id'])
    #             cartitem = Cartitems.objects.get(cart=cart_id, Food=food)
    #             cartitem.delete()
    #         except:
    #             return Response("OOps", status=status.HTTP_400_BAD_REQUEST)
    #     new_serializer = CartItemSerializer(cartitems, many=True)
    #     return Response(new_serializer.data, status=status.HTTP_200_OK)
