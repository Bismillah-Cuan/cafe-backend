"""initial migration

Revision ID: fdfbb8d1635f
Revises: e782819225fb
Create Date: 2024-12-25 02:32:05.496185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdfbb8d1635f'
down_revision: Union[str, None] = 'e782819225fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
