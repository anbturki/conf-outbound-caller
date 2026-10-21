from typing import Annotated, Optional

from api.dependencies import get_current_user
from common.schemas.dtos import CurrentUser
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from .services import DocumentService, get_document_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_file(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    document_service: DocumentService = Depends(get_document_service),
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    category_id: str = Form(...),
):
    org_id = current_user.org_id
    document = document_service.upload(
        name=name,
        description=description,
        category_id=category_id,
        file=file,
        org_id=org_id,
        user_id=current_user.id,
    )
    return {
        "filename": file.filename,
        "org_id": org_id,
        "document_id": document.id,
    }


@router.get("/")
def list_documents(
    document_service: Annotated[DocumentService, Depends(get_document_service)],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
):
    return document_service.list(org_id=str(current_user.org_id))


@router.get("/search")
async def search_documents(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    document_service: DocumentService = Depends(get_document_service),
    query: str = Query(..., description="Search query"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    limit: int = Query(2, ge=1, le=50, description="Number of results to return"),
):
    results = document_service.search_documents(
        query=query,
        org_id=str(current_user.org_id),
        n_results=limit,
        category_id=category_id,
    )
    return {
        "query": query,
        "results": [
            {
                "chunk_id": result["chunk_id"],
                "content": result["document"],
                "similarity_score": 1
                - result["distance"],  # Convert distance to similarity
                "metadata": result["metadata"],
            }
            for result in results
        ],
        "total_results": len(results),
    }
