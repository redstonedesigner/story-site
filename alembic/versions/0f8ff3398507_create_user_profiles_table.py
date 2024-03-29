"""Create user_profiles table

Revision ID: 0f8ff3398507
Revises: abfdfe3c37dc
Create Date: 2021-05-25 10:10:01.182809+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f8ff3398507'
down_revision = 'abfdfe3c37dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('education', sa.Text(), nullable=True),
    sa.Column('location', sa.Text(), nullable=True),
    sa.Column('skills', sa.Text(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['users.id'], name=op.f('fk_user_profiles_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_profiles'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profiles')
    # ### end Alembic commands ###
