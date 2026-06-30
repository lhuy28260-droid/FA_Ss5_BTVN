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
        
    current_enrolled = 0
    for r in registrations:
        if r["course_id"] == payload.course_id:
            current_enrolled += 1 
            
    if current_enrolled >= course_data["capacity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is full"
        )
        
    new_id = 1
    if registrations:
        max_id = registrations[0]["id"]
        for r in registrations:
            if r["id"] > max_id:
                max_id = r["id"]
        new_id = max_id + 1
        
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