from django.shortcuts import render, redirect
from .models import *
from .forms import PostCreateForm, CommentCreateForm


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


def comment_create(request, post_pk):
    # URL: /posts/<int:post_pk>/comments/create/
    # Template: 없음 (post-list.html내에 Form을 구현)
    #  post-list.html 내부에서, 각 Post마다 자신에게 연결된 PostComment목록을 보여주도록 함
    #   보여주는형식은
    #    <ul>
    #     <li><b>작성자명</b> <span>내용</span></li>
    #     <li><b>작성자명</b> <span>내용</span></li>
    #    </ul>
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        # Form인스턴스를 만드는데, data에 request.POST로 전달된 dict를 입력
        form = CommentCreateForm(data=request.POST)
        # Form인스턴스 생성시, 주어진 데이터가
        # 해당 Form이 가진 Field들에 적절한 데이터인지 검증
        if form.is_valid():
            form.save(post=post, author=request.user)
        return redirect('posts:post-list')
