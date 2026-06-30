from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
app = FastAPI()

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int
    
students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]
courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]
registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]


@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(payload: RegistrationCreate):
    
    # 1. Kiểm tra student_id tồn tại (Cổ điển)
    student_exists = False
    for s in students:
        if s["id"] == payload.student_id:
            student_exists = True
            break
            
    if not student_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
        
    # 2. Kiểm tra course_id tồn tại (Cổ điển)
    course_data = None
    for c in courses:
        if c["id"] == payload.course_id:
            course_data = c
            break
            
    if not course_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
        
    # 3. Bẫy 1: Kiểm tra Đăng ký trùng (Cổ điển - Không dùng any)
    is_duplicated = False
    for r in registrations:
        if r["student_id"] == payload.student_id and r["course_id"] == payload.course_id:
            is_duplicated = True
            break
            
    if is_duplicated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already registered this course"
        )
        
    # 4. Bẫy 2: Kiểm tra Khóa học đã đủ sĩ số (Cổ điển - Không dùng sum)
    current_enrolled = 0
    for r in registrations:
        if r["course_id"] == payload.course_id:
            current_enrolled += 1 # Đếm thủ công từng học viên
            
    if current_enrolled >= course_data["capacity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is full"
        )
        
    # 5. Tìm ID lớn nhất để tự động tăng (Cổ điển - Không dùng max list comprehension)
    new_id = 1
    if registrations:
        max_id = registrations[0]["id"]
        for r in registrations:
            if r["id"] > max_id:
                max_id = r["id"]
        new_id = max_id + 1
        
    # Tiến hành tạo đăng ký mới
    new_reg = {
        "id": new_id,
        "student_id": payload.student_id,
        "course_id": payload.course_id
    }
    registrations.append(new_reg)
    
    return {
        "message": "Registration created successfully",
        "data": new_reg
    }