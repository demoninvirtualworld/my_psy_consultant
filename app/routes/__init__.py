from flask import render_template


def register_blueprints(app):
    """注册所有蓝图"""
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # 前端入口：渲染 index.html
    @app.route('/')
    def index():
        return render_template('index.html')
