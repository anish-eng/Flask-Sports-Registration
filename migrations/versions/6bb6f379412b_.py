"""empty message

Revision ID: 6bb6f379412b
Revises: bf91a09cacf3
Create Date: 2021-05-28 17:34:46.389341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb6f379412b'
down_revision = 'bf91a09cacf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profilepic', sa.String(length=20), nullable=False))
        batch_op.alter_column('enddate',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('event_description',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('event_title',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('organiser',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('registrationend',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('registrationstart',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('startdate',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('venue',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('venue',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('startdate',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('registrationstart',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('registrationend',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('organiser',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('event_title',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('event_description',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('enddate',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.drop_column('profilepic')

    # ### end Alembic commands ###
