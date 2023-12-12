"""Add table active_actions

Revision ID: eacb777a9ce4
Revises: 50353071ba6f
Create Date: 2023-12-08 21:13:25.638710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eacb777a9ce4'
down_revision: Union[str, None] = '50353071ba6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.create_table(
        'active_actions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),

        sa.Column('active_queue_user_id', sa.Integer(), sa.ForeignKey('queue_users.id')),
        sa.Column('passive_queue_user_id', sa.Integer(), sa.ForeignKey('queue_users.id')),
        sa.Column('action_key', sa.String(8), sa.ForeignKey('queue_actions.key')),
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_table('active_actions')
    # ###
