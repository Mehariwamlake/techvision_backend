from django.contrib.auth.models import User
from rest_framework import serializers
from .models import  Course, CourseProduct, Product, CourseSection, Lesson,Purchase


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'status', 'created_at', 'updated_at']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'product', 'price', 'created_at', 'updated_at', 'chapa_session_id']

class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ['id', 'name', 'status', 'order', 'course', 'created_at', 'updated_at']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'youtube_video_id', 'order', 'status', 'section', 'created_at', 'updated_at']

class CourseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProduct
        fields = ['course', 'product', 'created_at', 'updated_at']