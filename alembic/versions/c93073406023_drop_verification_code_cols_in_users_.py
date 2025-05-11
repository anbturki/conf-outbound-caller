"""drop verification code cols in users table

Revision ID: c93073406023
Revises: a3c5073d6f3c
Create Date: 2025-05-10 17:57:54.903885+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c93073406023"
down_revision: Union[str, None] = "a3c5073d6f3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop verification code columns from users table
    op.drop_column("users", "password_reset_token_expires_at")
    op.drop_column("users", "password_reset_token")


def downgrade() -> None:
    """Downgrade schema."""
    # Add back verification code columns to users table
    op.add_column(
        "users", sa.Column("password_reset_token", sa.String(128), nullable=True)
    )
    op.add_column(
        "users",
        sa.Column("password_reset_token_expires_at", sa.DateTime, nullable=True),
    )
