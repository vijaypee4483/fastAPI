"""create post table

Revision ID: 138810e4458c
Revises: 
Create Date: 2022-08-02 20:51:46.710733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '138810e4458c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
