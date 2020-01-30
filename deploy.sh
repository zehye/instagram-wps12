#!/usr/bin/env sh

IDENTIFY_FILE="$HOME/.ssh/wps12th.pem"
HOST="ubuntu@54.180.2.2"
ORIGIN_SOURCE="$HOME/fastcampus/instagram"
DEST_SOURCE="/home/ubuntu/projects/instagram"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${HOST}"

echo "== runserver 배포 =="

# 숙제
# 다시 실행되는 서버 만들기
# (가능하다면) HOST만 바꾸고 이 스크립트를 실행하면 전체 서버가 세팅되고 runserver된 화면 볼 수 있도록 하기

# 서버 초기설정
echo "apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'
echo "apt install python3-pip"
${SSH_CMD} -C 'sudo apt -y install python3-pip'

# pip freeze
echo "pip freeze"
"$HOME"/.pyenv/versions/wps-instagram-env/bin/pip freeze > "$HOME"/fastcampus/instagram/requirements.txt

# 기존 폴더 삭제
echo "remove server source"
${SSH_CMD} sudo rm -rf ${DEST_SOURCE}

# 로컬에 있는 파일 업로드
echo "upload local source"
${SSH_CMD} mkdir -p ${DEST_SOURCE}
scp -q -i "${IDENTIFY_FILE}" -r "${ORIGIN_SOURCE}" ${HOST}:${DEST_SOURCE}

# pip install
echo "pip install"
${SSH_CMD} pip3 install -q -r /home/ubuntu/projects/instagram/instagram/requirements.txt

echo "screen settings"
# 실행중이던 screen 세션종료
${SSH_CMD} -C 'screen -X -S runserver quit'
# screen 실행
${SSH_CMD} -C 'screen -S runserver -d -m'
# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "screen -r runserver -X stuff 'sudo python3 /home/ubuntu/projects/instagram/instagram/app/manage.py runserver 0:80\n'"

echo "  finish!"