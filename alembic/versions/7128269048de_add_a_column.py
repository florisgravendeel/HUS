"""Add a column

Revision ID: 7128269048de
Revises: 1ff20a6fdf37
Create Date: 2021-10-27 11:20:36.648128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7128269048de'
down_revision = '1ff20a6fdf37'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')

