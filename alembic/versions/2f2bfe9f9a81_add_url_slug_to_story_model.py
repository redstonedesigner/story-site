"""Add URL slug to story model

Revision ID: 2f2bfe9f9a81
Revises: 5562577e4f0d
Create Date: 2021-05-04 09:22:01.460423+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f2bfe9f9a81'
down_revision = '5562577e4f0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url_slug', sa.String(length=32), nullable=False))
        batch_op.create_unique_constraint('stories_url_slug', ['url_slug'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stories', schema=None) as batch_op:
        batch_op.drop_constraint('stories_url_slug', type_='unique')
        batch_op.drop_column('url_slug')

    # ### end Alembic commands ###
