from app import db
from app.models import Client, Order, Tour


def update_cliente(passport, data):
    client = Client.query.get(passport)
    if client is None:
        return None

    first_name = data.get('first_name', None)
    if first_name:
        client.first_name = first_name

    last_name = data.get('last_name', None)
    if last_name:
        client.last_name = last_name

    email = data.get('email', None)
    if email:
        client.email = email

    registration_date = data.get('registration_date', None)
    if registration_date:
        client.registration_date = registration_date

    db.session.commit()

    return client


def update_order(id_, data):
    order = Order.query.get(id_)
    if order is None:
        return None

    tour_id = data.get('tour_id', None)
    if tour_id:
        order.tour_id = tour_id

    client_pass = data.get('client_pass', None)
    if client_pass:
        order.client_pass = client_pass

    tour_date = data.get('tour_date', None)
    if tour_date:
        order.tour_date = tour_date

    days = data.get('days', None)
    if days:
        order.days = days

    db.session.commit()

    return order


def update_tour(id_, data):
    tour = Tour.query.get(id_)
    if not tour:
        return None

    name = data.get('name', None)
    if name:
        tour.name = name

    country = data.get('country', None)
    if country:
        tour.country = country

    hotel = data.get('hotel', None)
    if hotel:
        tour.hotel = hotel

    tour_includes = data.get('tour_includes', None)
    if tour_includes:
        tour.tour_includes = tour_includes

    day_cost = data.get('day_cost', None)
    if day_cost:
        tour.day_cost = day_cost

    db.session.commit()

    return tour
