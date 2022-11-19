from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
app.config["IMAGE_UPLOADS"] = r'F:\DATA_KHOA_LUAN\sharedocu.vn\app\static\images\products' # thay doi duong dan anh o day
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app import routes, models
