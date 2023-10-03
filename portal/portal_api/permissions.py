from rest_framework import permissions
from .utils import get_token


class IsDean(permissions.BasePermission):
    def has_permission(self, request, view):
        user = get_token(request)
        return user[0].is_authenticated and user[0].is_dean


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = get_token(request)
        return user[0].is_authenticated and user[0].is_student
