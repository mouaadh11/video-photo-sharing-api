from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Form
# from src.schemas import Post

from src.db import create_db_and_tables, get_async_session, Post

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
import os

from src.images import imagekit
import uuid 
import tempfile
import shutil


@asynccontextmanager
async def lifspan(app: FastAPI):
   await create_db_and_tables()
   yield

app = FastAPI(lifespan=lifspan)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):

    temp_file_path = None
    try: 
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        with open(temp_file_path, "rb") as f:
            response = imagekit.files.upload(
                file=f,
                file_name=file.filename,
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        post = Post(
        caption=caption,
        url=response.url,
        file_type="video" if file.content_type.startswith("video/") else "image",
        file_name=file.filename)

        session.add(post)
        await session.commit()
        await session.refresh(post)

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        shutil.copyfile(temp_file_path, file_path)


    except Exception  as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists (temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
    

    return {
    "filename": file.filename,
    "caption": caption,
    "message": "File uploaded successfully",
    "url": response.url
}