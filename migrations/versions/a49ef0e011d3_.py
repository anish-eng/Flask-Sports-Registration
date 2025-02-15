"""empty message

Revision ID: a49ef0e011d3
Revises: 251c80a1b276
Create Date: 2021-05-26 13:01:30.347254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a49ef0e011d3'
down_revision = '251c80a1b276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grrno', sa.Integer(), nullable=False))
        batch_op.create_unique_constraint(None, ['grrno'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('grrno')

    # ### end Alembic commands ###
