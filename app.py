from flask import Flask, render_template
from config import Config
from extensions import db

# Import Blueprints
from routes.auth import auth_bp
from routes.user import user_bp
from routes.company import company_bp
from routes.reports import reports_bp
from routes.ai import ai_bp
from flask import session, request, redirect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(ai_bp)
    
    # Translations setup
    from utils.translations import t
    @app.context_processor
    def inject_translations():
        lang = session.get('lang', 'en')
        return dict(
            lang=lang,
            dir='rtl' if lang == 'ar' else 'ltr',
            t=lambda key: t(key, lang)
        )

    @app.route('/set-language/<lang>')
    def set_language(lang):
        if lang in ['en', 'ar']:
            session['lang'] = lang
        return redirect(request.referrer or '/')

    @app.route('/tutorial')
    def tutorial():
        return render_template('tutorial.html')
    
    @app.route('/')
    def index():
        return render_template('index.html')
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    