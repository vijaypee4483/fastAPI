"""add content in post table

Revision ID: a8a0e478e0d3
Revises: 138810e4458c
Create Date: 2022-08-02 20:58:37.898003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8a0e478e0d3'
down_revision = '138810e4458c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
