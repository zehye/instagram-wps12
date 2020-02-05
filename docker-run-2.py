#!/usr/bin/env python
import subprocess
import boto3

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '8001:8000'),
    ('--name', 'instagram'),
]

DOCKER_IMAGE_TAG = 'zehye/wps-instagram-12th'

subprocess.run('docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
subprocess.run('docker stop instagram', shell=True)

subprocess.run('docker run {options} zehye/wps_instagram_12th'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]), tag=DOCKER_IMAGE_TAG
), shell=True)

# secrets.json 파일 전송
subprocess.run('docker cp secrets.json instagram:/srv/instagram', shell=True)
# runserver 명령을 전송
subprocess.run('docker exec instagram python manage.py runserver 0:8000', shell=True)
