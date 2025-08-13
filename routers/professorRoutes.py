from fastapi import APIRouter, status, Depends
from typing import List
from models.professor import Professor, ProfessorCreate, ProfessorLogin, ProfessorReturn, ProfessorUpdate, ProfessorInsertion
from controllers import professorController as controller
from middlewares.authetication import verify_professor


router = APIRouter()




@router.post("/signup", response_model=ProfessorReturn, status_code=status.HTTP_201_CREATED)
async def create_professor(professor: ProfessorCreate):
    return await controller.create_professor_logic(professor)


@router.post("/login", response_model=ProfessorReturn, status_code=status.HTTP_200_OK)
async def login_professor(professor: ProfessorLogin):
    return await controller.login_professor_logic(professor)

@router.get("/", response_model=List[Professor], dependencies=[Depends(verify_professor)])
async def get_all_professors():
    return await controller.get_all_professors_logic()
