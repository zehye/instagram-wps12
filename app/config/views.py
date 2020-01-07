from django.shortcuts import render, redirect


def index(request):
    """
    settings.TEMPLATES의 DIRS에
        instagram/app/templates 경로를 추가
    Template: templates/index.html
        <h1>Index!</h1>
    URL:      '/', name='index'
    """
    if request.user.is_authenticated:
        return redirect('posts:post-list')
    return render(request, 'index.html')
