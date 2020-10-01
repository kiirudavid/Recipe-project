"""Initial Migration

Revision ID: fa301f080e01
Revises: 3591b767dbf7
Create Date: 2020-09-30 19:38:48.431005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa301f080e01'
down_revision = '3591b767dbf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('recipe_id', sa.Integer(), nullable=True))
    op.add_column('reviews', sa.Column('recipe_review', sa.String(), nullable=True))
    op.add_column('reviews', sa.Column('recipe_title', sa.String(), nullable=True))
    op.drop_column('reviews', 'movie_review')
    op.drop_column('reviews', 'movie_id')
    op.drop_column('reviews', 'movie_title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('movie_title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('reviews', sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('reviews', sa.Column('movie_review', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('reviews', 'recipe_title')
    op.drop_column('reviews', 'recipe_review')
    op.drop_column('reviews', 'recipe_id')
    # ### end Alembic commands ###
