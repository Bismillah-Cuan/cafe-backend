"""initial migration

Revision ID: 244960752806
Revises: 9f7f3c6f0fd7
Create Date: 2024-12-25 02:11:43.727702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '244960752806'
down_revision: Union[str, None] = '9f7f3c6f0fd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
