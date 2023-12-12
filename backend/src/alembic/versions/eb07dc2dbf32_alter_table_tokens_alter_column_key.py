"""Alter table tokens alter column key

Revision ID: eb07dc2dbf32
Revises: eacb777a9ce4
Create Date: 2023-12-12 13:52:28.569629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb07dc2dbf32'
down_revision: Union[str, None] = 'eacb777a9ce4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.drop_column('tokens', 'id')
    op.create_primary_key('tokens_pkey', 'tokens', ['key'])
    # ###


def downgrade() -> None:
    # ###
    op.drop_constraint('tokens_pkey', 'tokens', 'primary')
    op.add_column(
        'tokens',
        sa.Column('id', sa.Integer(), primary_key=True, index=True)
    )
    # ###
