from django.shortcuts import render
from rest_framework import filters, status, generics, viewsets
from rest_framework.decorators import action
from .serializers import CommentSerializer, PostSerializer, LikeSerializer
from rest_framework.response import Response
from .models import Post, Comment, Like
from notifications.models import Notification
from rest_framework import permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

        
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        # author = get_object_or_404(settings.AUTH_USER_MODEL, id=self.request.data.get('author'))
        return serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post=generics.get_object_or_404(Post, pk=pk)
        _, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            Notification.objects.create(
                recipient=post.author,
                actor = request.user,
                verb = 'liked your post',
                target = post
            )
            return Response({'message': 'post liked'}, status=status.HTTP_201_OK)
        return Response({'message': 'already liked this post'}, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({'message': 'post unliked'}, status=status.HTTP_200_OK)
        return Response({'message': 'operation failed'}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('created_at')


