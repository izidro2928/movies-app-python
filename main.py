from flask import Flask
from movies.movies import movies
from users.users import users
import secrets

app = Flask(__name__)
secret = secrets.token_urlsafe(32)

app.secret_key = secret
app.register_blueprint(movies)
app.register_blueprint(users, url_prefix='/users')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
