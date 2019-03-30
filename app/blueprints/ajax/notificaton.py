from flask import jsonify
from flask_login import login_required, current_user

from app.models import Notification
from . import ajax_bp


@ajax_bp.route('/notifications')
@login_required
def notifications():
    notifications = current_user.notifications.filter_by(is_read=False).order_by(Notification.timestamp.desc()).all()
    notifications = [item.content for item in notifications]

    return jsonify(notifications)
