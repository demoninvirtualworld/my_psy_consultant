import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """应用配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'psy-consultant-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 会话令牌有效期（秒），默认 7 天
    SESSION_TOKEN_EXPIRE_SECONDS = 7 * 24 * 3600
