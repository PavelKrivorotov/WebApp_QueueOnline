"""Add tables queue_actions and historyes

Revision ID: 7d545c4c957d
Revises: 4654b3acb11c
Create Date: 2023-11-25 19:33:16.539464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '7d545c4c957d'
down_revision: Union[str, None] = '4654b3acb11c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'queue_actions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('action', sa.String(64), unique=True),
        sa.Column('detail', sa.Text()),

        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'historyes',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('date', sa.DateTime(), server_default=func.now()),

        sa.Column('active_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('passive_user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('queue_id', sa.Integer(), sa.ForeignKey('queues.id')),
        sa.Column('action_id', sa.Integer(), sa.ForeignKey('queue_actions.id')),

        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('queue_actions')
    op.drop_table('historyes')
    # ### end Alembic commands ###