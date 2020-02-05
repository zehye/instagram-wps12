FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN         apt -y install nginx

# poetry export로 생성된 requirements.txt를 적절히 복사
COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

# 소스코드 복사
COPY        . /srv/instagram
WORKDIR     /srv/instagram/app

# Nginx설정파일을 복사
RUN         cp /srv/instagram/.config/instagram.nginx /etc/nginx/sites-enabled/

# collectstatic
#RUN         python manage.py collectstatic  --noinput

# Gunicorn실행 (/run/instagram.sock파일을 사용해서 config.wsgi모듈과 통신)
#  gunicorn -b unix:/run/instagram.sock config.wsgi
# Nginx실행 (Foreground모드로)
#  nginx -g "daemon off;"