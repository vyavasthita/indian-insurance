"""update userprofile model

Revision ID: 6a275c9c288c
Revises: 61cd9afb9169
Create Date: 2023-06-03 13:54:41.604665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a275c9c288c'
down_revision = '61cd9afb9169'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userprofile', schema=None) as batch_op:
        batch_op.drop_column('activation_status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('userprofile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('activation_status', sa.VARCHAR(length=10), nullable=True))

    # ### end Alembic commands ###
