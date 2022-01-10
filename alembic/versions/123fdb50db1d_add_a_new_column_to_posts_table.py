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
    op.create_table('users',
        sa.Column('user_id',sa.Integer(),nullable=False),
        sa.Column('email',sa.String(),nullable=False),
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'),nullable=False),
        sa.Column('user_id',sa.Integer(),nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')

    )
    pass


def downgrade():
    op.drop_table('users')
    pass
