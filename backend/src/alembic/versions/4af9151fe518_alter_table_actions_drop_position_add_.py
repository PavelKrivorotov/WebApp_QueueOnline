"""Alter table actions. Drop position. Add active_user_position and passive_user_position

Revision ID: 4af9151fe518
Revises: 46e44f3450fe
Create Date: 2023-11-29 14:58:47.796104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4af9151fe518'
down_revision: Union[str, None] = '46e44f3450fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.drop_column('actions', 'position')
    # ###


def downgrade() -> None:
    # ###
    op.add_column(
        'actions',
        sa.Column('position', sa.Integer())
    )
    # ###
