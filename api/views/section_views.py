from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer, LessonSerializer, ProductSerializer, CourseSerializer, CourseSectionSerializer, PurchaseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Product, Course, CourseSection, Lesson,Purchase
from ..services import get_next_course_section_order 


class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = CourseSection.objects.all()
    serializer_class = CourseSectionSerializer

    def list(self, request):
        """List all course ."""
        sections = Course.objects.all()
        serializer = CourseSerializer()
        return Response(serializer.data)

    
    
class CourseSectionViewSet(viewsets.ViewSet):
    """
    API endpoints for managing Course Sections.
    """

    def list(self, request):
        """List all course sections."""
        sections = CourseSection.objects.all()
        serializer = CourseSectionSerializer(sections, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a single course section by ID."""
        section = get_object_or_404(CourseSection, pk=pk)
        serializer = CourseSectionSerializer(section)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"])
    def create_section(self, request):
        """Create a new course section."""
        serializer = CourseSectionSerializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save(order=get_next_course_section_order(serializer.validated_data["course"].id))
            return Response(CourseSectionSerializer(section).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update an existing course section."""
        section = get_object_or_404(CourseSection, pk=pk)
        serializer = CourseSectionSerializer(section, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a course section."""
        section = get_object_or_404(CourseSection, pk=pk)
        section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"])
    def update_section_orders(self, request):
        """
        Update the order of sections based on a provided list of section IDs.
        """
        section_ids = request.data.get("section_ids", [])
        if not section_ids:
            return Response({"error": "section_ids list is required"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for index, section_id in enumerate(section_ids):
                CourseSection.objects.filter(id=section_id).update(order=index)

        return Response({"message": "Section order updated successfully"})