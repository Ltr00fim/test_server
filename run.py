from app import create_app
from config import Config
from setup_db import db

app = create_app(Config)

with app.app_context():
    db.create_all()
