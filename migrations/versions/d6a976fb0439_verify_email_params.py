"""verify_email_params

Revision ID: d6a976fb0439
Revises: 9c56f540f58f
Create Date: 2019-11-21 20:37:21.236763

"""
from alembic import op
import sqlalchemy as sa
import time
import logging
from app import db
from app.sqldb.models import User
import datetime


# revision identifiers, used by Alembic.
revision = 'd6a976fb0439'
down_revision = '9c56f540f58f'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(op.f('fk_prognosis_user_id_user'), 'prognosis', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('email_verified', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('register_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'register_date')
    op.drop_column('user', 'email_verified')
    op.drop_constraint(op.f('fk_prognosis_user_id_user'), 'prognosis', type_='foreignkey')
    # ### end Alembic commands ###
