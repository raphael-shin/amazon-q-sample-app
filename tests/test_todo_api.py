import pytest
import uuid
from fastapi import status
from app.main import todos

# Clear the todos dictionary before each test
@pytest.fixture(autouse=True)
def clear_todos():
    todos.clear()
    yield

def test_read_root(client):
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Todo API에 오신 것을 환영합니다!"}

class TestCreateTodo:
    def test_create_todo_success(self, client):
        """Test successful todo creation."""
        todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "completed": False
        }
        response = client.post("/todos/", json=todo_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["title"] == todo_data["title"]
        assert response_data["description"] == todo_data["description"]
        assert response_data["completed"] == todo_data["completed"]
        assert "id" in response_data
        assert "created_at" in response_data
        assert "updated_at" in response_data
    
    def test_create_todo_missing_title(self, client):
        """Test todo creation fails when title is missing."""
        todo_data = {
            "description": "This is a test todo",
            "completed": False
        }
        response = client.post("/todos/", json=todo_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "title" in response.text
    
    def test_create_todo_invalid_data_type(self, client):
        """Test todo creation fails with invalid data types."""
        todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "completed": "not a boolean"  # Should be a boolean
        }
        response = client.post("/todos/", json=todo_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "completed" in response.text

class TestReadTodos:
    def test_read_todos_empty(self, client):
        """Test reading todos when none exist."""
        response = client.get("/todos/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_read_todos_with_items(self, client):
        """Test reading todos when items exist."""
        # Create a todo first
        todo_data = {"title": "Test Todo"}
        client.post("/todos/", json=todo_data)
        
        response = client.get("/todos/")
        
        assert response.status_code == status.HTTP_200_OK
        todos_list = response.json()
        assert len(todos_list) == 1
        assert todos_list[0]["title"] == "Test Todo"
    
    def test_read_todos_with_pagination(self, client):
        """Test reading todos with pagination parameters."""
        # Create multiple todos
        for i in range(5):
            todo_data = {"title": f"Test Todo {i}"}
            client.post("/todos/", json=todo_data)
        
        # Test skip parameter
        response = client.get("/todos/?skip=2")
        assert response.status_code == status.HTTP_200_OK
        todos_list = response.json()
        assert len(todos_list) == 3  # 5 total - 2 skipped
        
        # Test limit parameter
        response = client.get("/todos/?limit=2")
        assert response.status_code == status.HTTP_200_OK
        todos_list = response.json()
        assert len(todos_list) == 2
        
        # Test both skip and limit
        response = client.get("/todos/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        todos_list = response.json()
        assert len(todos_list) == 2
        assert todos_list[0]["title"] == "Test Todo 1"

class TestReadTodo:
    def test_read_todo_success(self, client):
        """Test reading a specific todo successfully."""
        # Create a todo first
        todo_data = {"title": "Test Todo"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        response = client.get(f"/todos/{todo_id}")
        
        assert response.status_code == status.HTTP_200_OK
        todo = response.json()
        assert todo["id"] == todo_id
        assert todo["title"] == "Test Todo"
    
    def test_read_todo_not_found(self, client):
        """Test reading a non-existent todo."""
        non_existent_id = str(uuid.uuid4())
        response = client.get(f"/todos/{non_existent_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Todo not found" in response.text
    
    def test_read_todo_invalid_id_format(self, client):
        """Test reading a todo with an invalid ID format."""
        response = client.get("/todos/invalid-id")
        
        # FastAPI will try to validate the UUID format
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestUpdateTodo:
    def test_update_todo_success(self, client):
        """Test updating a todo successfully."""
        # Create a todo first
        todo_data = {
            "title": "Original Title",
            "description": "Original description",
            "completed": False
        }
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Update the todo
        updated_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "completed": True
        }
        response = client.put(f"/todos/{todo_id}", json=updated_data)
        
        assert response.status_code == status.HTTP_200_OK
        updated_todo = response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == "Updated Title"
        assert updated_todo["description"] == "Updated description"
        assert updated_todo["completed"] is True
        
        # Verify created_at is preserved and updated_at is changed
        assert updated_todo["created_at"] == create_response.json()["created_at"]
        assert updated_todo["updated_at"] != create_response.json()["updated_at"]
    
    def test_update_todo_not_found(self, client):
        """Test updating a non-existent todo."""
        non_existent_id = str(uuid.uuid4())
        update_data = {"title": "Updated Title"}
        response = client.put(f"/todos/{non_existent_id}", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Todo not found" in response.text
    
    def test_update_todo_missing_title(self, client):
        """Test updating a todo with missing required fields."""
        # Create a todo first
        todo_data = {"title": "Original Title"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Try to update without a title
        update_data = {"description": "Only description"}
        response = client.put(f"/todos/{todo_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "title" in response.text
    
    def test_update_todo_invalid_data_type(self, client):
        """Test updating a todo with invalid data types."""
        # Create a todo first
        todo_data = {"title": "Original Title"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Try to update with invalid data type
        update_data = {
            "title": "Updated Title",
            "completed": "not a boolean"  # Should be a boolean
        }
        response = client.put(f"/todos/{todo_id}", json=update_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "completed" in response.text

class TestDeleteTodo:
    def test_delete_todo_success(self, client):
        """Test deleting a todo successfully."""
        # Create a todo first
        todo_data = {"title": "Test Todo"}
        create_response = client.post("/todos/", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Delete the todo
        response = client.delete(f"/todos/{todo_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.text == ""  # No content
        
        # Verify the todo is deleted
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_todo_not_found(self, client):
        """Test deleting a non-existent todo."""
        non_existent_id = str(uuid.uuid4())
        response = client.delete(f"/todos/{non_existent_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Todo not found" in response.text
    
    def test_delete_todo_invalid_id_format(self, client):
        """Test deleting a todo with an invalid ID format."""
        response = client.delete("/todos/invalid-id")
        
        # FastAPI will try to validate the UUID format
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY