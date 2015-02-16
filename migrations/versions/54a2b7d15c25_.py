"""empty message

Revision ID: 54a2b7d15c25
Revises: 22bbd75e514b
Create Date: 2015-02-16 09:55:56.977772

"""

# revision identifiers, used by Alembic.
revision = '54a2b7d15c25'
down_revision = '22bbd75e514b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rejected_loans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('loan_amount', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('risk_score', sa.Integer(), nullable=True),
    sa.Column('debt_to_income', sa.Integer(), nullable=True),
    sa.Column('zip_code', sa.String(), nullable=True),
    sa.Column('address_state', sa.String(), nullable=True),
    sa.Column('employment_length', sa.Integer(), nullable=True),
    sa.Column('policy_code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rejected_loans')
    ### end Alembic commands ###
