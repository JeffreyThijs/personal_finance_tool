"""added last prognosis viewed

Revision ID: f6b1b2443b54
Revises: d6a976fb0439
Create Date: 2019-11-22 23:55:47.623878

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f6b1b2443b54'
down_revision = 'd6a976fb0439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_prognosis_viewed', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_prognosis_viewed')
    # ### end Alembic commands ###