from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(100), nullable=False)
    n_min = db.Column(db.Integer, nullable=False)
    n_max = db.Column(db.Integer, nullable=False)
    step = db.Column(db.Integer, nullable=False)
    input_sizes = db.Column(db.Text, nullable=False)
    times = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)