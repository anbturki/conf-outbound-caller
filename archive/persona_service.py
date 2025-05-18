from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy import and_, asc, delete, desc, not_, or_, select, update
from sqlalchemy.orm import Session

from app.api.resources.persona.model import Persona
from app.api.resources.persona.schema import (
    PersonaCreateRequest,
    PersonaListQueryParams,
    PersonaUpdateRequest,
)


class PersonaService:
    def __init__(self, db: Session):
        self.db = db

    def create_persona(
        self,
        org_id: UUID,
        user_id: UUID,
        persona_data: PersonaCreateRequest,
    ) -> Persona:
        persona = Persona(
            name=persona_data.name,
            description=persona_data.description,
            category=persona_data.category,
            details=persona_data.details.model_dump(),
            org_id=org_id,
            user_id=user_id,
        )
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        return persona

    async def get_persona(self, persona_id: UUID, user_id: UUID) -> Optional[Persona]:
        query = select(Persona).where(
            and_(Persona.id == persona_id, Persona.user_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_persona(
        self, persona_id: UUID, user_id: UUID, persona_data: PersonaUpdateRequest
    ) -> Optional[Persona]:
        update_data = persona_data.model_dump(exclude_unset=True)
        if not update_data:
            return None

        query = (
            update(Persona)
            .where(
                and_(
                    Persona.id == persona_id,
                    Persona.user_id == user_id,
                    not_(Persona.is_pre_built),
                )
            )
            .values(**update_data)
            .returning(Persona)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def delete_persona(self, persona_id: UUID, user_id: UUID) -> bool:
        query = delete(Persona).where(
            and_(
                Persona.id == persona_id,
                Persona.user_id == user_id,
                not_(Persona.is_pre_built),
            )
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0

    async def list_personas(
        self, org_id: UUID, query_params: PersonaListQueryParams
    ) -> Tuple[List[Persona], int]:
        # Build base query
        query = select(Persona).where(Persona.org_id == org_id)

        # Apply filters
        if query_params.search:
            search_term = f"%{query_params.search}%"
            query = query.where(
                or_(
                    Persona.name.ilike(search_term),
                    Persona.description.ilike(search_term),
                )
            )

        if query_params.category:
            query = query.where(Persona.category == query_params.category)

        if query_params.type:
            if query_params.type == "custom":
                query = query.where(not_(Persona.is_pre_built))
            elif query_params.type == "pre-built":
                query = query.where(Persona.is_pre_built)

        # Get total count
        count_query = select(Persona).where(query.whereclause)
        total = len((self.db.execute(count_query)).scalars().all())

        # Apply sorting
        if query_params.sort:
            sort_column = getattr(Persona, query_params.sort)
            if query_params.order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

        # Apply pagination
        query = query.offset((query_params.page - 1) * query_params.limit).limit(
            query_params.limit
        )

        # Execute query
        result = self.db.execute(query)
        personas = result.scalars().all()

        return personas, total
