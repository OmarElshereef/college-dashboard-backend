from fastapi import HTTPException, status
from models.course import CourseCreate
from database.supabase_client import SupabaseClient

supabase = SupabaseClient().get_client()

async def create_course_controller(course: CourseCreate):
    prof_result = supabase.table("professors").select("id").eq("id", course.professor_id).execute()
    if not prof_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor not found")

    existing_course = supabase.table("courses").select("*").eq("code", course.code).execute()
    if existing_course.data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course with this code already exists")

    result = supabase.table("courses").insert(course.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create course")

    return result.data[0]



async def get_all_courses_controller():
    try:
        result = supabase.table("courses").select("*").execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



async def get_course_controller(course_id: int):
    try:
        result = supabase.table("courses").select("*").eq("id", course_id).execute()
        if not result.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))