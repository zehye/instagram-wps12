#!/usr/bin/env sh

IDENTIFY_FILE="$HOME/.ssh/wps12th.pem"
HOST="ubuntu@54.180.2.2"
ORIGIN_SOURCE="$HOME/fastcampus/instagram"
DEST_SOURCE="/home/ubuntu/projects/instagram"
DOCKER_REPO="zehye/wps_instagram_12th"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${HOST}"

echo "== Docker 배포 =="

# 서버 초기설정
echo "apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'
echo "apt install docker.io"
${SSH_CMD} -C 'sudo apt -y install docker.io'

# docker build
echo "docker build"
docker build -t ${DOCKER_REPO} -f Dockerfile "${ORIGIN_SOURCE}"

# docker push
echo "docker push"
docker push ${DOCKER_REPO}

echo "docker stop"
${SSH_CMD} -C "sudo docker stop instagram"

echo "docker pull"
${SSH_CMD} -C "sudo docker pull ${DOCKER_REPO}"

# screen에서 docker run
echo "screen settings"
# 실행중이던 screen 세션종료
${SSH_CMD} -C 'screen -X -S docker quit'
# screen 실행
${SSH_CMD} -C 'screen -S docker -d -m'
# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "screen -r docker -X stuff 'sudo docker run --rm -it -p 80:8000 --name=instagram zehye/wps-instagram-12th\n'"

echo "  finish!"