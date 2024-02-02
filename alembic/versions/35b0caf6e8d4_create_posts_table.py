"""create posts table

Revision ID: 35b0caf6e8d4
Revises: 
Create Date: 2024-02-01 01:51:38.788996

"""
from typing import Sequence, Union

from alembic import op   #object from alembic
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35b0caf6e8d4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:    #to make changes
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable= False))        #grabbing the sqlalchemy object sa for column
    pass


def downgrade() -> None:   # handles rolling it back or deleting
    op.drop_table('posts')
    pass
