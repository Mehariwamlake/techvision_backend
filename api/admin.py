from django.contrib import admin

# Register your models here.

from .models import Course, CourseProduct, Product, Purchase, CourseSection, Lesson, UserCourseAccess, UserLessonComplete, Apply, Department, Employee

admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(CourseProduct)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Lesson)
admin.site.register( UserCourseAccess)
admin.site.register(UserLessonComplete)
admin.site.register( Apply)
admin.site.register(Department)
admin.site.register(Employee)

