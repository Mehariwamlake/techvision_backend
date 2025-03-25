from django.shortcuts import render

# Create your views here.

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import  CourseSection, Lesson
from ..services import get_next_course_section_order 


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def create(self, request, *args, **kwargs):
        """Create a lesson for a course section"""
        data = request.data
        section = CourseSection.objects.get(pk=data['section'])
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            lesson = serializer.save(section=section)
            return Response(
                {"message": f"Lesson {lesson.id} created successfully for section {section.id}."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)