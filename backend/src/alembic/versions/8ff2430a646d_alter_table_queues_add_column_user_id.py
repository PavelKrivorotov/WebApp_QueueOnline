"""Alter table queues. Add column user_id

Revision ID: 8ff2430a646d
Revises: 3cd3419b4604
Create Date: 2023-11-26 21:31:32.726399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ff2430a646d'
down_revision: Union[str, None] = '3cd3419b4604'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.add_column(
        'queues',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'))
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_column('queues', 'user_id')
    # ###
