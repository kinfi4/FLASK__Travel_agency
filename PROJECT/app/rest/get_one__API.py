from flask_restful import Resource, marshal_with
from flask import abort

from app import api, db
from app.models import Client, Order, Tour
from app.rest.constants import resource_order_fields, resource_tour_fields, resource_client_fields, tour_put_args, \
    order_put_args, client_put_args
from app.service.UPDATE_operators import update_cliente, update_order, update_tour
from app.service.DELETE_operators import delete_client, delete_order, delete_tour


class GetJsonClient(Resource):
    @marshal_with(resource_client_fields)
    def get(self, passport):
        """
            Method which can be used to get specific client using his passport

            Expects: clients passport : str
            Modifies: nothing
            Returns: client
        """
        client = Client.query.get(passport)
        if not client:
            abort(404)

        return client

    @marshal_with(resource_client_fields)
    def delete(self, passport):
        """
            Method which can be used to delete specific client using his passport

            Expects: clients passport : str
            Modifies: nothing
            Returns: client
        """
        client = delete_client(passport)
        if not client:
            abort(404)

        return client

    @marshal_with(resource_client_fields)
    def put(self, passport):
        """
            Method which can be used to edit specific client using his passport

            Expects: clients passport : str
            Modifies: nothing
            Returns: client
        """
        data = client_put_args.parse_args()
        client = update_cliente(passport, data)

        if not client:
            abort(404)

        return client


class GetJsonOrder(Resource):
    @marshal_with(resource_order_fields)
    def get(self, id):
        """
            Method which can be used to get specific order using his id

            Expects: order id : int
            Modifies: nothing
            Returns: order
        """

        order = Order.query.get(id)
        if not order:
            abort(404)

        return order

    @marshal_with(resource_order_fields)
    def delete(self, id):
        """
            Method which can be used to delete specific order using his id

            Expects: order id : int
            Modifies: order with specified id
            Returns: deleted order
        """

        order = delete_order(id)
        if not order:
            abort(404)

        return order

    @marshal_with(resource_order_fields)
    def put(self, id):
        """
            Method which can be used to edit specific order using his id

            Expects: order id : int
            Modifies: order with specified id
            Returns: edited order
        """

        order = update_order(id, order_put_args.parse_args())
        if not order:
            abort(404)

        return order


class GetJsonTour(Resource):
    @marshal_with(resource_tour_fields)
    def get(self, id):
        """
            Method which can be used to get specific tour using his id

            Expects: tour id : int
            Modifies: nothing
            Returns: order
        """

        tour = Tour.query.get(id)
        if not tour:
            abort(404)

        return tour

    @marshal_with(resource_tour_fields)
    def delete(self, id):
        """
            Method which can be used to delete specific tour using his id

            Expects: tour id : int
            Modifies: tour with specified id
            Returns: deleted tour
        """
        tour = delete_tour(id)
        if not tour:
            abort(404)

        return tour

    @marshal_with(resource_tour_fields)
    def put(self, id):
        """
            Method which can be used to edit specific tour using his id

            Expects: tour id : int
            Modifies: tour with specified id
            Returns: edited tour
        """

        tour = update_tour(id, tour_put_args.parse_args())
        if not tour:
            abort(404)

        return tour


api.add_resource(GetJsonClient, '/json_clients/<string:passport>')
api.add_resource(GetJsonOrder, '/json_orders/<int:id>')
api.add_resource(GetJsonTour, '/json_tours/<int:id>')
