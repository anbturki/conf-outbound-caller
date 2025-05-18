from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from .models.category import Category


class CategoryService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def save(self, category: Category, commit: bool = True):
        self.db.add(category)
        if commit:
            self.db.commit()
            self.db.refresh(category)
        else:
            self.db.flush()
            return category

    def commit(self):
        self.db.commit()

    def refresh(self, category: Category):
        self.db.refresh(category)


def get_category_service(
    db: Annotated[Session, Depends(get_db)],
) -> CategoryService:
    return CategoryService(db)
