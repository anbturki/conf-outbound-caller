from sqlalchemy.orm import Query


class SoftDeleteQuery(Query):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, ident):
        # Override get() to return None if the record is soft-deleted
        entity = super().get(ident)
        if entity and entity.is_deleted:
            return None
        return entity

    def filter_by(self, **kwargs):
        # Automatically filter out soft-deleted records
        return super().filter_by(**kwargs).filter(self._get_soft_delete_filter())

    def _get_soft_delete_filter(self):
        # Helper to generate the soft delete filter
        return not self.mapper.class_.is_deleted
