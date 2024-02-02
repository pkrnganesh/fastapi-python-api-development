"""add content column to posts table

Revision ID: 827eb3818222
Revises: 35b0caf6e8d4
Create Date: 2024-02-03 00:32:55.504245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '827eb3818222'
down_revision: Union[str, None] = '35b0caf6e8d4'   #making union of old data too
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
