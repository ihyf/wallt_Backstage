"""message 01

Revision ID: 5d0033c8ddb5
Revises: 2d13b9e19733
Create Date: 2019-01-05 17:38:03.151889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d0033c8ddb5'
down_revision = '2d13b9e19733'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('edit_time', sa.DATETIME(), nullable=True),
    sa.Column('msg_content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
