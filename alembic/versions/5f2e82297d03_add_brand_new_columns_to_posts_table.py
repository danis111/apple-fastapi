"""add brand new columns to posts table

Revision ID: 5f2e82297d03
Revises: 14d520bf1a58
Create Date: 2022-01-10 19:36:34.345682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f2e82297d03'
down_revision = '14d520bf1a58'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass