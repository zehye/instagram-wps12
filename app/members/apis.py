from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserSerializer


class AuthTokenAPIView(APIView):
    def post(self, request):

        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        # 4. 얻어낸 User객체와 연결되는 Token을 get_or_create()로
        #    가져오거나 생성
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        # 5. 생성된 Token의 'key'속성을 적절히 반환
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)
