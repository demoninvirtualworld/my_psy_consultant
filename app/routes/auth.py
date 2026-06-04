from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': '请提供注册信息'}), 400

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    # 校验用户名
    if not username:
        return jsonify({'success': False, 'message': '用户名不能为空'}), 400
    if len(username) < 2:
        return jsonify({'success': False, 'message': '用户名至少需要2个字符'}), 400
    if len(username) > 80:
        return jsonify({'success': False, 'message': '用户名不能超过80个字符'}), 400

    # 校验密码
    if not password:
        return jsonify({'success': False, 'message': '密码不能为空'}), 400
    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少需要6个字符'}), 400

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': '该用户名已被注册，请更换'}), 409

    # 创建用户
    user = User(username=username, name=username)
    user.set_password(password)

    # 生成会话令牌（注册后自动登录）
    expire_seconds = current_app.config.get('SESSION_TOKEN_EXPIRE_SECONDS', 604800)
    session_token = user.generate_session_token(expire_seconds)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'session_token': session_token,
            'user': user.to_dict(),
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'message': '请提供登录信息'}), 400

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400

    # 查找用户
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    # 校验密码
    if not user.check_password(password):
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    # 生成新的会话令牌
    expire_seconds = current_app.config.get('SESSION_TOKEN_EXPIRE_SECONDS', 604800)
    session_token = user.generate_session_token(expire_seconds)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'session_token': session_token,
            'user': user.to_dict(),
        }
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    data = request.get_json(silent=True) or {}
    session_token = data.get('session_token', '')

    if session_token:
        user = User.query.filter_by(session_token=session_token).first()
        if user:
            user.clear_session()
            db.session.commit()

    return jsonify({'success': True, 'message': '已退出登录'}), 200
