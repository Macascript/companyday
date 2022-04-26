"""UserMixin Dependencies

Revision ID: f11f673af54d
Revises: 3a33ce6e80f1
Create Date: 2022-04-24 21:24:11.230768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f11f673af54d'
down_revision = '3a33ce6e80f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('empresa', sa.Column('is_confirmed', sa.Boolean(), nullable=True))
    op.drop_column('empresa', 'is_active')
    op.drop_column('empresa', 'is_created')
    op.drop_column('empresa', 'is_updated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('empresa', sa.Column('is_updated', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('empresa', sa.Column('is_created', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('empresa', sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('empresa', 'is_confirmed')
    # ### end Alembic commands ###