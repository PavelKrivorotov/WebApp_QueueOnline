"""Alter table actions. Alter queue_key

Revision ID: 760730b108f0
Revises: 8083c7441127
Create Date: 2023-11-29 17:26:29.256908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '760730b108f0'
down_revision: Union[str, None] = '8083c7441127'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.alter_column('actions', 'queue_key', type_=sa.String(64))
    # ###


def downgrade() -> None:
    pass
