
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseListView, ProductViewSet, PurchaseViewSet
from .views.course_views import CourseViewSet
from .views.section_views import CourseSectionViewSet
from .views.lesson_views import LessonViewSet

router = DefaultRouter()

router.register(r'courses', CourseViewSet, basename='courses')

router.register(r'sections', CourseSectionViewSet, basename='sections')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'products', ProductViewSet)
router.register(r'purchases', PurchaseViewSet)


urlpatterns = [
   
    path('courses/', CourseListView.as_view(), name='courses'),
    path('', include(router.urls)),
    path('sections/', CourseListView.as_view(), name='sections'),
    path('courses/<int:pk>/create_lesson/', CourseViewSet.as_view({'post': 'create_lesson'})),
    path('courses/<int:pk>/publish/', CourseViewSet.as_view({'post': 'publish'})),
    path('products/<int:pk>/purchase/', ProductViewSet.as_view({'post': 'purchase'})),
    path('purchases/<int:pk>/complete_purchase/', PurchaseViewSet.as_view({'post': 'complete_purchase'})),
]

