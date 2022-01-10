"""add foreignkey to posts table

Revision ID: 07e02a9e117c
Revises: 123fdb50db1d
Create Date: 2022-01-09 21:43:30.422968

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '07e02a9e117c'
down_revision = '123fdb50db1d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass