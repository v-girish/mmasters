"""Fix director column name typo in movie snapshots table

Revision ID: dc15a018c241
Revises: a12ec42582d6
Create Date: 2020-06-13 12:41:37.284817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc15a018c241'
down_revision = 'a12ec42582d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie_snapshots', sa.Column('director', sa.String(), nullable=True))
    op.drop_column('movie_snapshots', 'directory')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie_snapshots', sa.Column('directory', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('movie_snapshots', 'director')
    # ### end Alembic commands ###