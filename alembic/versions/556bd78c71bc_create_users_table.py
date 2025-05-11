"""create users table

Revision ID: 556bd78c71bc
Revises:
Create Date: 2025-05-10 12:50:08.410026+00:00

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "556bd78c71bc"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        email VARCHAR NOT NULL UNIQUE,
        hashed_password VARCHAR NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        first_name VARCHAR,
        last_name VARCHAR,
        is_email_verified BOOLEAN DEFAULT FALSE,
        active_organization_id UUID,
        terms_accepted BOOLEAN DEFAULT FALSE,
        password_reset_token VARCHAR,
        password_reset_token_expires_at TIMESTAMP,
        last_login TIMESTAMP,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    CREATE INDEX ix_users_email ON users(email);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX ix_users_email")
    op.execute("DROP TABLE users")
