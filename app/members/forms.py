from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '아이디',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
            }
        )
    )

    def clean(self):
        # Form.clean에서는 cleaned_data에 접근 가능
        # cleaned_data에는
        #  이 Form이 가진 모든 Field들에서 리턴된 데이터가 key: value로 들어있음
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)


class SignupForm(forms.Form):
    def save(self):
        pass
