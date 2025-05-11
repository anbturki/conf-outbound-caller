"""alter timestamp cols on token verifications

Revision ID: 2955ec4e8f80
Revises: c93073406023
Create Date: 2025-05-11 07:41:39.868155+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2955ec4e8f80"
down_revision: Union[str, None] = "c93073406023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add timezone awareness to datetime columns."""
    # Convert all datetime columns to timezone-aware
    op.alter_column(
        "verification_tokens",
        "expires_at",
        type_=sa.DateTime(timezone=True),
        postgresql_using="expires_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "verification_tokens",
        "created_at",
        type_=sa.DateTime(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "verification_tokens",
        "updated_at",
        type_=sa.DateTime(timezone=True),
        postgresql_using="updated_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "verification_tokens",
        "verified_at",
        type_=sa.DateTime(timezone=True),
        postgresql_using="verified_at AT TIME ZONE 'UTC'",
        nullable=True,
    )


def downgrade() -> None:
    """Revert datetime columns to timezone-naive."""
    op.alter_column(
        "verification_tokens",
        "expires_at",
        type_=sa.DateTime(timezone=False),
        postgresql_using="expires_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "verification_tokens",
        "created_at",
        type_=sa.DateTime(timezone=False),
        postgresql_using="created_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "verification_tokens",
        "updated_at",
        type_=sa.DateTime(timezone=False),
        postgresql_using="updated_at AT TIME ZONE 'UTC'",
    )

    op.alter_column(
        "verification_tokens",
        "verified_at",
        type_=sa.DateTime(timezone=False),
        postgresql_using="verified_at AT TIME ZONE 'UTC'",
        nullable=True,
    )
