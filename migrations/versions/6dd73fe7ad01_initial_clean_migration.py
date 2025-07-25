"""initial clean migration

Revision ID: 6dd73fe7ad01
Revises: 
Create Date: 2025-07-20 11:28:36.659131

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6dd73fe7ad01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('icon_url', sa.String(length=255), nullable=True),
    sa.Column('parent_category_id', sa.Integer(), nullable=True),
    sa.Column('is_agricultural_specific', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_category_id'], ['categories.category_id'], ),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('countries',
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('country_id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('name')
    )
    op.create_table('crops',
    sa.Column('crop_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('scientific_name', sa.String(length=100), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('growing_season', sa.String(length=50), nullable=True),
    sa.Column('climate_requirements', sa.Text(), nullable=True),
    sa.Column('water_requirements', sa.String(length=50), nullable=True),
    sa.Column('soil_type', sa.String(length=100), nullable=True),
    sa.Column('maturity_days', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('crop_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('livestock',
    sa.Column('livestock_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('breed', sa.String(length=100), nullable=True),
    sa.Column('purpose', sa.String(length=100), nullable=True),
    sa.Column('climate_suitability', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('livestock_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('states_provinces',
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.country_id'], ),
    sa.PrimaryKeyConstraint('state_id')
    )
    op.create_table('locations',
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.Column('latitude', sa.Numeric(precision=10, scale=8), nullable=True),
    sa.Column('longitude', sa.Numeric(precision=11, scale=8), nullable=True),
    sa.Column('climate_zone', sa.String(length=50), nullable=True),
    sa.Column('elevation', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.country_id'], ),
    sa.ForeignKeyConstraint(['state_id'], ['states_provinces.state_id'], ),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('farm_size', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('farm_size_unit', sa.String(length=10), nullable=True),
    sa.Column('farming_experience', sa.Integer(), nullable=True),
    sa.Column('farming_type', sa.String(length=50), nullable=True),
    sa.Column('primary_language', sa.String(length=10), nullable=True),
    sa.Column('avatar_url', sa.String(length=255), nullable=True),
    sa.Column('cover_image_url', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('whatsapp_number', sa.String(length=20), nullable=True),
    sa.Column('is_phone_verified', sa.Boolean(), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('join_date', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('communities',
    sa.Column('community_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('community_type', sa.String(length=50), nullable=False),
    sa.Column('focus_crops', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('location_city', sa.String(length=100), nullable=True),
    sa.Column('location_country', sa.String(length=100), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('community_id')
    )
    op.create_table('consultations',
    sa.Column('consultation_id', sa.UUID(), nullable=False),
    sa.Column('expert_id', sa.UUID(), nullable=False),
    sa.Column('farmer_id', sa.UUID(), nullable=False),
    sa.Column('consultation_type', sa.String(length=20), nullable=False),
    sa.Column('scheduled_start', sa.DateTime(), nullable=False),
    sa.Column('scheduled_end', sa.DateTime(), nullable=False),
    sa.Column('topic', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('related_crops', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('farm_location_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('payment_status', sa.String(length=20), nullable=True),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['expert_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['farm_location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['farmer_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('consultation_id')
    )
    op.create_table('expert_profiles',
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('specializations', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('certification', sa.String(length=255), nullable=True),
    sa.Column('education', sa.String(length=255), nullable=True),
    sa.Column('years_experience', sa.Integer(), nullable=False),
    sa.Column('hourly_rate', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('availability_status', sa.String(length=20), nullable=True),
    sa.Column('languages_spoken', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('service_areas', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('rating', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('review_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('profile_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('posts',
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('excerpt', sa.Text(), nullable=True),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('featured_image_url', sa.String(length=255), nullable=True),
    sa.Column('season_relevance', sa.String(length=50), nullable=True),
    sa.Column('applicable_locations', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('related_crops', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.Column('read_time', sa.Integer(), nullable=True),
    sa.Column('is_featured', sa.Boolean(), nullable=True),
    sa.Column('language', sa.String(length=10), nullable=True),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('user_crops',
    sa.Column('user_crop_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('crop_id', sa.Integer(), nullable=False),
    sa.Column('area_planted', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('area_unit', sa.String(length=10), nullable=True),
    sa.Column('planting_date', sa.Date(), nullable=True),
    sa.Column('expected_harvest', sa.Date(), nullable=True),
    sa.Column('actual_harvest', sa.Date(), nullable=True),
    sa.Column('yield_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('yield_unit', sa.String(length=10), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('season', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['crop_id'], ['crops.crop_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_crop_id')
    )
    op.create_table('user_expertise',
    sa.Column('expertise_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('expertise', sa.String(length=100), nullable=False),
    sa.Column('years_experience', sa.Integer(), nullable=True),
    sa.Column('certification', sa.String(length=255), nullable=True),
    sa.Column('institution', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('expertise_id')
    )
    op.create_table('user_follows',
    sa.Column('follow_id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.UUID(), nullable=False),
    sa.Column('following_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['following_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('follow_id'),
    sa.UniqueConstraint('follower_id', 'following_id', name='unique_follow')
    )
    op.create_table('comments',
    sa.Column('comment_id', sa.UUID(), nullable=False),
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('parent_comment_id', sa.UUID(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_comment_id'], ['comments.comment_id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('community_members',
    sa.Column('community_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['community_id'], ['communities.community_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('community_id', 'user_id')
    )
    op.create_table('community_posts',
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('community_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['community_id'], ['communities.community_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('expert_reviews',
    sa.Column('review_id', sa.UUID(), nullable=False),
    sa.Column('expert_id', sa.UUID(), nullable=False),
    sa.Column('reviewer_id', sa.UUID(), nullable=False),
    sa.Column('consultation_id', sa.UUID(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['consultation_id'], ['consultations.consultation_id'], ),
    sa.ForeignKeyConstraint(['expert_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['reviewer_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('review_id')
    )
    op.create_table('post_likes',
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.create_table('post_tags',
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.post_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.tag_id'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tags')
    op.drop_table('post_likes')
    op.drop_table('expert_reviews')
    op.drop_table('community_posts')
    op.drop_table('community_members')
    op.drop_table('comments')
    op.drop_table('user_follows')
    op.drop_table('user_expertise')
    op.drop_table('user_crops')
    op.drop_table('posts')
    op.drop_table('expert_profiles')
    op.drop_table('consultations')
    op.drop_table('communities')
    op.drop_table('users')
    op.drop_table('locations')
    op.drop_table('states_provinces')
    op.drop_table('tags')
    op.drop_table('livestock')
    op.drop_table('crops')
    op.drop_table('countries')
    op.drop_table('categories')
    # ### end Alembic commands ###
