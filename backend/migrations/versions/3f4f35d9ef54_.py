"""empty message

Revision ID: 3f4f35d9ef54
Revises: a45589d92e70
Create Date: 2023-06-02 17:56:52.189356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f4f35d9ef54'
down_revision = 'a45589d92e70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insuranceplan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insurance_plan_name', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('insurance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('insured_amount', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('insurance_plan_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['insurance_plan_id'], ['insuranceplan.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=100), nullable=True))
        batch_op.alter_column('email_address',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=60),
               existing_nullable=True)
        batch_op.drop_column('insured_amount')
        batch_op.drop_column('insurance_plan_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('insurance_plan_name', sa.VARCHAR(length=200), nullable=True))
        batch_op.add_column(sa.Column('insured_amount', sa.INTEGER(), nullable=True))
        batch_op.alter_column('email_address',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.drop_column('password')

    op.drop_table('insurance')
    op.drop_table('insuranceplan')
    # ### end Alembic commands ###
