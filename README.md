# API 문서
### 인증
#### BasicAuth

HTTP의 Basic Authentication을 사용

HTTP Header의 `Authentication`키에 `Basic <value>` 값을 넣어 전송

`<value>`에 들억는 값은 "**username:password**"문자열을 Base64로 인코팅한 값

ex)
```
Authentication:Basic
```

#### TokenAuth

(DRF라이브러리)[]에서 제공하는 토큰 인증 방식

HTTP Header의 `Authentication`키에 `Token <value>` 값을 넣어 전송

`<value>`에 들어가는 값은 Token을 발급받는 API(AuthTokenAPI)에 자격증명(일반적으로 username과 password)를 전달받은 후 받은 **token** 값을 사용

클라이언트에서는 해당 **token** 을 로그인을 윶하는 동안 로컬 저장소에 저장 후 , 매 HTTP Request마다 Header에 인증값을 전송하는 형태로 세션 유지


ex) 전송하는 HTTP Header의 값
```

```

### posts
#### PostList