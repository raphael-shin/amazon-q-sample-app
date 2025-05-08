from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(
    title="Todo API",
    description="FastAPI 기반의 Todo 관리 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인만 허용하도록 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Todo 모델 정의
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Todo 데이터 저장소 (실제 프로젝트에서는 데이터베이스 사용)
todos = {}

# 루트 경로
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Todo API에 오신 것을 환영합니다!"}

# Todo 생성
@app.post("/todos/", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"])
async def create_todo(todo: TodoCreate):
    todo_id = str(uuid.uuid4())
    current_time = datetime.now()
    
    todo_dict = todo.dict()
    todo_dict.update({
        "id": todo_id,
        "created_at": current_time,
        "updated_at": current_time
    })
    
    todos[todo_id] = todo_dict
    return todo_dict

# 모든 Todo 조회
@app.get("/todos/", response_model=List[Todo], tags=["Todos"])
async def read_todos(skip: int = 0, limit: int = 100):
    return list(todos.values())[skip:skip + limit]

# 특정 Todo 조회
@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def read_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

# Todo 업데이트
@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_todo(todo_id: str, todo: TodoCreate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_dict = todo.dict()
    todo_dict.update({
        "id": todo_id,
        "created_at": todos[todo_id]["created_at"],
        "updated_at": datetime.now()
    })
    
    todos[todo_id] = todo_dict
    return todo_dict

# Todo 삭제
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
async def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    del todos[todo_id]
    return None
