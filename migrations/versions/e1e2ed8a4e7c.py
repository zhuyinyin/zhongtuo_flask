"""empty message

Revision ID: e1e2ed8a4e7c
Revises: 24ed1d0a4fb7
Create Date: 2020-05-22 00:08:52.201873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e1e2ed8a4e7c'
down_revision = '24ed1d0a4fb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=250),
               type_=sa.String(length=18),
               existing_nullable=True)
    op.alter_column('user', 'usernames',
               existing_type=mysql.VARCHAR(length=16),
               type_=sa.String(length=160),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'usernames',
               existing_type=sa.String(length=160),
               type_=mysql.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('user', 'password',
               existing_type=sa.String(length=18),
               type_=mysql.VARCHAR(length=250),
               existing_nullable=True)
    # ### end Alembic commands ###
