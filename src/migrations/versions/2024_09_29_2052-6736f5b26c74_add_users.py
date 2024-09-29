"""add users

Revision ID: 6736f5b26c74
Revises: e058e288b288
Create Date: 2024-09-29 20:52:40.925112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6736f5b26c74"
down_revision: Union[str, None] = "e058e288b288"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
