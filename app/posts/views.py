from django.shortcuts import render, redirect


def post_list(request):
    return render(request, 'posts/post-list.html')


