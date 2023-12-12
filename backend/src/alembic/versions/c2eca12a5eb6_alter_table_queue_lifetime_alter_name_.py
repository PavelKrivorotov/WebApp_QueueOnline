"""Alter table queue_lifetime alter name queue_lifetimes

Revision ID: c2eca12a5eb6
Revises: 7d545c4c957d
Create Date: 2023-11-25 20:04:55.232700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2eca12a5eb6'
down_revision: Union[str, None] = '7d545c4c957d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.rename_table('queue_lifetime', 'queue_lifetimes')
    # ###


def downgrade() -> None:
    # ###
    op.rename_table('queue_lifetimes', 'queue_lifetime')
    # ###
