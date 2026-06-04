from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Flask 应用工厂"""
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='../static'
    )
    app.config.from_object('config.Config')

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    from app.routes import register_blueprints
    register_blueprints(app)

    # 创建数据库表
    with app.app_context():
        # 确保导入所有模型，以便 SQLAlchemy 能发现它们
        from app.models import user  # noqa: F401
        db.create_all()

    return app
