from datetime import date, timedelta

from flask_restful import Resource, marshal_with
from flask import request

from app import api, db
from app.models import Client, Order, Tour
from app.rest.constants import resource_order_fields, resource_tour_fields, resource_client_fields, tour_put_args, \
    order_put_args, client_put_args


class GetJsonClients(Resource):
    @marshal_with(resource_client_fields)
    def get(self):
        """
            Expects: nothing
            Modifies: nothing
            Returns: a query list of all the clients
        """
        return self.prepare_context(request.args)

    def prepare_context(self, filters=None):
        return list(self.filter_clients(filters))

    @staticmethod
    def filter_clients(filters):
        if filters:
            sort_by = filters.get('sort-input', False)
            desc = filters.get('desc', False)

            if sort_by == 'first_name':
                if desc:
                    clients = list(Client.query.order_by(Client.first_name))
                    clients.reverse()
                else:
                    clients = Client.query.order_by(Client.first_name)
            elif sort_by == 'last_name':
                if desc:
                    clients = list(Client.query.order_by(Client.last_name))
                    clients.reverse()
                else:
                    clients = Client.query.order_by(Client.last_name)
            elif sort_by == 'num_orders':
                if desc:
                    clients = list(Client.query.all())
                    clients.sort(key=lambda c: c.number_of_orders, reverse=True)
                else:
                    clients = list(Client.query.all())
                    clients.sort(key=lambda c: c.number_of_orders)
            else:
                clients = Client.query.all()
        else:
            clients = Client.query.all()

        return clients

    @marshal_with(resource_client_fields)
    def post(self):
        """
            Method which can be used to add new client to the database

            Expects: nothing
            Modifies: nothing
            Returns: created client
        """
        args = client_put_args.parse_args()

        client = Client()
        client.passport = args.get('passport', None)
        client.first_name = args.get('first_name', None)
        client.last_name = args.get('last_name', None)
        client.email = args.get('email', None)
        client.registration_date = args.get('registration_date', None)

        db.session.add(client)
        db.session.commit()

        return client


class GetJsonOrders(Resource):
    @marshal_with(resource_order_fields)
    def get(self):
        """
            Expects: nothing
            Modifies: nothing
            Returns: query list of all the orders in database
        """
        return self.prepare_context(request.args)

    def prepare_context(self, filters=None):

        return list(self.filter_orders(filters))

    @staticmethod
    def filter_orders(filters):
        if filters:
            s_from_date = filters.get('tour_date_from', None)
            s_by_date = filters.get('tour_date_by', None)

            if s_from_date and s_by_date:
                from_date = date.fromisoformat(s_from_date)
                by_date = date.fromisoformat(s_by_date)

                by_date += timedelta(days=1)
                from_date -= timedelta(days=1)

                print(from_date, by_date)
                orders = Order.query.filter(Order.tour_date > from_date).filter(by_date > Order.tour_date)
            elif s_from_date:
                from_date = date.fromisoformat(s_from_date)
                from_date -= timedelta(days=1)

                orders = Order.query.filter(Order.tour_date >= from_date)
            elif s_by_date:
                by_date = date.fromisoformat(s_by_date)
                by_date += timedelta(days=1)

                orders = Order.query.filter(by_date >= Order.tour_date)
            else:
                orders = Order.query.all()
        else:
            orders = Order.query.all()

        return orders

    @marshal_with(resource_order_fields)
    def post(self):
        """
            Method which can be used to add new order to the database

            Expects: nothing
            Modifies: nothing
            Returns: created order
        """
        args = order_put_args.parse_args()

        order = Order()
        order.client_pass = args.get('client_pass', None)
        order.tour_id = args.get('tour_id', None)
        order.days = args.get('days', None)
        order.tour_date = args.get('tour_date', None)

        db.session.add(order)
        db.session.commit()

        return order


class GetJsonTours(Resource):
    @marshal_with(resource_tour_fields)
    def get(self):
        """
            Expects: nothing
            Modifies: nothing
            Returns: a query list of all the tours in database
        """
        return self.prepare_context(request.args)

    def prepare_context(self, filters=None):

        return list(self.filter_tours(filters))

    @staticmethod
    def filter_tours(filters):
        if filters:
            str_from_price = filters.get('from_price', None)
            str_by_price = filters.get('by_price', None)

            if not str_by_price:
                str_by_price = 10e10

            if not str_from_price:
                str_from_price = '0'

            from_price = float(str_from_price) - 1
            by_price = float(str_by_price) + 1

            if from_price and by_price:
                tours = Tour.query.filter(Tour.day_cost > int(from_price)).filter(by_price > Tour.day_cost)
            elif from_price:
                tours = Tour.query.filter(Tour.day_cost >= from_price)
            elif by_price:
                tours = Tour.query.filter(by_price >= Tour.day_cost)
            else:
                tours = Tour.query.all()
        else:
            tours = Tour.query.all()

        return tours

    @marshal_with(resource_tour_fields)
    def post(self):
        """
            Method which can be used to add new tour to the database

            Expects: nothing
            Modifies: nothing
            Returns: created tour
        """
        args = tour_put_args.parse_args()

        tour = Tour()
        tour.name = args.get('name', None)
        tour.country = args.get('country', None)
        tour.hotel = args.get('hotel', None)
        tour.tour_includes = args.get('tour_includes', None)
        tour.day_cost = args.get('day_cost', None)

        db.session.add(tour)
        db.session.commit()

        return tour


api.add_resource(GetJsonClients, '/json_clients')
api.add_resource(GetJsonOrders, '/json_orders')
api.add_resource(GetJsonTours, '/json_tours')
