"""Alter table actions. Add columns active_user_position and passive_user_position

Revision ID: 8083c7441127
Revises: 0a1e1a157f01
Create Date: 2023-11-29 17:09:34.816681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8083c7441127'
down_revision: Union[str, None] = '0a1e1a157f01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.add_column(
        'actions',
        sa.Column('active_user_position', sa.Integer())
    )
    op.add_column(
        'actions',
        sa.Column('passive_user_position', sa.Integer())
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_column('actions', 'active_user_position')
    op.drop_column('actions', 'passive_user_position')
    # ###
