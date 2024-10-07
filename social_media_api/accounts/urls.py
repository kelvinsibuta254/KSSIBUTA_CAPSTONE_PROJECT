from django.urls import path

from .views import UserRegisterView, LoginView, LogoutView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('profile', ProfileUpdateView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow'),

]