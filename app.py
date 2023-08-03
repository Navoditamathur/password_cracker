from flask import Flask, render_template,  session
from flask_session import Session
from views import views
from auth import auth
from datetime import timedelta

app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = "INFSCI2150_crackpassword"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=50)

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')


"""Run App"""
if __name__ == "__main__":
    app.run(debug=True)

