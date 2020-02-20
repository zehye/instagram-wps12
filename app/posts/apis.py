from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializer import PostSerializer, PostCreateSerializer, PostCreateImageSerializer, PostCommentSerializer, PostCommentCreateSerializer


class PostListCreateAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class PostImageCreateAPIView(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        for image in request.data.getList('image'):
            data = {'image': image}
            serializer = PostCreateImageSerializer(data=data)
            if serializer.is_valid():
                serializer.save(data=data)
            else:
                return Response(serializer.errors)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostCommentListCreateAPIView(APIView):
    # URL: /apis/posts/1/Comments/
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comment = post.postcomment_set.all()
        serializer = PostCommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        serializer = PostCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
