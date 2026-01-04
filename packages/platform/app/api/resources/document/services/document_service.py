from typing import List, Optional

from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from app.api.resources.document.models.document import Document
from app.clients import minio
from app.clients.chromadb import add_document_chunks, search_documents
from app.clients.minio import bucket_name
from app.core.database import get_db

from .document_processor import DocumentProcessor


class DocumentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.processor = DocumentProcessor()

    def save(self, document: Document, commit: bool = True):
        self.db.add(document)
        if commit:
            self.db.commit()
            self.db.refresh(document)
        else:
            self.db.flush()
            return document

    def _process_and_store_vectors(self, document: Document, file_content: bytes):
        chunks = self.processor.process_document(
            file_content=file_content,
            content_type=document.file_type,
            filename=document.original_name,
        )
        metadata = {
            "document_name": document.name,
            "original_filename": document.original_name,
            "file_type": document.file_type,
            "category_id": str(document.category_id),
            "user_id": str(document.user_id),
            "description": document.description,
        }
        add_document_chunks(
            document_id=str(document.id),
            chunks=chunks,
            metadata=metadata,
            org_id=str(document.org_id),
        )

    def upload(
        self,
        file: UploadFile,
        name: str,
        description: str,
        category_id: str,
        org_id: str,
        user_id: str,
    ):
        try:
            file_ext = file.filename.split(".")[-1]
            file_content = file.file.read()
            file.file.seek(0)
            document = Document(
                name=name,
                original_name=file.filename,
                file_type=file.content_type,
                file_size=file.size,
                org_id=org_id,
                description=description,
                category_id=category_id,
                user_id=user_id,
                file_ext=file_ext,
                file_path="TEMP",
            )
            self.save(document, commit=False)
            file_path = f"{org_id}/{document.id}.{file_ext}"
            minio.put_object(
                bucket_name=bucket_name,
                object_name=file_path,
                content_type=file.content_type,
                data=file.file,
                length=file.size,
                metadata={"org_id": org_id, "document_id": document.id},
            )
            document.file_path = file_path
            self._process_and_store_vectors(document, file_content)
            return document
        except Exception as e:
            self.rollback()
            raise e
        finally:
            self.commit()

    def get_file_url(self, file_path: str) -> str:
        """Generate the full URL for a file in MinIO"""
        return minio.get_presigned_url(
            method="GET",
            bucket_name=bucket_name,
            object_name=file_path,
        )

    def search_documents(
        self,
        query: str,
        org_id: str,
        n_results: int = 10,
        category_id: Optional[str] = None,
    ) -> List[dict]:
        """Search documents using semantic search"""
        filter_metadata = {}
        if category_id:
            filter_metadata["category_id"] = category_id

        return search_documents(
            query=query,
            org_id=org_id,
            n_results=n_results,
            filter_metadata=filter_metadata,
        )

    def list(self, **kwargs) -> List[Document]:
        return self.db.query(Document).filter_by(**kwargs).all()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def refresh(self, document: Document):
        self.db.refresh(document)


def get_document_service(
    db: Session = Depends(get_db),
) -> DocumentService:
    return DocumentService(db)
