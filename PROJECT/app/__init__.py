import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kinfi4:1415926535@localhost:5432/travel_agency'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


from app import views, models, rest


if __name__ == '__main__':
    open('app.log', 'a').close()
    logging.basicConfig(filename='app.log', level=logging.DEBUG)

    app.run(debug=True)
