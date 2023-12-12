"""Add table queue_users

Revision ID: 0a1e1a157f01
Revises: 4af9151fe518
Create Date: 2023-11-29 15:01:32.462467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a1e1a157f01'
down_revision: Union[str, None] = '4af9151fe518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.create_table(
        'queue_users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('position', sa.Integer()),

        sa.Column('queue_key', sa.String(6), sa.ForeignKey('queues.key')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_table('queue_users')
    # ###
