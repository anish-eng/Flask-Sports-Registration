"""empty message

Revision ID: 9bb13c93bd7f
Revises: 6bb6f379412b
Create Date: 2021-05-29 15:03:39.358715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb13c93bd7f'
down_revision = '6bb6f379412b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersport', schema=None) as batch_op:
        batch_op.drop_column('user_sportid')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usersport', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_sportid', sa.INTEGER(), nullable=False))

    # ### end Alembic commands ###
