from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from routes import routes_blueprint
from extensions import db  # Import db from extensions

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # Initialize the app with db
migrate = Migrate(app, db)
CORS(app)

app.register_blueprint(routes_blueprint)

if __name__ == '__main__':
    app.run(port=5555, debug=True)