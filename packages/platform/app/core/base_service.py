from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from shared import logger
from sqlalchemy import and_, asc, desc, func, or_, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import operators

from app.core.exceptions import ResourceNotFoundException

ModelType = TypeVar("ModelType")
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
QueryParamsType = TypeVar("QueryParamsType", bound=BaseModel)


class BaseService(Generic[ModelType, UpdateSchemaType, QueryParamsType], ABC):
    ALLOWED_OPERATORS = {
        "eq": operators.eq,
        "ne": operators.ne,
        "gt": operators.gt,
        "gte": operators.ge,
        "lt": operators.lt,
        "lte": operators.le,
        "in": operators.in_op,
        "not_in": operators.notin_op,
        "like": operators.like_op,
        "ilike": operators.ilike_op,
    }

    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
        # Get valid column names for this model to prevent SQL injection
        self.valid_columns = set(col.name for col in model.__table__.columns)
        # Get valid relationship names for this model to prevent SQL injection
        self.valid_relationships = set(
            rel.key for rel in model.__mapper__.relationships
        )

    def _validate_column_name(self, column_name: str) -> bool:
        """Validate that column name exists on the model"""
        return (
            column_name in self.valid_columns or column_name in self.valid_relationships
        )

    def _validate_sort_params(self, sort_col: str, order: str = "asc"):
        """Validate sort column and order"""
        if not self._validate_column_name(sort_col):
            logger.warning(f"Invalid sort column attempted: {sort_col}")
            return False, f"Invalid sort column: {sort_col}"
        if order.lower() not in ["asc", "desc"]:
            logger.warning(f"Invalid sort order attempted: {order}")
            return False, f"Invalid sort order: {order}"
        return True, None

    def _sanitize_filters(self, filters: dict[str, Any]) -> dict[str, Any]:
        """Sanitize filter dictionary by validating column names"""
        sanitized = {}
        for key, value in filters.items():
            if self._validate_column_name(key):
                sanitized[key] = value
            else:
                logger.warning(f"Invalid filter key attempted: {key}")
        return sanitized

    def _build_where_conditions(self, **filters) -> List:
        conditions = []
        sanitized_filters = self._sanitize_filters(filters)
        for key, value in sanitized_filters.items():
            if hasattr(self.model, key):
                column = getattr(self.model, key)
                conditions.append(column == value)
        return conditions

    def commit(self) -> None:
        """Explicitly commit the current transaction"""
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error committing transaction: {e}")
            raise

    def rollback(self) -> None:
        """Explicitly rollback the current transaction"""
        try:
            self.db.rollback()
        except Exception as e:
            logger.error(f"Error rolling back transaction: {e}")
            raise

    def save(self, instance: ModelType, commit: bool = True) -> ModelType:
        try:
            self.db.add(instance)
            if commit:
                self.db.commit()
                self.db.refresh(instance)
            else:
                self.db.flush()
                self.db.expunge(instance)
                self.db.merge(instance)

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving instance: {e}")
            raise
        return instance

    def get_by_id(self, id: UUID, **filters) -> Optional[ModelType]:
        """Get a single instance by ID with optional filters"""
        try:
            conditions = [self.model.id == id]
            conditions.extend(self._build_where_conditions(**filters))

            query = select(self.model).where(and_(*conditions))
            result = self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting instance by ID: {e}")
            raise

    def get_by_id_and_org_id(
        self, id: UUID, org_id: UUID, **filters
    ) -> Optional[ModelType]:
        """Get a single instance by organization ID with optional filters"""
        try:
            conditions = [self.model.id == id, self.model.org_id == org_id]
            conditions.extend(self._build_where_conditions(**filters))

            query = select(self.model).where(and_(*conditions))
            result = self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting instance by organization ID: {e}")
            raise

    def get_one_or_raise(self, id: UUID, org_id: UUID, **filters) -> ModelType:
        """Get a single instance by optional filters and raise an exception if not found"""
        instance = self.get_by_id_and_org_id(id, org_id, **filters)
        if not instance:
            raise ResourceNotFoundException(
                resource_type=self.model.__name__, resource_id=id
            )
        return instance

    def update_by_id(
        self, id: UUID, update_data: UpdateSchemaType, **filters
    ) -> Optional[ModelType]:
        """Update an instance by ID with optional filters"""
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            if not update_dict:
                return None

            # Sanitize update data - only allow updates to valid columns
            sanitized_update = {}
            for key, value in update_dict.items():
                if self._validate_column_name(key):
                    sanitized_update[key] = value
                else:
                    logger.warning(f"Attempted to update invalid column: {key}")

            if not sanitized_update:
                return None

            conditions = [self.model.id == id]
            conditions.extend(self._build_where_conditions(**filters))

            query = (
                update(self.model)
                .where(and_(*conditions))
                .values(**sanitized_update)
                .returning(self.model)
            )
            result = self.db.execute(query)
            self.db.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating instance: {e}")
            raise

    def delete_by_id(self, id: UUID, **filters) -> bool:
        """Soft delete an instance by ID with optional filters by setting deleted_at"""
        conditions = [self.model.id == id]
        for key, value in filters.items():
            if hasattr(self.model, key):
                conditions.append(getattr(self.model, key) == value)

        query = (
            update(self.model).where(and_(*conditions)).values(deleted_at=func.now())
        )
        result = self.db.execute(query)
        self.db.commit()
        return result.rowcount > 0

    def _build_search_conditions(
        self, search_term: str, search_fields: List[str]
    ) -> List:
        """Build search conditions safely"""
        search_conditions = []
        # Escape the search term for LIKE queries
        escaped_search = search_term.replace("%", "\\%").replace("_", "\\_")
        search_pattern = f"%{escaped_search}%"

        for field in search_fields:
            if self._validate_column_name(field) and hasattr(self.model, field):
                column = getattr(self.model, field)
                # Use parameterized query - SQLAlchemy handles the escaping
                search_conditions.append(column.ilike(search_pattern))
        return search_conditions

    def paginate(
        self,
        query_params: QueryParamsType,
        base_filters: Optional[Dict[str, Any]] = None,
        search_fields: Optional[List[str]] = None,
        allowed_sort_columns: Optional[List[str]] = None,
    ) -> Tuple[List[ModelType], int]:
        """
        Generic pagination with filtering and searching
        """
        try:
            query = select(self.model)

            # Store conditions for count query
            all_conditions = []

            if base_filters:
                conditions = self._build_where_conditions(**base_filters)
                if conditions:
                    query = query.where(and_(*conditions))
                    all_conditions.extend(conditions)

            if (
                hasattr(query_params, "search")
                and query_params.search
                and search_fields
            ):
                search_conditions = self._build_search_conditions(
                    query_params.search, search_fields
                )
                if search_conditions:
                    search_condition = or_(*search_conditions)
                    query = query.where(search_condition)
                    all_conditions.append(search_condition)

            # Create count query with the same conditions
            count_query = select(func.count(self.model.id))
            if all_conditions:
                count_query = count_query.where(and_(*all_conditions))

            count_result = self.db.execute(count_query)
            total = count_result.scalar()

            # Apply sorting with validation
            if hasattr(query_params, "sort") and query_params.sort:
                sort_column = query_params.sort
                order = getattr(query_params, "order", "asc").lower()

                if allowed_sort_columns and sort_column not in allowed_sort_columns:
                    logger.warning(f"Sort column {sort_column} not in allowed list")
                else:
                    is_valid, error_msg = self._validate_sort_params(sort_column, order)
                    if is_valid and hasattr(self.model, sort_column):
                        column = getattr(self.model, sort_column)
                        if order == "desc":
                            query = query.order_by(desc(column))
                        else:
                            query = query.order_by(asc(column))

            # Apply pagination with validation
            page = max(1, getattr(query_params, "page", 1))
            limit = min(1000, max(1, getattr(query_params, "limit", 10)))
            query = query.offset((page - 1) * limit).limit(limit)

            # AWAIT the database call
            result = self.db.execute(query)
            items = result.scalars().all()

            return items, total

        except Exception as e:
            logger.error(f"Error in list_with_pagination: {e}")
            raise
