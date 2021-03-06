"""empty message

Revision ID: 1c3e6f199f86
Revises: 6e7972f48883
Create Date: 2021-11-15 21:43:39.262961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c3e6f199f86'
down_revision = '6e7972f48883'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile_lookup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('social_profile_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['social_profile_id'], ['social_media.social_profile.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['social_media.user_account.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='social_media'
    )
    op.create_index(op.f('ix_social_media_profile_lookup_social_profile_id'), 'profile_lookup', ['social_profile_id'], unique=False, schema='social_media')
    op.create_index(op.f('ix_social_media_profile_lookup_user_id'), 'profile_lookup', ['user_id'], unique=False, schema='social_media')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_social_media_profile_lookup_user_id'), table_name='profile_lookup', schema='social_media')
    op.drop_index(op.f('ix_social_media_profile_lookup_social_profile_id'), table_name='profile_lookup', schema='social_media')
    op.drop_table('profile_lookup', schema='social_media')
    # ### end Alembic commands ###
