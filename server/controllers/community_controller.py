from flask import request, jsonify
from datetime import datetime

from server.models.community import Community, CommunityMember, CommunityPost
from server.database import db
from server.utils.auth import token_required

@token_required
def get_communities(current_user):
    """
    Get paginated communities with filters.
    
    Query Parameters:
    - page: int (default=1)
    - per_page: int (default=10)
    - search: string
    - community_type: string
    - country: string
    """
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search')
    community_type = request.args.get('community_type')
    country = request.args.get('country')
    
    # Base query
    query = Community.query
    
    # Apply filters
    if search:
        query = query.filter(
            (Community.name.ilike(f'%{search}%')) | 
            (Community.description.ilike(f'%{search}%'))
        )
    
    if community_type:
        query = query.filter_by(community_type=community_type)
    
    if country:
        query = query.filter_by(location_country=country)
    
    # Paginate results
    communities_page = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Format response
    communities = []
    for community in communities_page.items:
        community_dict = community.to_dict()
        
        # Add member count
        community_dict['member_count'] = CommunityMember.query.filter_by(community_id=community.community_id).count()
        
        # Check if user is a member
        member = CommunityMember.query.filter_by(
            community_id=community.community_id,
            user_id=current_user.user_id
        ).first()
        community_dict['is_member'] = bool(member)
        
        communities.append(community_dict)
    
    return jsonify({
        'communities': communities,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': communities_page.pages,
            'total_items': communities_page.total
        }
    }), 200


@token_required
def create_community(current_user):
    """
    Create a new community.
    
    Request Body:
    {
        "name": "Organic Corn Farmers",
        "description": "A community for organic corn farmers...",
        "community_type": "Crop-Specific",
        "focus_crops": ["Corn", "Wheat"],
        "location_city": "Nairobi",
        "location_country": "Kenya",
        "is_private": false
    }
    """
    data = request.get_json()
    
    # Create community
    community = Community(
        name=data.get('name'),
        description=data.get('description'),
        community_type=data.get('community_type'),
        focus_crops=data.get('focus_crops'),
        location_city=data.get('location_city'),
        location_country=data.get('location_country'),
        is_private=data.get('is_private', False),
        created_by=current_user.user_id
    )
    
    db.session.add(community)
    db.session.flush()  # Get community_id without committing
    
    # Add creator as admin member
    member = CommunityMember(
        community_id=community.community_id,
        user_id=current_user.user_id,
        role='admin',
        status='active'
    )
    
    db.session.add(member)
    db.session.commit()
    
    return jsonify({
        'message': 'Community created successfully',
        'community': community.to_dict()
    }), 201


@token_required
def get_community(current_user, community_id):
    """
    Get a single community with full details.
    """
    community = Community.query.get(community_id)
    
    if not community:
        return jsonify({'message': 'Community not found'}), 404
    
    # Get community data
    community_data = community.to_dict()
    
    # Add member count
    community_data['member_count'] = CommunityMember.query.filter_by(community_id=community_id).count()
    
    # Check if user is a member
    member = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user.user_id
    ).first()
    community_data['is_member'] = bool(member)
    community_data['member_role'] = member.role if member else None
    
    # Get recent posts
    posts = CommunityPost.query.filter_by(community_id=community_id).order_by(CommunityPost.created_at.desc()).limit(5).all()
    community_data['recent_posts'] = [post.to_dict() for post in posts]
    
    return jsonify(community_data), 200


@token_required
def update_community(current_user, community_id):
    """
    Update an existing community.
    
    Request Body:
    {
        "name": "Updated: Organic Corn Farmers",
        "description": "Updated description...",
        ...other fields to update...
    }
    """
    community = Community.query.get(community_id)
    
    if not community:
        return jsonify({'message': 'Community not found'}), 404
    
    # Check if user is admin
    member = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user.user_id,
        role='admin'
    ).first()
    
    if not member and current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    for field in ['name', 'description', 'community_type', 'focus_crops', 
                 'location_city', 'location_country', 'is_private']:
        if field in data:
            setattr(community, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Community updated successfully',
        'community': community.to_dict()
    }), 200


@token_required
def delete_community(current_user, community_id):
    """
    Delete a community.
    """
    community = Community.query.get(community_id)
    
    if not community:
        return jsonify({'message': 'Community not found'}), 404
    
    # Check if user is admin
    member = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user.user_id,
        role='admin'
    ).first()
    
    if not member and current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Delete community members
    CommunityMember.query.filter_by(community_id=community_id).delete()
    
    # Delete community posts
    CommunityPost.query.filter_by(community_id=community_id).delete()
    
    # Delete community
    db.session.delete(community)
    db.session.commit()
    
    return jsonify({'message': 'Community deleted successfully'}), 200


@token_required
def join_community(current_user, community_id):
    """
    Join a community.
    """
    community = Community.query.get(community_id)
    
    if not community:
        return jsonify({'message': 'Community not found'}), 404
    
    # Check if user is already a member
    member = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user.user_id
    ).first()
    
    if member:
        return jsonify({'message': 'Already a member of this community'}), 400
    
    # Determine status based on community privacy
    status = 'pending' if community.is_private else 'active'
    
    # Add user as member
    member = CommunityMember(
        community_id=community_id,
        user_id=current_user.user_id,
        role='member',
        status=status
    )
    
    db.session.add(member)
    db.session.commit()
    
    return jsonify({
        'message': 'Successfully joined community' if status == 'active' else 'Join request submitted',
        'status': status
    }), 200


@token_required
def get_community_posts(current_user, community_id):
    """
    Get posts for a specific community.
    
    Query Parameters:
    - page: int (default=1)
    - per_page: int (default=10)
    """
    # Check if community exists
    community = Community.query.get(community_id)
    
    if not community:
        return jsonify({'message': 'Community not found'}), 404
    
    # Check if user is a member
    member = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user.user_id
    ).first()
    
    if not member and community.is_private:
        return jsonify({'message': 'Not a member of this community'}), 403
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Get posts
    posts_page = CommunityPost.query.filter_by(community_id=community_id).order_by(
        CommunityPost.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Format response
    posts = [post.to_dict() for post in posts_page.items]
    
    return jsonify({
        'posts': posts,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': posts_page.pages,
            'total_items': posts_page.total
        }
    }), 200


@token_required
def create_community_post(current_user, community_id):
    """
    Create a post in a community.
    
    Request Body:
    {
        "content": "Hello everyone! I'm new to organic farming...",
        "image_url": "https://example.com/image.jpg"  # Optional
    }
    """
    # Check if community exists
    community = Community.query.get(community_id)
    
    if not community:
        return jsonify({'message': 'Community not found'}), 404
    
    # Check if user is a member
    member = CommunityMember.query.filter_by(
        community_id=community_id,
        user_id=current_user.user_id,
        status='active'
    ).first()
    
    if not member:
        return jsonify({'message': 'Not an active member of this community'}), 403
    
    data = request.get_json()
    
    # Create post
    post = CommunityPost(
        community_id=community_id,
        user_id=current_user.user_id,
        content=data.get('content'),
        image_url=data.get('image_url')
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({
        'message': 'Post created successfully',
        'post': post.to_dict()
    }), 201