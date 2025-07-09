from rest_framework import serializers

from .models import Comment, Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "phone_number", "birth_date"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "text", "image", "author", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "text", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]
