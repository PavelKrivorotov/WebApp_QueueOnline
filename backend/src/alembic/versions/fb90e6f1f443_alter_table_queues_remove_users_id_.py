"""Alter table queues. Remove users_id references

Revision ID: fb90e6f1f443
Revises: c2eca12a5eb6
Create Date: 2023-11-25 22:21:34.726435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb90e6f1f443'
down_revision: Union[str, None] = 'c2eca12a5eb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.drop_column('queues', 'user_id')
    # ###


def downgrade() -> None:
    # ###
    op.add_column(
        'queues',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'))
    )
    # ###
