from rest_framework import serializers
from tutdb.models import Question, Enrollment, UserResponse


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField("get_all_options")
    session = serializers.StringRelatedField()
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
        for data in response_data:
            question_id = data.get('question_id')
            selected_choice_id = data.get('selected_choice')
            response = UserResponse.objects.create(user=user, question_id=question_id, selected_choice_id=selected_choice_id)
        return response

    
