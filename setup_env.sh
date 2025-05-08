#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

echo "🔧 uv를 사용하여 Python 가상환경 설정 중..."

# uv가 설치되어 있는지 확인
if ! command -v uv &> /dev/null; then
    echo "❌ uv가 설치되어 있지 않습니다. 설치를 진행합니다..."
    pip install uv
fi

# 가상환경 생성
echo "🔧 가상환경 생성 중..."
uv venv

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source .venv/bin/activate

# 필요한 패키지 설치
echo "🔧 필요한 패키지 설치 중..."
uv pip install fastapi uvicorn pydantic

echo "✅ 환경 설정이 완료되었습니다!"
echo "🚀 서버를 실행하려면 './run.sh' 명령어를 사용하세요."
