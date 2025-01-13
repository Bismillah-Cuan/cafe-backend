"""initial migration

Revision ID: 37bd7966e661
Revises: ea1258f451f3
Create Date: 2024-12-25 02:16:06.130163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37bd7966e661'
down_revision: Union[str, None] = 'ea1258f451f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
