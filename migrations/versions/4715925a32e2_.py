"""empty message

Revision ID: 4715925a32e2
Revises: 130ac7a73b26
Create Date: 2015-02-13 20:57:21.353475

"""

# revision identifiers, used by Alembic.
revision = '4715925a32e2'
down_revision = '130ac7a73b26'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('is_test_data', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('loans', 'is_test_data')
    ### end Alembic commands ###