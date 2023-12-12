"""Alter table queue_users. Alter column queue_key

Revision ID: 9387d0d82248
Revises: 760730b108f0
Create Date: 2023-11-29 17:33:55.850038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9387d0d82248'
down_revision: Union[str, None] = '760730b108f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.alter_column('queue_users', 'queue_key', type_=sa.String(64))
    # ###


def downgrade() -> None:
    pass
