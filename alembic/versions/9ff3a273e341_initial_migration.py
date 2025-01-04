"""Initial migration

Revision ID: 9ff3a273e341
Revises: 3aceba538596
Create Date: 2025-01-04 17:09:49.470554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ff3a273e341'
down_revision: Union[str, None] = '3aceba538596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
