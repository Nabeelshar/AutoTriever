"""init database

Revision ID: cd1b12ec4c1b
Revises: 
Create Date: 2020-11-30 04:29:56.971663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd1b12ec4c1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nu_release_item',
    sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('actual_target', sa.Text(), nullable=True),
    sa.Column('page_title', sa.Text(), nullable=True),
    sa.Column('fetch_tries', sa.Integer(), nullable=True),
    sa.Column('seriesname', sa.Text(), nullable=False),
    sa.Column('releaseinfo', sa.Text(), nullable=True),
    sa.Column('groupinfo', sa.Text(), nullable=False),
    sa.Column('referrer', sa.Text(), nullable=False),
    sa.Column('outbound_wrapper', sa.Text(), nullable=False),
    sa.Column('release_date', sa.DateTime(), nullable=False),
    sa.Column('first_seen', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('outbound_wrapper'),
    sa.UniqueConstraint('seriesname', 'releaseinfo', 'groupinfo', 'outbound_wrapper')
    )
    op.create_index(op.f('ix_nu_release_item_groupinfo'), 'nu_release_item', ['groupinfo'], unique=False)
    op.create_index(op.f('ix_nu_release_item_seriesname'), 'nu_release_item', ['seriesname'], unique=False)
    op.create_table('web_pages',
    sa.Column('id', sa.BigInteger().with_variant(sa.Integer(), 'sqlite'), nullable=False),
    sa.Column('state', sa.Enum('new', 'fetching', 'complete', 'error', name='dlstate_enum'), nullable=False),
    sa.Column('errno', sa.Integer(), nullable=True),
    sa.Column('url', sa.Text(), nullable=False),
    sa.Column('mimetype', sa.Text(), nullable=True),
    sa.Column('is_text', sa.Boolean(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('fetchtime', sa.DateTime(), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_web_pages_fetchtime'), 'web_pages', ['fetchtime'], unique=False)
    op.create_index(op.f('ix_web_pages_state'), 'web_pages', ['state'], unique=False)
    op.create_index(op.f('ix_web_pages_url'), 'web_pages', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_web_pages_url'), table_name='web_pages')
    op.drop_index(op.f('ix_web_pages_state'), table_name='web_pages')
    op.drop_index(op.f('ix_web_pages_fetchtime'), table_name='web_pages')
    op.drop_table('web_pages')
    op.drop_index(op.f('ix_nu_release_item_seriesname'), table_name='nu_release_item')
    op.drop_index(op.f('ix_nu_release_item_groupinfo'), table_name='nu_release_item')
    op.drop_table('nu_release_item')
    # ### end Alembic commands ###