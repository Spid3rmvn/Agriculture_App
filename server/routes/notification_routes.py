"""
Notification management API routes.
Handles notification retrieval, preferences, and history.
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from sqlalchemy import desc, and_, or_
from sqlalchemy.orm import joinedload

from server.database import db
from server.models.notifications import Notification, NotificationPreferences, NotificationDelivery
from server.models.user import User
from server.services.notification_service import notification_service
from server.utils.auth import token_required
from server.utils.validators import validate_json_data
from server.utils.error_handlers import create_error_response, create_success_response

# Create blueprint
notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')


@notification_bp.route('', methods=['GET'])
@token_required
def get_notifications(current_user):
    """
    Get notifications for the current user.
    Query parameters:
    - limit: Number of notifications to return (default: 20, max: 100)
    - offset: Number of notifications to skip (default: 0)
    - status: Filter by status (pending, sent, failed, read)
    - type: Filter by notification type
    - unread_only: Return only unread notifications (true/false)
    """
    try:
        # Parse query parameters
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        status_filter = request.args.get('status')
        type_filter = request.args.get('type')
        unread_only = request.args.get('unread_only', '').lower() == 'true'
        
        # Build query
        query = Notification.query.filter_by(user_id=current_user.user_id)
        
        # Apply filters
        if status_filter:
            query = query.filter(Notification.status == status_filter)
        
        if type_filter:
            query = query.filter(Notification.type == type_filter)
        
        if unread_only:
            query = query.filter(Notification.read_at.is_(None))
        
        # Apply pagination and ordering
        notifications = query.order_by(desc(Notification.created_at))\
                            .offset(offset)\
                            .limit(limit)\
                            .all()
        
        # Get total count for pagination
        total_count = query.count()
        
        # Get unread count
        unread_count = Notification.query.filter(
            and_(
                Notification.user_id == current_user.user_id,
                Notification.read_at.is_(None)
            )
        ).count()
        
        return jsonify({
            'notifications': [notification.to_dict() for notification in notifications],
            'total_count': total_count,
            'unread_count': unread_count,
            'has_more': offset + limit < total_count
        }), 200
        
    except ValueError as e:
        return create_error_response('INVALID_PARAMS', f'Invalid query parameters: {str(e)}', status_code=400)
    except Exception as e:
        current_app.logger.error(f"Error fetching notifications: {str(e)}")
        return create_error_response('FETCH_NOTIFICATIONS_FAILED', f'Failed to fetch notifications: {str(e)}', status_code=500)


@notification_bp.route('/<notification_id>/read', methods=['POST'])
@token_required
def mark_notification_read(current_user, notification_id):
    """Mark a specific notification as read."""
    try:
        notification = Notification.query.filter_by(
            notification_id=notification_id,
            user_id=current_user.user_id
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        if not notification.read_at:
            notification.read_at = datetime.utcnow()
            notification.status = 'read'
            db.session.commit()
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error marking notification as read: {str(e)}")
        db.session.rollback()
        return create_error_response('MARK_READ_FAILED', f'Failed to mark notification as read: {str(e)}', status_code=500)


@notification_bp.route('/mark-read', methods=['POST'])
@token_required
def mark_notifications_read(current_user):
    """Mark multiple notifications as read."""
    try:
        data = request.get_json()
        if not data or 'notification_ids' not in data:
            return create_error_response('MISSING_NOTIFICATION_IDS', 'notification_ids array is required', status_code=400)
        
        notification_ids = data['notification_ids']
        if not isinstance(notification_ids, list):
            return create_error_response('INVALID_NOTIFICATION_IDS', 'notification_ids must be an array', status_code=400)
        
        # Update notifications
        updated_count = Notification.query.filter(
            and_(
                Notification.notification_id.in_(notification_ids),
                Notification.user_id == current_user.user_id,
                Notification.read_at.is_(None)
            )
        ).update({
            'read_at': datetime.utcnow(),
            'status': 'read'
        }, synchronize_session=False)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Marked {updated_count} notifications as read',
            'updated_count': updated_count
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error marking notifications as read: {str(e)}")
        db.session.rollback()
        return create_error_response('MARK_READ_FAILED', f'Failed to mark notifications as read: {str(e)}', status_code=500)


@notification_bp.route('/mark-all-read', methods=['POST'])
@token_required
def mark_all_notifications_read(current_user):
    """Mark all notifications as read for the current user."""
    try:
        # Update all unread notifications
        updated_count = Notification.query.filter(
            and_(
                Notification.user_id == current_user.user_id,
                Notification.read_at.is_(None)
            )
        ).update({
            'read_at': datetime.utcnow(),
            'status': 'read'
        })
        
        db.session.commit()
        
        return jsonify({
            'message': f'Marked {updated_count} notifications as read',
            'updated_count': updated_count
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error marking all notifications as read: {str(e)}")
        db.session.rollback()
        return create_error_response('MARK_ALL_READ_FAILED', f'Failed to mark all notifications as read: {str(e)}', status_code=500)


@notification_bp.route('/preferences', methods=['GET'])
@token_required
def get_notification_preferences(current_user):
    """Get notification preferences for the current user."""
    try:
        preferences = notification_service.get_user_preferences(str(current_user.user_id))
        return create_success_response(data=preferences.to_dict())
        
    except Exception as e:
        current_app.logger.error(f"Error fetching notification preferences: {str(e)}")
        return create_error_response('FETCH_PREFERENCES_FAILED', f'Failed to fetch preferences: {str(e)}', status_code=500)


@notification_bp.route('/preferences', methods=['PUT'])
@token_required
def update_notification_preferences(current_user):
    """Update notification preferences for the current user."""
    try:
        data = request.get_json()
        if not data:
            return create_error_response('NO_DATA', 'No data provided', status_code=400)
        
        # Validate preference data
        valid_fields = {
            'email_notifications', 'push_notifications', 'sms_notifications',
            'in_app_notifications', 'notification_types', 'quiet_hours_start',
            'quiet_hours_end', 'timezone'
        }
        
        # Filter out invalid fields
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        if not filtered_data:
            return create_error_response('NO_VALID_FIELDS', 'No valid preference fields provided', status_code=400)
        
        # Update preferences
        preferences = notification_service.update_user_preferences(
            str(current_user.user_id), 
            filtered_data
        )
        
        return create_success_response(
            data={'preferences': preferences.to_dict()},
            message='Notification preferences updated successfully'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error updating notification preferences: {str(e)}")
        db.session.rollback()
        return create_error_response('UPDATE_PREFERENCES_FAILED', f'Failed to update preferences: {str(e)}', status_code=500)


@notification_bp.route('/history', methods=['GET'])
@token_required
def get_notification_history(current_user):
    """
    Get detailed notification history with delivery information.
    Query parameters:
    - days: Number of days to look back (default: 30, max: 90)
    - channel: Filter by delivery channel
    - status: Filter by delivery status
    """
    try:
        # Parse query parameters
        days = min(int(request.args.get('days', 30)), 90)
        channel_filter = request.args.get('channel')
        status_filter = request.args.get('status')
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query with joins
        query = db.session.query(Notification)\
                          .options(joinedload(Notification.deliveries))\
                          .filter(
                              and_(
                                  Notification.user_id == current_user.user_id,
                                  Notification.created_at > cutoff_date
                              )
                          )
        
        notifications = query.order_by(desc(Notification.created_at)).all()
        
        # Filter deliveries if needed
        history = []
        for notification in notifications:
            notification_dict = notification.to_dict()
            
            # Add delivery information
            deliveries = []
            for delivery in notification.deliveries:
                if channel_filter and delivery.channel != channel_filter:
                    continue
                if status_filter and delivery.status != status_filter:
                    continue
                deliveries.append(delivery.to_dict())
            
            if not channel_filter and not status_filter:
                # Include all deliveries if no filters
                deliveries = [d.to_dict() for d in notification.deliveries]
            
            notification_dict['deliveries'] = deliveries
            history.append(notification_dict)
        
        return jsonify({
            'history': history,
            'period_days': days,
            'total_notifications': len(history)
        }), 200
        
    except ValueError as e:
        return create_error_response('INVALID_PARAMS', f'Invalid query parameters: {str(e)}', status_code=400)
    except Exception as e:
        current_app.logger.error(f"Error fetching notification history: {str(e)}")
        return create_error_response('FETCH_HISTORY_FAILED', f'Failed to fetch notification history: {str(e)}', status_code=500)


@notification_bp.route('/analytics', methods=['GET'])
@token_required
def get_notification_analytics(current_user):
    """Get notification analytics for the current user."""
    try:
        days = min(int(request.args.get('days', 30)), 90)
        
        analytics = notification_service.get_notification_analytics(
            user_id=str(current_user.user_id),
            days=days
        )
        
        return create_success_response(
            data={'analytics': analytics, 'period_days': days}
        )
        
    except ValueError as e:
        return create_error_response('INVALID_PARAMS', f'Invalid query parameters: {str(e)}', status_code=400)
    except Exception as e:
        current_app.logger.error(f"Error fetching notification analytics: {str(e)}")
        return create_error_response('ANALYTICS_FAILED', f'Failed to fetch analytics: {str(e)}', status_code=500)


@notification_bp.route('/types', methods=['GET'])
@token_required
def get_notification_types(current_user):
    """Get available notification types for preference configuration."""
    try:
        # Define available notification types
        notification_types = {
            'payment_confirmation': {
                'name': 'Payment Confirmations',
                'description': 'Notifications about payment status and confirmations',
                'default_enabled': True
            },
            'consultation_booked': {
                'name': 'Consultation Bookings',
                'description': 'Notifications when consultations are booked or cancelled',
                'default_enabled': True
            },
            'expert_response': {
                'name': 'Expert Responses',
                'description': 'Notifications when experts respond to your questions',
                'default_enabled': True
            },
            'new_comment': {
                'name': 'New Comments',
                'description': 'Notifications when someone comments on your posts',
                'default_enabled': True
            },
            'new_follower': {
                'name': 'New Followers',
                'description': 'Notifications when someone follows you',
                'default_enabled': True
            },
            'community_activity': {
                'name': 'Community Activity',
                'description': 'Notifications about activity in your communities',
                'default_enabled': False
            },
            'system_updates': {
                'name': 'System Updates',
                'description': 'Important system announcements and updates',
                'default_enabled': True
            },
            'marketing': {
                'name': 'Marketing & Promotions',
                'description': 'Promotional content and marketing messages',
                'default_enabled': False
            }
        }
        
        return create_success_response(data={'notification_types': notification_types})
        
    except Exception as e:
        current_app.logger.error(f"Error fetching notification types: {str(e)}")
        return create_error_response('FETCH_TYPES_FAILED', f'Failed to fetch notification types: {str(e)}', status_code=500)


@notification_bp.route('/test', methods=['POST'])
@token_required
def send_test_notification(current_user):
    """Send a test notification to the current user (for testing purposes)."""
    try:
        data = request.get_json() or {}
        
        # Create test notification
        test_notification = Notification(
            user_id=current_user.user_id,
            type='system_test',
            title=data.get('title', 'Test Notification'),
            message=data.get('message', 'This is a test notification to verify your notification settings.'),
            channels=data.get('channels', ['in_app', 'push']),
            priority='normal'
        )
        
        db.session.add(test_notification)
        db.session.commit()
        
        # Send the notification
        import asyncio
        results = asyncio.run(notification_service.send_notification(test_notification))
        
        return create_success_response(
            data={
                'notification': test_notification.to_dict(),
                'delivery_results': [
                    {
                        'channel': r.channel,
                        'success': r.success,
                        'message': r.message
                    } for r in results
                ]
            },
            message='Test notification sent'
        )
        
    except Exception as e:
        current_app.logger.error(f"Error sending test notification: {str(e)}")
        db.session.rollback()
        return create_error_response('TEST_NOTIFICATION_FAILED', f'Failed to send test notification: {str(e)}', status_code=500)


# Error handlers for the blueprint
@notification_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Notification not found'}), 404


@notification_bp.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Access denied'}), 403


@notification_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500