from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    """creates a read-only field for the author's username"""
    class Meta:
        """Defines metadata for the serializer"""
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']
        """The code below specifies fields that should not be modified when creating or updating a comment"""
        read_only_fields = ['created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    """This defines serializer for the Post model"""
    author = serializers.ReadOnlyField(source='author.username')
    """creates a read-only field for the author's username"""
    comments = CommentSerializer(many=True, read_only=True)
    """The line above nests the CommentSerializer within the PostSerializer. 
    The many=True argument indicates that a post can have multiple comments, and read_only=True means comments cannot be modified through this serializer."""
    likes_count = serializers.SerializerMethodField() # return the number of likes for the post

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'created_at', 'updated_at', 'likes_count', 'comments']
        read_only_fields = ['created_at', 'updated_at']

        def get_likes_count(self, obj):
            """This method calculates the number of likes for the post"""
            return obj.likes.count()

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    """The code above creates a read-only field for the username of the user who liked the post."""

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['created_at'] #the field cannot be modified enhancing data integrity and security