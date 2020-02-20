from rest_framework import serializers

from .models import Post, PostImage, PostComment
from members.serializer import UserSerializer


# Post
#  List         PostSerializer
#  Retrieve     PostDetailSerializer
#  Update       PostUpdateSerializer
#  Create       PostCreateSerializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'pk',
            'content',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'content',
        )

    def to_representation(self, instance):
        return PostSerializer(instance).data


class PostCreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = (
            'pk',
            'content',
        )


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = (
            'content',
        )
