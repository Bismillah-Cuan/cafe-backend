"""initial migration

Revision ID: ea1258f451f3
Revises: 244960752806
Create Date: 2024-12-25 02:14:23.159394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea1258f451f3'
down_revision: Union[str, None] = '244960752806'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
