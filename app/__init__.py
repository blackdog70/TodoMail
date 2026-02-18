from flask import Flask
from .auth import bp as auth_bp, login_manager
from .routes import bp as main_bp
from .i18n import translate, get_locale, translations

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_i18n():
        return {
            '_': translate,
            'current_lang': get_locale(),
            'languages': translations.keys(),
        }
    return app
