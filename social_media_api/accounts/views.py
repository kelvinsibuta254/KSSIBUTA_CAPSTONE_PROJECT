from django.shortcuts import render
from rest_framework import status, generics
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomUserSerializer, UserRegistrationSerializer, UserLoginSerializer

class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'status': 'user created',
                'token': token.key,
                'user': {
                    'username': user.username,
                    'bio' : user.bio
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key
                }, status=status.HTTP_200_OK)

                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'success': True, 'detail': "Logged out Successfully"}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer_class = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer_class = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_follow = self.get_queryset().get(id=user_id)
            if user_to_follow == request.user:
                return Response({'error': 'You can not follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
                request.user.following.add(user_to_follow)
                return Response({'message': 'You have successfully followed this user'}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({'message': 'USER NOT FOUND'}, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_unfollow = self.get_queryset().get(id=user_id)
            request.user.following.remove(user_to_follow)
            return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'USER NOT FOUND!!!'}, status=status.HTTP_404_NOT_FOUND)