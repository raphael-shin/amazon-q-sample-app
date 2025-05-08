# Amazon Q Sample App - Todo API

FastAPI 기반의 Todo 관리 API 백엔드 서버입니다.

## 기능

- Todo 항목 생성, 조회, 수정, 삭제 (CRUD)
- Swagger UI를 통한 API 테스트
- Docker 컨테이너 지원

## 시작하기

### 환경 설정

```bash
# 환경 설정 스크립트 실행
./setup_env.sh
```

### 서버 실행

```bash
# 서버 실행 스크립트
./run.sh
```

### API 문서

서버 실행 후 다음 URL에서 Swagger UI를 통해 API를 테스트할 수 있습니다:
- http://localhost:8000/docs

## 테스트 실행

API 엔드포인트에 대한 자동화된 테스트를 실행하려면:

```bash
# 필요한 패키지 설치
pip install -r requirements.txt

# 테스트 실행
pytest

# 상세한 테스트 출력을 보려면
pytest -v
```

테스트는 다음 사항을 검증합니다:
- 모든 API 엔드포인트의 성공 케이스 (200 OK 응답)
- 오류 처리 및 예외 케이스 (4xx, 5xx 응답)
- 모든 HTTP 메서드 (GET, POST, PUT, DELETE)
- 필수 필드가 누락된 경우의 적절한 오류 반환
- 잘못된 데이터 타입에 대한 유효성 검사
