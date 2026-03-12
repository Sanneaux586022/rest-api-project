import os 
import redis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

r = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))

