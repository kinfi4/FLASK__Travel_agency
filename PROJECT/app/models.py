from datetime import date
from app import db


class Client(db.Model):
    passport = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(99))
    last_name = db.Column(db.String(99))
    registration_date = db.Column(db.Date, default=date.today())

    @property
    def number_of_orders(self):
        return len(list(Order.query.filter(Order.client_pass == self.passport)))

    def __repr__(self):
        return f'Client: {self.first_name} {self.last_name}'


class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(63))
    hotel = db.Column(db.String(127))
    tour_includes = db.Column(db.String(255))
    day_cost = db.Column(db.Float)

    @property
    def number_of_orders(self):
        return len(Order.query.filter(tour_id=self.id))

    def __repr__(self):
        return f'Tour: {self.name}'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'))
    client_pass = db.Column(db.String(80), db.ForeignKey('client.passport'))
    add_date = db.Column(db.Date, index=True, default=date.today())
    days = db.Column(db.Integer)

    @property
    def tour_day_cost(self):
        return Tour.query.get(self.tour_id).day_cost

    @property
    def total_cost(self):
        return self.tour_day_cost * self.days

    def __repr__(self):
        return f'{self.id}, {self.client_pass}'
