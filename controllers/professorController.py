from fastapi import HTTPException, status
from models.professor import Professor, ProfessorCreate, ProfessorLogin, ProfessorReturn, ProfessorUpdate, ProfessorInsertion
from models.user import UserInsertProfessor
from database.supabase_client import SupabaseClient
from utils.auth import create_access_token, hash_password, verify_password
from datetime import datetime



supabase = SupabaseClient().get_client()

async def create_professor_logic(professor: ProfessorCreate):
    existing = supabase.table("users").select("*").eq("email", professor.email).execute()
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    user_insert = UserInsertProfessor(
        role="professor",
        email=professor.email,
        password=hash_password(professor.password),
        created_at=datetime.now(),
    )
    user_result = supabase.table("users").insert(user_insert.model_dump(mode="json")).execute()
    if not user_result.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    user = user_result.data[0]
    user_id = user["id"]

    professor_insert = ProfessorInsertion(
        id=user_id,
        name=professor.name,
        department=professor.department
    )


    prof_result = supabase.table("professors").insert(professor_insert.model_dump()).execute()
    if not prof_result.data:
        supabase.table("users").delete().eq("id", user_id).execute()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create professor profile"
        )

    prof_data = prof_result.data[0]

    
    token = create_access_token({"user_id": user_id, "role": "professor"})

    return ProfessorReturn(
        id=user_id,
        name=professor.name,
        email=professor.email,
        department=professor.department,
        created_at=user["created_at"],
        token=token
    )




async def login_professor_logic(professor: ProfessorLogin):
    user_result = supabase.table("users").select("*").eq("email", professor.email).execute()
    if not user_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user = user_result.data[0]

    
    if user.get("role") != "professor":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a professor account")

    
    if not verify_password(professor.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    
    professor_result = supabase.table("professors").select("*").eq("id", user["id"]).execute()
    if not professor_result.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor profile not found")
    
    db_professor = professor_result.data[0]

    
    token = create_access_token({"user_id": user["id"], "role": "professor"})

    
    return ProfessorReturn(
        id=user["id"],
        name=db_professor["name"],
        email=professor.email,
        department=db_professor["department"],
        created_at=user["created_at"],
        token=token
    )


async def get_all_professors_logic():
    result = supabase.table("professors").select("id, name, department, users(email, created_at)").execute()
    if not result.data:
        return []

    return [Professor.from_supabase(row) for row in result.data]
