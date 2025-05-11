"""create user_organization  table

Revision ID: f2100df96764
Revises: 955d8234e061
Create Date: 2025-05-10 12:50:40.702957+00:00

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f2100df96764"
down_revision: Union[str, None] = "955d8234e061"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TYPE org_roles AS ENUM ('owner', 'member');
    CREATE TABLE user_organization (
        user_id UUID REFERENCES users(id),
        organization_id UUID REFERENCES organizations(id),
        role org_roles DEFAULT 'member',
        created_at TIMESTAMP DEFAULT NOW(),
        PRIMARY KEY (user_id, organization_id)
    );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE user_organization")
    op.execute("DROP TYPE org_roles")
