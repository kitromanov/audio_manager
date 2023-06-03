# from rest_framework.permissions import BasePermission
#
#
# class UserPermission(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if request.user.is_staff:
#                 return True
#             elif view.action in ['create']:
#                 return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_staff:
#             return True
#         elif view.action in ['update', 'partial_update'] and obj.created_by == request.user:
#             return True
#         return False
