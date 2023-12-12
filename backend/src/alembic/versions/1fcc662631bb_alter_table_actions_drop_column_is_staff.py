"""Alter table actions. Drop column is_staff

Revision ID: 1fcc662631bb
Revises: 8ff2430a646d
Create Date: 2023-11-26 21:46:14.207489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fcc662631bb'
down_revision: Union[str, None] = '8ff2430a646d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.drop_column('actions', 'is_staff')
    # ###


def downgrade() -> None:
    # ###
    op.add_column(
        'actions',
        sa.Column('is_staff', sa.Boolean(), default=False)
    )
    # ###
