"""Drop 'account' table

Revision ID: 66f55b28d644
Revises: f1a10b258f62
Create Date: 2021-10-27 15:10:53.809695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66f55b28d644'
down_revision = 'f1a10b258f62'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('account')


def downgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('last_transaction_date', sa.DateTime),
    )
