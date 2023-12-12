"""Rework database

Revision ID: 46e44f3450fe
Revises: d2c4c863a333
Create Date: 2023-11-28 18:09:36.879454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46e44f3450fe'
down_revision: Union[str, None] = 'd2c4c863a333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.drop_table('actions')
    op.drop_table('queue_actions')
    op.drop_table('queues')
    op.drop_table('queue_lifetimes')

    op.create_table(
        'queue_lifetimes',
        sa.Column('key', sa.String(8), primary_key=True, index=True),
        sa.Column('lifetime', sa.Interval(), unique=True)
    )
    op.create_table(
        'queues',
        sa.Column('key', sa.String(64), primary_key=True, index=True),
        sa.Column('title', sa.String(150)),
        sa.Column('created', sa.DateTime(), server_default=sa.sql.func.now()),
        sa.Column('is_active', sa.Boolean(), default=True),

        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('queue_lifetime_key', sa.String(8), sa.ForeignKey('queue_lifetimes.key'))
    )
    op.create_table(
        'queue_actions',
        sa.Column('key', sa.String(8), primary_key=True, index=True),
        sa.Column('action', sa.String(64), unique=True),
        sa.Column('detail', sa.Text())
    )
    op.create_table(
        'actions',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('date', sa.DateTime(), server_default=sa.sql.func.now()),
        sa.Column('position', sa.Integer()),

        sa.Column('active_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('passive_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('queue_key', sa.String(8), sa.ForeignKey('queues.key')),
        sa.Column('action_key', sa.String(8), sa.ForeignKey('queue_actions.key')),
    )
    # ###


def downgrade() -> None:
    # ###
    pass
    # ###
