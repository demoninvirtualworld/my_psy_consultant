import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(80), default='')
    age = db.Column(db.String(10), default='')
    gender = db.Column(db.String(10), default='')  # male / female / other
    session_token = db.Column(db.String(128), unique=True, nullable=True)
    session_token_expires = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password: str):
        """设置密码（存储哈希值）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """校验密码"""
        return check_password_hash(self.password_hash, password)

    def generate_session_token(self, expire_seconds: int = 604800) -> str:
        """
        生成会话令牌
        :param expire_seconds: 过期秒数，默认 7 天
        :return: 令牌字符串
        """
        self.session_token = secrets.token_urlsafe(48)
        self.session_token_expires = datetime.utcnow() + timedelta(seconds=expire_seconds)
        return self.session_token

    def is_session_valid(self) -> bool:
        """检查当前会话令牌是否有效"""
        if not self.session_token or not self.session_token_expires:
            return False
        return datetime.utcnow() < self.session_token_expires

    def clear_session(self):
        """清除会话令牌"""
        self.session_token = None
        self.session_token_expires = None

    def to_dict(self) -> dict:
        """返回用户信息的字典表示（不含敏感字段）"""
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name or self.username,
            'age': self.age,
            'gender': self.gender,
        }

    def __repr__(self):
        return f'<User {self.username}>'
