from datetime import date, timedelta

from flask_restful import Resource, marshal_with
from flask import request

from app import api, db
from app.models import Client, Order, Tour
from app.rest.constants import resource_order_fields, resource_tour_fields, resource_client_fields, tour_put_args, \
    order_put_args, client_put_args
from app.service.CREATE_operators import add_object_to_db
from app.service.READ_operators import get_clients, get_tours, get_orders


class GetJsonClients(Resource):
    @marshal_with(resource_client_fields)
    def get(self):
        """
            Expects: nothing
            Modifies: nothing
            Returns: a query list of all the clients
        """
        return get_clients(request.args)

    @marshal_with(resource_client_fields)
    def post(self):
        """
            Method which can be used to add new client to the database

            Expects: nothing
            Modifies: nothing
            Returns: created client
        """
        args = client_put_args.parse_args()
        client = add_object_to_db(Client, **args)

        return client


class GetJsonOrders(Resource):
    @marshal_with(resource_order_fields)
    def get(self):
        """
            Expects: nothing
            Modifies: nothing
            Returns: query list of all the orders in database
        """
        return get_orders(request.args)

    @marshal_with(resource_order_fields)
    def post(self):
        """
            Method which can be used to add new order to the database

            Expects: nothing
            Modifies: nothing
            Returns: created order
        """
        args = order_put_args.parse_args()
        order = add_object_to_db(Order, **args)

        return order


class GetJsonTours(Resource):
    @marshal_with(resource_tour_fields)
    def get(self):
        """
            Expects: nothing
            Modifies: nothing
            Returns: a query list of all the tours in database
        """
        return get_tours(request.args)

    @marshal_with(resource_tour_fields)
    def post(self):
        """
            Method which can be used to add new tour to the database

            Expects: nothing
            Modifies: nothing
            Returns: created tour
        """
        args = tour_put_args.parse_args()
        tour = add_object_to_db(Tour, **args)

        return tour


api.add_resource(GetJsonClients, '/json_clients')
api.add_resource(GetJsonOrders, '/json_orders')
api.add_resource(GetJsonTours, '/json_tours')
