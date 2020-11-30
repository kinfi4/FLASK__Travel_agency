from flask_restful import Resource, marshal_with

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

        return Client.query.all()

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
        return Order.query.all()

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
        return Tour.query.all()

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
