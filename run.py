from flask import Flask, render_template, session

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your-secret-key-here'

# Регистрация блюпринтов
from app.data.routes import data
app.register_blueprint(data, url_prefix='/monitoring')

from app.auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def main():
    if session.get('user_id'):
        return render_template("main_authenticated.html")
    return render_template("main_guest.html")

@app.route('/away')
def away():
    return render_template("away.html")



if __name__ == '__main__':
    app.run(debug=True)