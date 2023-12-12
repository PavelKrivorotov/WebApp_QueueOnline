"""Add table queue_roles. Ater table queue_users, add column queue_role

Revision ID: 50353071ba6f
Revises: 9387d0d82248
Create Date: 2023-12-04 19:10:10.155767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50353071ba6f'
down_revision: Union[str, None] = '9387d0d82248'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.create_table(
        'queue_roles',
        sa.Column('key', sa.String(8), primary_key=True, index=True),
        sa.Column('role', sa.String(64), unique=True),
        sa.Column('detail', sa.Text()),
    )

    op.add_column(
        'queue_users',
        sa.Column('queue_role', sa.String(8), sa.ForeignKey('queue_roles.key'))
    )
    # ###


def downgrade() -> None:
    # ###
    op.drop_column('queue_users', 'queue_role')
    op.drop_table('queue_roles')
    # ###
