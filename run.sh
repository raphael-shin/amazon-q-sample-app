#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# 가상환경이 존재하는지 확인
if [ ! -d ".venv" ]; then
    echo "❌ 가상환경이 존재하지 않습니다. 먼저 './setup_env.sh'를 실행해주세요."
    exit 1
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source .venv/bin/activate

# 서버 실행
echo "🚀 FastAPI 서버 실행 중..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
