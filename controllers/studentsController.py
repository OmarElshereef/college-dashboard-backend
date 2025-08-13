from fastapi import HTTPException, status, Response, UploadFile
from typing import List
from models.student import StudentCreate, StudentInsertion, StudentLogin,StudentReturn,Student
from models.user import UserInsertStudent

from utils.auth import create_access_token,hash_password, verify_password
from utils.multer import upload_to_supabase_storage
from database.supabase_client import SupabaseClient
from datetime import datetime
supabase = SupabaseClient().get_client()


async def signup_student_logic(student: StudentCreate, response: Response):
    existing = supabase.table("users").select("*").eq("email", student.email).execute()
    if existing.data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this email already exists")

    insertion = UserInsertStudent(
        role="student",
        email=student.email,
        password=hash_password(student.password),
        created_at=datetime.now(),
    )

    user_result = supabase.table("users").insert(insertion.model_dump(mode="json")).execute()
    if not user_result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    
    user = user_result.data[0]

    user_id = user["id"]

    student_insertion = StudentInsertion(
        id=user_id,
        name=student.name)



    student_result = supabase.table("students").insert(student_insertion.model_dump()).execute()
    if not student_result.data:
        supabase.table("users").delete().eq("id", user_id).execute()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create student profile"
        )
    
    
    token = create_access_token({"user_id": user_id, "role": "student"})


    return_student = StudentReturn(
        name= student.name,
        id=user_id,
        email=student.email,
        created_at=user["created_at"],
        token=token
    )


    return return_student

async def login_student_logic(student: StudentLogin, response: Response):
    user_result = supabase.table("users").select("*").eq("email", student.email).execute()
    if not user_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user = user_result.data[0]

    if user.get("role") != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a student account")

    if not verify_password(student.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    student_result = supabase.table("students").select("*").eq("id", user["id"]).execute()
    if not student_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    
    db_student = student_result.data[0]

    token = create_access_token({"user_id": user["id"], "role": "student"})



    return StudentReturn(
        id = user["id"],
        name = db_student["name"],
        email = student.email,
        created_at = user["created_at"],
        token=token
    )


async def get_all_students_logic():
    result = supabase.table("students").select("id, name, users(email, created_at)").execute()
    if not result.data:
        return []

    return [Student.from_supabase(row) for row in result.data]

async def get_student_logic(student_id: int):
    result = supabase.table("students").select("id, name, users(email, created_at)").eq("id", student_id).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    data = result.data[0]

    return Student.from_supabase(data)

async def upload_image_logic(student_id :int , file: UploadFile):
    student_result = supabase.table("students").select("id").eq("id", student_id).execute()
    if not student_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    public_url_response = await upload_to_supabase_storage(file)
    result = supabase.table("students_images").insert({
        "student_id": student_id,
        "image_url": public_url_response,
    }).execute()

    return result.data[0]

async def get_student_images_logic(student_id: int):
    student_result = supabase.table("students").select("id").eq("id", student_id).execute()
    if not student_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    images = supabase.table("students_images").select("image_url").eq("student_id", student_id).execute()
    return images.data
