"""add forign-key to posts table

Revision ID: 87a67476c73c
Revises: 9de1c36697c8
Create Date: 2022-08-02 23:45:44.954041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87a67476c73c'
down_revision = '9de1c36697c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('owner_id', table_name='posts')
    pass
