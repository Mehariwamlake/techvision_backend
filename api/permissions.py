from rest_framework import permissions

class CanCreateCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Custom logic to check if the user can create a course
        return request.user and request.user.has_perm('courses.add_course')

class CanUpdateCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Custom logic to check if the user can update a course
        return request.user and request.user.has_perm('courses.change_course')

class CanDeleteCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Custom logic to check if the user can delete a course
        return request.user and request.user.has_perm('courses.delete_course')
