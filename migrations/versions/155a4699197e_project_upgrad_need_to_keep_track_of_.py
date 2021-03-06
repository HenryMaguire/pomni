"""project upgrad: need to keep track of what session we're on

Revision ID: 155a4699197e
Revises: 6f41b7a54003
Create Date: 2018-08-23 23:57:08.703445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '155a4699197e'
down_revision = '6f41b7a54003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('current_stage', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'current_stage')
    # ### end Alembic commands ###
