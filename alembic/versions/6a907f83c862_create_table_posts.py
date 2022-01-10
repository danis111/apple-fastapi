"""create table posts

Revision ID: 6a907f83c862
Revises: 
Create Date: 2022-01-09 19:55:55.968206

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import Column


# revision identifiers, used by Alembic.
revision = '6a907f83c862'
down_revision = None 
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
