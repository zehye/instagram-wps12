from django.shortcuts import render


def index(request):
    """
    settings.TEMPLATES의 DIRS에
        instagram/app/templates 경로를 추가
    Template: templates/index.html
        <h1>Index!</h1>
    URL:      '/', name='index'
    """
    return render(request, 'index.html')
