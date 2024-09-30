from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7639056bb137"
down_revision: Union[str, None] = "6736f5b26c74"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
