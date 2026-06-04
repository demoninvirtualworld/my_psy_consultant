from flask import Blueprint, jsonify, g
from app.utils.auth import login_required

user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """获取当前登录用户的信息"""
    return jsonify({
        'success': True,
        'data': g.current_user.to_dict(),
    }), 200
