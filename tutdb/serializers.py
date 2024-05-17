from rest_framework import serializers
from tutdb.models import Question, Session, Course, Enrollment, UserResponse, Choice


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField("get_all_options")
    session = serializers.StringRelatedField()
    answer = serializers.StringRelatedField()
    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['id', 'uuid', 'question', 'session', 'options', 'picked_answer', 'answer', 'question_number']

    
    def get_all_options(self, obj):
        all_options = [obj.option_1, obj.option_2, obj.option_3, obj.option_4,]
        return all_options


class QuestionDetailSerializer(serializers.ModelSerializer):
   
    options = serializers.SerializerMethodField("get_all_options")
    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['question_number', 'question', 'session', 'options']

    
    def get_all_options(self, obj):
        all_options = [obj.option_1, obj.option_2, obj.option_3, obj.option_4,]
        return all_options


class OptionsSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=1)

    def validate_answer(self, value):
        if value not in ['A', 'B', 'C', 'D']:
            raise serializers.ValidationError("Wrong option selected")
        elif value == "":
            raise serializers.ValidationError("You must select an option")
        return value
    

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class MyEnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField("get_course_name")
    user = serializers.SerializerMethodField("get_user_name")
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'course_name']

    def get_course_name(self, obj):
        return obj.course.name
    
    def get_user_name(self, obj):
        return obj.user.username.capitalize()
    
class UserResponseSerializer(serializers.ModelSerializer):
    is_correct = serializers.SerializerMethodField("check_accuracy")
    selected_choice = serializers.StringRelatedField()
    class Meta:
        model= UserResponse
        fields = ["question", "selected_choice", "is_correct"]        
    
    def check_accuracy(self, obj):
        if obj.selected_choice == obj.question.answer:
            return True


class QuestionResponseSerializer(serializers.ModelSerializer):
    items = UserResponseSerializer(many=True, read_only=True)

    class Meta:
        model = UserResponse
        fields = ['id', 'items']

    def create(self, validated_data):
        user = self.context['request'].user
        response_data = self.context.get('request').data.get('items', [])
        session_year = self.context['view'].kwargs['session']
        session = Session.objects.get(slug=session_year)
        course_slug = self.context['view'].kwargs['course_slug']
        course = Course.objects.get(slug=course_slug)
        for data in response_data:
            question = data.get('question_id')
            selected_choice = data.get('selected_choice')
            print(question, selected_choice)
            selected_choice_id = Choice.objects.get(text=selected_choice).id
            question_id = Question.objects.get(question_number=question).id
            # response = UserResponse.objects.create(user=user, question_id=question_id, selected_choice_id=selected_choice_id)
            response = UserResponse.objects.create(user=user, question_id=question_id, selected_choice_id=selected_choice_id, course=course, session=session)
        return response


class ItemSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_choice = serializers.CharField()


class UpdateQuestionResponseSerializer(serializers.Serializer):
    items = ItemSerializer(many=True)


    def create(self, validated_data):
        items_data = validated_data.get('items', [])
        created_items = []
        for item_data in items_data:
            # Assuming item_data contains 'product_id' and 'quantity'
            question_id = item_data.get('question_id')
            selected_choice = item_data.get('selected_choice')
            if question_id is not None and selected_choice is not None:
                # Create your item object here or perform any desired operations
                created_item = {
                    'question_id': question_id,
                    'selected_choice': selected_choice
                }
                created_items.append(created_item)
        return created_items

    
