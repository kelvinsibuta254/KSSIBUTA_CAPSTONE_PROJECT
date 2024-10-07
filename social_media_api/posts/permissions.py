from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """This is a custom permission class for a DRF API.
    If the request method is safe (like reading data), the method returns True,
     allowing access to anyone.
     If the request method is not safe (like POST, PUT, DELETE), this line checks
     if the user making the request (request.user) is the same as the author of the object (obj.author).
If they are the same, it returns True, granting permission to modify or delete the object. If not, it returns False, denying access."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user