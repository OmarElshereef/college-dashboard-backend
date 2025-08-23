from fastapi import FastAPI, APIRouter, Depends, UploadFile

data_router = APIRouter()


@data_router.post("upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile):
    return {"message": f"Data uploaded for project {project_id}"}
