from django.contrib import admin
from .models import *


class PostImageInline(admin.TabularInline):
    model = PostImage


class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Moel
    - Post의 __str__을 적절히 작성한다.

    Admin
    - 작성자, 글, 작성시간이 모두 보여지게 한다: list_display

    상세화면에 PostImage를 곧바로 추가할 수 있도록 한다
        inlines: TabularInline(위의 PostImageInline을 적절히 채운 후 사용)

    - 마찬가지로 PostComment 도 곧바로 추가할 수 있도록 한다.
    """
    list_display = ('author', 'content', 'created')
    inlines = [
        PostImageInline,
        PostCommentInline,
    ]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass
