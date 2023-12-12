"""Alter queues table. Add new column is_active

Revision ID: 3cd3419b4604
Revises: 09ae220ac1f8
Create Date: 2023-11-26 20:23:18.996554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cd3419b4604'
down_revision: Union[str, None] = '09ae220ac1f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.add_column(
        'queues',
        sa.Column('is_active', sa.Boolean(), default=True)
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_column('queues', 'is_active')
    # ###
