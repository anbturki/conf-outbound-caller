from typing import Annotated

from api.resources.user.models.user import User
from core.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from .models.organization import Organization
from .models.user_organization import OrgRoles, UserOrganization


class OrganizationService:
    def __init__(self, db: Session):
        self.db = db

    def get_one(self, org_id: str) -> Organization:
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    def add_member(
        self,
        org: Organization,
        user: User,
        role: OrgRoles = OrgRoles.MEMBER,
        commit: bool = True,
    ) -> UserOrganization:
        org_user = UserOrganization()

        org_user.org_id = org.id
        org_user.user_id = user.id
        org_user.role = role

        self.db.add(org_user)

        if commit:
            self.db.commit()
            self.db.refresh(org_user)
        else:
            self.db.flush([org_user])

        return org_user

    def save(
        self,
        data: Organization,
        commit: bool = True,
    ) -> Organization:
        self.db.add(data)
        if commit:
            self.db.commit()
            self.db.refresh(data)
        else:
            self.db.flush([data])
        return data


def get_organization_service(
    db: Annotated[Session, Depends(get_db)],
) -> OrganizationService:
    return OrganizationService(db)
