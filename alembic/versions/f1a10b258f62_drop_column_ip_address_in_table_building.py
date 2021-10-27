"""Drop column 'ip-address' in table 'building'

Revision ID: f1a10b258f62
Revises: 7128269048de
Create Date: 2021-10-27 14:55:17.159767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a10b258f62'
down_revision = '7128269048de'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('building', 'ip_address')


def downgrade():
    op.add_column('building', sa.Column('ip_address', sa.String))
