from typing import List

from api.resources.document.models.document import Document
from core.database import get_db
from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

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
            # minio.put_object(
            #     bucket_name=bucket_name,
            #     object_name=file_path,
            #     content_type=file.content_type,
            #     data=file.file,
            #     length=file.size,
            #     metadata={"org_id": org_id, "document_id": document.id},
            # )
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
        # return minio.get_presigned_url(
        #     method="GET",
        #     bucket_name=bucket_name,
        #     object_name=file_path,
        # )

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
