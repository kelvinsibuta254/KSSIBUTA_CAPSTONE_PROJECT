from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
        
class NotificationMarkReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        notification = Notification.objects.filter(id=kwargs['pk'], recipient=request.user).first()
        if notification:
            notification.is_read = True
            notification.save()
            return Response({'message': 'notification marked as read'})
        return Response({'message': 'notification not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)