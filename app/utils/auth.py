from functools import wraps
from typing import Optional
from flask import request, g
from app.models.user import User


def get_bearer_token() -> Optional[str]:
    """从 Authorization 头中提取 Bearer 令牌"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]
    return None


def get_current_user() -> Optional[User]:
    """根据请求中的会话令牌获取当前用户"""
    token = get_bearer_token()
    if not token:
        return None
    user = User.query.filter_by(session_token=token).first()
    if user and user.is_session_valid():
        return user
    return None


def login_required(f):
    """装饰器：要求用户已登录，将当前用户注入 g.current_user"""

    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return {'success': False, 'message': '请先登录'}, 401
        g.current_user = user
        return f(*args, **kwargs)

    return decorated
