from rest_framework import serializers
from tutdb.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField("get_all_options")
    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['id', 'uuid', 'question', 'options', 'picked_answer', 'answer', 'question_number']

    
    def get_all_options(self, obj):
        all_options = [obj.option_1, obj.option_2, obj.option_3, obj.option_4,]
        return all_options


class QuestionDetailSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField("get_all_options")
    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['question_number', 'question', 'options']

    
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