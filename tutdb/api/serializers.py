from rest_framework import serializers
from tutdb.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField("get_all_options")
    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['id', 'question', 'options', 'picked_answer', 'answer', 'question_number']

    
    def get_all_options(self, obj):
        all_options = [obj.option_1, obj.option_2, obj.option_3, obj.option_4,]
        return all_options
