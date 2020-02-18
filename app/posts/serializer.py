from rest_framework import serializers

from .models import Post


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
