"""Redid country table

Revision ID: 6bc36b1b1d6f
Revises: 1e824312edc9
Create Date: 2021-01-05 11:36:59.513520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bc36b1b1d6f'
down_revision = '1e824312edc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('confirmed', sa.Integer(), nullable=True),
    sa.Column('deaths', sa.Integer(), nullable=True),
    sa.Column('case_fatality', sa.Float(), nullable=True),
    sa.Column('deaths_per_100k', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('country')
    # ### end Alembic commands ###
