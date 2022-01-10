"""add a few column to post table

Revision ID: add3ac4d73a8
Revises: 07e02a9e117c
Create Date: 2022-01-09 22:14:25.347377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add3ac4d73a8'
down_revision = '07e02a9e117c'
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