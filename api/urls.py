from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import viewsets
from api.views.Candidates_views import CandidatesViewSet
from .views import CourseListView, ProductViewSet, PurchaseViewSet
from .views.course_views import CourseViewSet
from .views.section_views import CourseSectionViewSet
from .views.lesson_views import LessonViewSet
from api.views.department_views import DepartmentViewSet
from api.views.company_views import CompanyViewSet
from api.views.employees_views import EmployeesViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'employees', EmployeesViewSet, basename='employees')
router.register(r'companys', CompanyViewSet, basename='companys')
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'candidates', CandidatesViewSet, basename='candidates')
router.register(r'sections', CourseSectionViewSet, basename='sections')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'products', ProductViewSet)
router.register(r'purchases', PurchaseViewSet)

# URL patterns
urlpatterns = [
    # List and detail routes for course and candidate
    path('courses/', CourseListView.as_view(), name='courses'),
    path('sections/', CourseListView.as_view(), name='sections'),
    
    # Use the router to automatically generate URLs for the registered viewsets
    path('', include(router.urls)),
    
    # Custom actions within viewsets
    path('courses/<int:pk>/create_lesson/', CourseViewSet.as_view({'post': 'create_lesson'})),
    path('courses/<int:pk>/publish/', CourseViewSet.as_view({'post': 'publish'})),
    path('products/<int:pk>/purchase/', ProductViewSet.as_view({'post': 'purchase'})),
    path('purchases/<int:pk>/complete_purchase/', PurchaseViewSet.as_view({'post': 'complete_purchase'})),
]
