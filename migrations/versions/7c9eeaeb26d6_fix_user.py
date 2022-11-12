"""fix user

Revision ID: 7c9eeaeb26d6
Revises: 7af649df473f
Create Date: 2022-11-12 09:18:01.022039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c9eeaeb26d6'
down_revision = '7af649df473f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('USER', 'UserName',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('USER', 'Password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('USER', 'Password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('USER', 'UserName',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
