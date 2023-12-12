"""Alter table queues. Add column title

Revision ID: 09ae220ac1f8
Revises: 4aeeef0aa794
Create Date: 2023-11-26 11:11:04.902927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09ae220ac1f8'
down_revision: Union[str, None] = '4aeeef0aa794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.add_column(
        'queues',
        sa.Column('title', sa.String(150))
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_column('queues', 'title')
    # ###
