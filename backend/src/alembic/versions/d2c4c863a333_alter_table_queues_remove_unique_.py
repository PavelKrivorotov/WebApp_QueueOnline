"""Alter table queues. Remove unique constraint on queue_lifetime_id

Revision ID: d2c4c863a333
Revises: 1fcc662631bb
Create Date: 2023-11-27 00:22:51.623473

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2c4c863a333'
down_revision: Union[str, None] = '1fcc662631bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ###
    op.drop_constraint('queues_queue_lifetime_id_key', 'queues')
    # ###


def downgrade() -> None:
    # ###
    op.create_unique_constraint('queues_queue_lifetime_id_key', 'queues')
    # ###
