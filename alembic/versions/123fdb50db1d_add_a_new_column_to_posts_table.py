"""add a new column to posts table

Revision ID: 123fdb50db1d
Revises: 6a907f83c862
Create Date: 2022-01-09 21:14:35.558963

"""
from datetime import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123fdb50db1d'
down_revision = '6a907f83c862'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass