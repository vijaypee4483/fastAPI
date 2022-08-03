"""add user table

Revision ID: 9de1c36697c8
Revises: a8a0e478e0d3
Create Date: 2022-08-02 21:11:47.363526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9de1c36697c8'
down_revision = 'a8a0e478e0d3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
