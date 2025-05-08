FROM python:3.11-slim

WORKDIR /app

# 필요한 패키지 설치
RUN pip install --no-cache-dir uv

# 소스 코드 복사
COPY . /app/

# 가상환경 생성 및 의존성 설치
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install fastapi uvicorn pydantic

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
