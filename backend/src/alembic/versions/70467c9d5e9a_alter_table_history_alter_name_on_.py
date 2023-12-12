"""Alter table history. Alter name on actions

Revision ID: 70467c9d5e9a
Revises: fb90e6f1f443
Create Date: 2023-11-25 22:30:01.796176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70467c9d5e9a'
down_revision: Union[str, None] = 'fb90e6f1f443'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.rename_table('historyes', 'actions')
    # ###


def downgrade() -> None:
    # ###
    op.rename_table('actions', 'historyes')
    # ###
