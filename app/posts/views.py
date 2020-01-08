from django.shortcuts import render, redirect
from .models import *
from .forms import PostCreateForm


def post_list(request):
    posts = Post.objects.order_by('-pk')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post-list.html', context)


def post_like(request, pk):
    """
    pk가 pk인 post에 대한
    1. postlike객체를 생성한다.
    2. 만약 해당 객체가 이미 있다면 삭제한다.
    3. 완료후 posts:post-list로 redirect한다.
    :param request:
    :param pk:
    :return:
    """
    post = Post.objects.get(pk=pk)
    user = request.user

    post_like_qs = PostLike.objects.filter(user=user, post=post)
    if post_like_qs.exists():
        post_like_qs.delete()
    else:
        PostLike.objects.create(post=post, user=user)
    return redirect('posts:post-list')


def post_create(request):
    if request.method == 'POST':
        text = request.POST['text']
        images = request.FILES['image']
        post = Post.objects.create(
            author=request.user,
            content=text
        )

        for image in images:
            post.postimage_set.create(image=image)
        # post_image = PostImage.objects.create(
        #     post=post,
        #     image=image,
        # )

        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post-create.html', context)
