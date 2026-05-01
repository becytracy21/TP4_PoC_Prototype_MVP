from rest_framework import serializers
from .models import Boat, Course, Inscription

class BoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boat
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ['id', 'boat', 'course', 'resultat']
