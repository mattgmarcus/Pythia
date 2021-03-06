"""empty message

Revision ID: 1e00f3edeb11
Revises: 4715925a32e2
Create Date: 2015-02-14 16:35:06.638967

"""

# revision identifiers, used by Alembic.
revision = '1e00f3edeb11'
down_revision = '4715925a32e2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loans', 'issue_date')
    op.drop_column('loans', 'last_payment_date')
    op.drop_column('loans', 'description')
    op.drop_column('loans', 'title')
    op.drop_column('loans', 'url')
    op.drop_column('loans', 'next_payment_date')
    op.drop_column('loans', 'earliest_credit_line')
    op.drop_column('loans', 'last_credit_pulled_date')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('last_credit_pulled_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('earliest_credit_line', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('next_payment_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('last_payment_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('loans', sa.Column('issue_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    ### end Alembic commands ###
