from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kinfi4:1415926535@localhost:5432/travel_agency'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models


if __name__ == '__main__':
    app.run(debug=True)
