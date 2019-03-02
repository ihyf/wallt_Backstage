"""SlideShow 01091352

Revision ID: f25fa14b089b
Revises: cbd6792f23f5
Create Date: 2019-01-09 13:52:19.405933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f25fa14b089b'
down_revision = 'cbd6792f23f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('slide_show',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('slide_show_name', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('image1', sa.LargeBinary(length=2048), nullable=True),
    sa.Column('image2', sa.LargeBinary(length=2048), nullable=True),
    sa.Column('image3', sa.LargeBinary(length=2048), nullable=True),
    sa.Column('edit_time', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('slide_show')
    # ### end Alembic commands ###