from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedView

# router = routers.DefaultRouter()
# router.register(r'posts', PostViewSet)
# router.register(r'comments', CommentViewSet)
urlpatterns = [
    # path('', include(router.urls)),
    path('posts/feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]