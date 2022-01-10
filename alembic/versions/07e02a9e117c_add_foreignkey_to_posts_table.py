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
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass