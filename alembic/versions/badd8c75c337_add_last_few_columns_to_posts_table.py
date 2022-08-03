"""add last few columns  to posts table

Revision ID: badd8c75c337
Revises: 87a67476c73c
Create Date: 2022-08-03 00:11:19.259820

"""
from cgitb import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'badd8c75c337'
down_revision = '87a67476c73c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                    nullable=False, server_default='true'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(),
                nullable=False, server_default=sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
