from gino.ext.starlette import Gino

from server.models.settings import Settings

settings = Settings()

db = Gino(dsn=settings.pg_dsn)


class Currency(db.Model):
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, default="?", nullable=False)
    exchange_code = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Float, nullable=False)
