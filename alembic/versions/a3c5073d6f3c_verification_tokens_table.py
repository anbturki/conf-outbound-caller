"""verification_tokens table

Revision ID: a3c5073d6f3c
Revises: f2100df96764
Create Date: 2025-05-10 17:51:26.639859+00:00

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a3c5073d6f3c"
down_revision: Union[str, None] = "f2100df96764"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enums first
    verification_token_status = ENUM(
        "active",
        "deactivated",
        "verified",
        "expired",
        name="verificationtokenstatus",
        create_type=True,
    )
    verification_token_type = ENUM(
        "email",
        "password_reset",
        "phone_number",
        name="verificationtokentype",
        create_type=True,
    )

    op.create_table(
        "verification_tokens",
        sa.Column("id", UUID, primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column("token", sa.String(128), nullable=False),
        sa.Column("token_type", verification_token_type, nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone_number", sa.String(20), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attempts", sa.Integer, default=0),
        sa.Column("max_attempts", sa.Integer, default=5),
        sa.Column(
            "status", verification_token_status, nullable=False, default="active"
        ),
        sa.Column("deactivation_reason", sa.String, nullable=True),
        sa.Column("is_verified", sa.Boolean, default=False, nullable=False),
        sa.Column("verified_at", sa.DateTime, nullable=True),
        sa.Column("created_from_ip", sa.String(45), nullable=True),
        sa.Column("created_from_user_agent", sa.String(255), nullable=True),
        sa.Column("verified_from_ip", sa.String(45), nullable=True),
        sa.Column("verified_from_user_agent", sa.String(255), nullable=True),
        sa.Column("user_id", UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.UniqueConstraint("token_type", "email", "token", name="uq_email_token"),
        sa.UniqueConstraint(
            "token_type", "phone_number", "token", name="uq_phone_token"
        ),
    )

    # Create indexes
    op.create_index("idx_token_status", "verification_tokens", ["token", "status"])
    op.create_index(
        "idx_user_tokens", "verification_tokens", ["user_id", "token_type", "status"]
    )
    op.create_index("idx_expires_at", "verification_tokens", ["expires_at"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("verification_tokens")
    op.execute("DROP TYPE verificationtokenstatus")
    op.execute("DROP TYPE verificationtokentype")
