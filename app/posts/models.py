from django.db import models
from members.models import User


class Post(models.Model):
    """
    인스타그램의 포스트
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    like_user = models.ManyToManyField(
        # PostLike 를 통한 Many to Many 구현
        User,
        through='PostLike',
        related_name='like_post_set',
    )
    created = models.DateTimeField(auto_now_add=True)


class PostImage(models.Model):
    """
    포스트의 사진들
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images')


class PostComment(models.Model):
    """
    각 포스트의 댓글 (Many to one)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    """
    사용자가 좋아요 뉴른 Post정보를 저장
    Many to Many 필드를 참조모델(Intermediate Model)을 거쳐 사용
        언제 생성되었는지를 Extra fields로 저장!(created)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
