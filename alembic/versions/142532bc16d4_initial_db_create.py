"""initial db create

Revision ID: 142532bc16d4
Revises: 
Create Date: 2023-05-27 02:42:09.430891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '142532bc16d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dramas',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('short_id', sa.Integer(), nullable=False),
    sa.Column('full_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('ratings', sa.Integer(), nullable=True),
    sa.Column('watchers', sa.Integer(), nullable=True),
    sa.Column('reviews', sa.Integer(), nullable=True),
    sa.Column('native_title', sa.String(), nullable=True),
    sa.Column('known_as', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('screenwriter', sa.String(), nullable=True),
    sa.Column('director', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('episodes', sa.Integer(), nullable=True),
    sa.Column('aired', sa.String(), nullable=True),
    sa.Column('aired_on', sa.String(), nullable=True),
    sa.Column('release_date', sa.String(), nullable=True),
    sa.Column('duration', sa.String(), nullable=True),
    sa.Column('original_network', sa.String(), nullable=True),
    sa.Column('content_rating', sa.String(), nullable=True),
    sa.Column('ranked', sa.Integer(), nullable=True),
    sa.Column('popularity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_id')
    )
    op.create_table('genres',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('tags',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('movie_genres',
    sa.Column('drama_id', sa.UUID(), nullable=False),
    sa.Column('genre_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['drama_id'], ['dramas.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.PrimaryKeyConstraint('drama_id', 'genre_id')
    )
    op.create_table('movie_tags',
    sa.Column('drama_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['drama_id'], ['dramas.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('drama_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_tags')
    op.drop_table('movie_genres')
    op.drop_table('tags')
    op.drop_table('genres')
    op.drop_table('dramas')
    # ### end Alembic commands ###