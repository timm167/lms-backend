from rest_framework import serializers
from core.models import Lesson, Assignment

#-----------------------------------------------------------#

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url']

#-----------------------------------------------------------#


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'max_score', 'pass_score']

#-----------------------------------------------------------#


#-----------------------------------------------------------#
# Display serializers
#-----------------------------------------------------------#

class AssignmentDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title']

#-----------------------------------------------------------#

class LessonDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title']

#-----------------------------------------------------------#