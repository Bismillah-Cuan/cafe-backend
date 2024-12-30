"""change raw_material_id in pr model to not unique

Revision ID: 14bdc5672716
Revises: fdfbb8d1635f
Create Date: 2024-12-30 13:07:43.873442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14bdc5672716'
down_revision: Union[str, None] = 'fdfbb8d1635f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
