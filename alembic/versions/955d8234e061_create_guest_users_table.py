"""create guest users table

Revision ID: 955d8234e061
Revises: 6aa92939bb64
Create Date: 2025-05-10 12:50:22.483089+00:00

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "955d8234e061"
down_revision: Union[str, None] = "6aa92939bb64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE TYPE guest_session_status AS ENUM ('linked', 'unlinked');
    CREATE TABLE guest_sessions (
        id VARCHAR PRIMARY KEY,
        ip_address VARCHAR NOT NULL,
        user_agent VARCHAR NOT NULL,
        linked_user_id VARCHAR,
        session_status guest_session_status DEFAULT 'unlinked',
        created_at TIMESTAMP DEFAULT NOW(),
        last_active_at TIMESTAMP DEFAULT NOW()
    );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE guest_sessions")
    op.execute("DROP TYPE guest_session_status")
