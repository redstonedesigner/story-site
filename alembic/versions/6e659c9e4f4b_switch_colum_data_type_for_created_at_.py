"""Switch colum data type for created_at and modified_at

Revision ID: 6e659c9e4f4b
Revises: 5df368b5a5b6
Create Date: 2021-05-05 13:22:38.262743+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e659c9e4f4b'
down_revision = '5df368b5a5b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('story_chapters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('story_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['story_id'], ['stories.id'], name='chapter_story_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('id')
    )
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('multiple_chapters', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.drop_column('multiple_chapters')

    op.drop_table('story_chapters')
    # ### end Alembic commands ###
