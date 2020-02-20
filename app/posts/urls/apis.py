from django.urls import path
from .. import apis

urlpatterns = [
    path('', apis.PostListCreateAPIView.as_view()),
    path('<int:pk>/comment/create/', apis.PostImageCreateAPIView.as_view()),
    path('<int:pk>/comment/', apis.PostCommentListCreateAPIView.as_view()),
]
