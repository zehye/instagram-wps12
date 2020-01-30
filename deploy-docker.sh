#!/usr/bin/env sh

IDENTIFY_FILE="$HOME/.ssh/wps12th.pem"
USER="ubuntu"
HOST="54.180.2.2"
TARGET=${USER}@${HOST}
ORIGIN_SOURCE="$HOME/fastcampus/instagram"
DEST_SOURCE="/home/ubuntu/projects/instagram"
DOCKER_REPO="zehye/wps_instagram_12th"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${TARGET}"

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

# 로컬의 aws profile을 전달
echo "aws profile"
${SSH_CMD} -C "sudo rm -rf /home/ubuntu/.aws"
echo "aws profileeeeeee"
scp -i "${IDENTITY_FILE}" -r "$HOME/.aws/" ${TARGET}:/home/ubuntu/

# screen에서 docker run
echo "screen settings"
# 실행중이던 screen 세션종료
${SSH_CMD} -C 'screen -X -S docker quit'
# screen 실행
${SSH_CMD} -C 'screen -S docker -d -m'
# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "screen -r docker -X stuff 'sudo docker run --rm -it -p 80:8000 --name=instagram zehye/wps-instagram-12th /bin/bash\n'"
# bash를 실행중인 container에 HOST의 ~/.aws폴더를 복사
${SSH_CMD} -C "sudo docker cp ~/.aws/ instagram:/root"
# container에서 bash를 실행중인 screen에 runserver명령어를 전달
${SSH_CMD} -C "screen -r docker -X stuff 'python manage.py runserver 0:8000\n'"

echo "  finish!"