from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework.response import Response


from ..serializers import UserSerializer, LessonSerializer, ProductSerializer, CourseSerializer, CourseSectionSerializer, PurchaseSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Product, Course, CourseSection, Lesson,Purchase
from ..services import get_next_course_section_order 


class CourseListView(generics.ListAPIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
        
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_course(self, request, *args, **kwargs):
        # Create the course
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            course = serializer.save()
            # After creating the course, automatically create a section for it
            return Response(
                {"message": f"Course created successfully! Now, create sections for the course."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


    @action(detail=True, methods=['post'])
    def create_section(self, request, pk=None):
        """Automatically create a section for a specific course"""
        course = self.get_object()
        data = request.data
        data['course'] = course.id
        section_serializer = CourseSectionSerializer(data=data)
        if section_serializer.is_valid():
            section = section_serializer.save()
            return Response(
                {"message": f"Section {section.id} created successfully. Now, create lessons."},
                status=status.HTTP_201_CREATED
            )
        return Response(section_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def create_lesson(self, request, pk=None):
        """Create a lesson for a course section"""
        section = CourseSection.objects.get(pk=pk)
        data = request.data
        data['section'] = section.id
        lesson_serializer = LessonSerializer(data=data)
        if lesson_serializer.is_valid():
            lesson = lesson_serializer.save()
            return Response(
                {"message": f"Lesson {lesson.id} created successfully. Now, you can publish the course."},
                status=status.HTTP_201_CREATED
            )
        return Response(lesson_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish the course after sections and lessons are created"""
        course = self.get_object()
        course.status = 'public'  # Assuming 'public' means published
        course.save()
        return Response(
            {"message": f"Course {course.id} is now published!"},
            status=status.HTTP_200_OK
        )
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Retrieve the details of a course, including sections and lessons"""
        try:
            course = get_object_or_404(Course, pk=pk)
            # Get sections associated with the course
            sections = CourseSection.objects.filter(course=course)
            section_serializer = CourseSectionSerializer(sections, many=True)
            
            # Get lessons associated with each section
            for section in section_serializer.data:
                section['lessons'] = LessonSerializer(
                    Lesson.objects.filter(section_id=section['id']), many=True
                ).data

            return Response({
                "course": CourseSerializer(course).data,
                "sections": section_serializer.data
            }, status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)