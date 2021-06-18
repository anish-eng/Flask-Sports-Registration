"""empty message

Revision ID: bf91a09cacf3
Revises: 0f6bdd1335b1
Create Date: 2021-05-27 17:19:04.087437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf91a09cacf3'
down_revision = '0f6bdd1335b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organiser', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('venue', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('venue')
        batch_op.drop_column('organiser')

    # ### end Alembic commands ###
