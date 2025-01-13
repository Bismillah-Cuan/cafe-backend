"""initial migration

Revision ID: e782819225fb
Revises: 37bd7966e661
Create Date: 2024-12-25 02:31:15.806367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e782819225fb'
down_revision: Union[str, None] = '37bd7966e661'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
