"""Update PO db and PO relations

Revision ID: b6ef6a3e645f
Revises: e121d6d82a28
Create Date: 2025-01-14 16:05:23.171298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6ef6a3e645f'
down_revision: Union[str, None] = 'e121d6d82a28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
