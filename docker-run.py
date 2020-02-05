#!/usr/bin/env python

# 도커 이미지에 secrets.json이 포함
import subprocess

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-p', '8001:8000'),
    ('--name', 'instagram'),
]
DOCKER_IMAGE_TAG = 'zehye/wps-instagram=12th'

subprocess.run(f'poetry export -f requirements.txt > requirements.txt', shell=True)

subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
subprocess.run(f'docker stop instagram', shell=True)

subprocess.run('docker run -d {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)
subprocess.run(f'docker cp secrets.json instagram:/srv/instagram', shell=True)
subprocess.run('docker exec -it instagram /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)


#
# access_key = subprocess.run('aws configure get aws_access_key_id --profile WPS-secretsManager',
#                stdout=subprocess.PIPE,
#                shell=True).stdout.decode('utf-8').strip()
#
# secret_key = subprocess.run('aws configure get aws_secret_access_key --profile WPS-secretsManager',
#                stdout=subprocess.PIPE,
#                shell=True).stdout.decode('utf-8').strip()
#
# print(access_key)
# print(secret_key)
#
# import boto3
#
# session = boto3.session.Session(profile_name='WPS-secretsManager')
# credentials = session.get_credentials()
# access_key = credentials.access_key
# secret_key = credentials.secret_key
# print(access_key)
# print(secret_key)
#
# DOCKER_OPTIONS = [
#     ('--rm', ''),
#     ('-it', ''),
#     ('-p', '8001:8000'),
#     ('--name', 'instagram'),
#     ('--env', f'AWS_SECRETS_MANAGER_ACCESS_KEY_ID={access_key}'),
#     ('--env', f'AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY={secret_key}')
# ]
#
# DOCKER_IMAGE_TAG = 'zehye/wps-instagram-12th'
#
# subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
# subprocess.run('docker stop instagram', shell=True)
# subprocess.run('docker run {options} zehye/wps_instagram_12th'.format(
#     options=' '.join([
#         f'{key} {value}' for key, value in DOCKER_OPTIONS
#     ]), tag=DOCKER_IMAGE_TAG
# ), shell=True)