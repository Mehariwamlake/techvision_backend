from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework.response import Response


from ..serializers import  CourseProductSerializer, CourseSectionSerializer, LessonSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import CourseSection, Lesson, Product, Purchase,Course, CourseProduct




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Retrieve product details including associated courses, sections, and lessons."""
        product = get_object_or_404(Product, pk=pk)
        course_products = CourseProduct.objects.filter(product=product)
        
        courses_data = []
        for course_product in course_products:
            course = course_product.course
            sections = CourseSection.objects.filter(course=course)
            sections_data = []
            
            for section in sections:
                lessons = Lesson.objects.filter(section=section)
                sections_data.append({
                    "section": CourseSectionSerializer(section).data,
                    "lessons": LessonSerializer(lessons, many=True).data
                })
            
            courses_data.append({
                "course": CourseProductSerializer(course_product).data,
                "sections": sections_data
            })
        
        return Response({
            "product": ProductSerializer(product).data,
            "courses": courses_data
        }, status=status.HTTP_200_OK)

        
    @action(detail=True, methods=['post'])
    def product_course(self, request, pk= None):
        product = self.get_object()
        course_id = request.data.get("course_id")
        
        if not course_id:
            return Response({"error": "course_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        course = get_object_or_404(Course, pk= course_id)
        association, created = CourseProduct.objects.get_or_create(course=course, product= product)
        
        if created:
            return Response({"message": "Course associated with product successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Course is already associated with this product."}, status=status.HTTP_200_OK)

            
    
    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        """Purchase a product and associate all courses with the user"""
        product = self.get_object()
        user = request.user
        if product.is_free():
            # If product is free, immediately grant access to courses
            purchase = Purchase.objects.create(
                user=user,
                product=product,
                price=0,
                product_details={"product_name": product.name},
                chapa_session_id="free-session-id",  # Placeholder for free purchase
            )
            purchase.associate_courses_with_user()
            return Response({"message": "Free product purchased successfully!"}, status=200)
        else:
            # Process payment and create purchase (not implemented here)
            pass