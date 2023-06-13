from rest_framework.permissions import BasePermission


class IsStaffOrCreatorOrAssignedUser(BasePermission):

    @staticmethod
    def has_permission(request, view):
        if request.user and (
                request.user.is_staff or view.get_object().creator == request.user or request.user in view.get_object().assigned_users.all()) and not request.user.is_blocked:
            return True
        return False
