import os
import shutil
import uuid
from uuid import UUID

from app.auth.utils import get_current_user
from app.db.crud import add_doc, get_user_docs, remove_doc
from app.db.database import get_db
from app.db.models import Document
from app.db.vectors import add_doc_vector
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from rag.file_processing.data_ingestion import process_file
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)


@router.get("/")
async def list_user_docs(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    documents = await get_user_docs(user_id=current_user.id, db=db)
    return {"documents": documents}


@router.post("/")
async def upload_document(file: UploadFile = File(...), current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    _, ext = os.path.splitext(file.filename)
    if not ext:
        raise HTTPException(status_code=400, detail="File has no extension")

    file_id = str(uuid.uuid4())
    file_location = f"{FILES_DIR}/{file_id}{ext}"
    # Save the file to disk
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    document = Document(
        id=file_id, user_id=current_user.id, file_type=file.content_type, file_name=file.filename, file_path=file_location)

    await add_doc(document, db)
    # Process the file
    do_vectors = await process_file(file_location, current_user.id, file_id)
    for doc_vector in do_vectors:
        await add_doc_vector(doc_vector, db)
    # Create Document object

    return {"msg": "Document uploaded successfully", "id": file_id}


@router.delete("/{doc_id}")
async def delete_document(doc_id: UUID, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        file_path = await remove_doc(doc_id, current_user.id, db)
    except PermissionError:
        raise HTTPException(
            status_code=403, detail="Document not found or Access denied to delete this document")
    try:
        os.remove(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    return {"msg": "Document deleted successfully"}
