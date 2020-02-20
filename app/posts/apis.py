from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializer import PostSerializer, PostCreateSerializer, PostCreateImageSerializer, PostCommentSerializer, PostCommentCreateSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request):
    #     serializer = PostCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         instance = serializer.save(author=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors)


class PostImageCreateAPIView(APIView):
    """
    PostImageCreateSerializer를 사용하도록 구현
    """

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        for image in request.data.getlist('image'):
            data = {'image': image}
            serializer = PostCreateImageSerializer(data=data)
            if serializer.is_valid():
                serializer.save(post=post)
            else:
                return Response(serializer.errors)
        serializer = PostSerializer(post)
        return Response(serializer.data)


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_summary='PostComment List',
    operation_description='Post의 댓글 목록을 보여줍니다',
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_summary='PostComment Create',
    operation_description='Post의 댓글을 생성합니다',
    responses={
        status.HTTP_201_CREATED: PostCommentSerializer(),
    }
))
class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return post.postcomment_set.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostCommentSerializer
        elif self.request.method == 'POST':
            return PostCommentCreateSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(post=post)

#
# class PostCommentListCreateAPIView(APIView):
#     # URL: /api/posts/1/comments/
#
#     def get(self, request, post_pk):
#         # post_pk에 해당하는 Post에 연결된 PostComment전체 가져오기
#         # many=True
#         post = get_object_or_404(Post, pk=post_pk)
#         comments = post.postcomment_set.all()
#         serializer = PostCommentSerializer(comments, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, post_pk):
#         # content:  request.data
#         # author:   request.user
#         # post:     URL params
#         post = get_object_or_404(Post, pk=post_pk)
#         serializer = PostCommentCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(post=post, author=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors)