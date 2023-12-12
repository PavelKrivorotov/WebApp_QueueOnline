"""Alter table actions. Add columns position and is_staff

Revision ID: 4aeeef0aa794
Revises: 70467c9d5e9a
Create Date: 2023-11-25 22:57:31.133568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aeeef0aa794'
down_revision: Union[str, None] = '70467c9d5e9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.add_column(
        'actions',
        sa.Column('position', sa.Integer())
    )
    op.add_column(
        'actions',
        sa.Column('is_staff', sa.Boolean, default=False)
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_column('actions', 'position')
    op.drop_column('actions', 'is_staff')
    # ###
