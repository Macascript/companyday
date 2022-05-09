"""Updated password length

Revision ID: 708a99b4c096
Revises: 49c7948f0962
Create Date: 2022-05-08 21:30:48.183224

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '708a99b4c096'
down_revision = '49c7948f0962'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('empresa', sa.Column('contrasenya', sa.String(length=50), nullable=True))
    op.drop_column('empresa', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('empresa', sa.Column('password', mysql.VARCHAR(length=50), nullable=True))
    op.drop_column('empresa', 'contrasenya')
    # ### end Alembic commands ###