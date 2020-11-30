from flask_restful import Resource, marshal_with
from flask import abort

from app import api, db
from app.models import Client, Order, Tour
from app.rest.constants import resource_order_fields, resource_tour_fields, resource_client_fields, tour_put_args, \
    order_put_args, client_put_args


class GetJsonClient(Resource):
    @marshal_with(resource_client_fields)
    def get(self, passport):
        """
            Method which can be used to get specific client using his passport

            Expects: clients passport
            Modifies: nothing
            Returns: client
        """
        client = Client.query.get(passport)
        if not client:
            abort(404)

        return client

    @marshal_with(resource_client_fields)
    def delete(self, passport):
        client = Client.query.get(passport)
        if not client:
            abort(404)

        db.session.delete(client)
        db.session.commit()

        return client

    @marshal_with(resource_client_fields)
    def put(self, passport):
        client = Client.query.get(passport)
        if not client:
            abort(404)

        args = client_put_args.parse_args()

        first_name = args.get('first_name', None)
        if first_name:
            client.first_name = first_name

        last_name = args.get('last_name', None)
        if last_name:
            client.last_name = last_name

        email = args.get('email', None)
        if email:
            client.email = email

        registration_date = args.get('registration_date', None)
        if registration_date:
            client.registration_date = registration_date

        db.session.commit()

        return client


class GetJsonOrder(Resource):
    @marshal_with(resource_order_fields)
    def get(self, id):
        order = Order.query.get(id)
        if not order:
            abort(404)

        return order

    @marshal_with(resource_tour_fields)
    def delete(self, id):
        order = Order.query.get(id)
        if not order:
            abort(404)

        db.session.delete(order)
        db.session.commit()

        return order

    @marshal_with(resource_order_fields)
    def put(self, id):
        order = Order.query.get(id)
        if not order:
            abort(404)

        args = order_put_args.parse_args()

        tour_id = args.get('tour_id', None)
        if tour_id:
            order.tour_id = tour_id

        client_pass = args.get('client_pass', None)
        if client_pass:
            order.client_pass = client_pass

        tour_date = args.get('tour_date', None)
        if tour_date:
            order.tour_date = tour_date

        days = args.get('days', None)
        if days:
            order.days = days

        db.session.commit()

        return order


class GetJsonTour(Resource):
    @marshal_with(resource_tour_fields)
    def get(self, id):
        tour = Tour.query.get(id)
        if not tour:
            abort(404)

        return tour

    @marshal_with(resource_tour_fields)
    def delete(self, id):
        tour = Tour.query.get(id)
        if not tour:
            abort(404)

        db.session.delete(tour)
        db.session.commit()

        return tour


api.add_resource(GetJsonClient, '/json_clients/<string:passport>')
api.add_resource(GetJsonOrder, '/json_orders/<int:id>')
api.add_resource(GetJsonTour, '/json_tours/<int:id>')
