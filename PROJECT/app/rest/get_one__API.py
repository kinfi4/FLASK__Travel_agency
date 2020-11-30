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

        client = Client.query.get(passport)
        if not client:
            abort(404)

        db.session.delete(client)
        db.session.commit()

        return client

    @marshal_with(resource_client_fields)
    def put(self, passport):
        """
            Method which can be used to edit specific client using his passport

            Expects: clients passport : str
            Modifies: nothing
            Returns: client
        """

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

    @marshal_with(resource_tour_fields)
    def delete(self, id):
        """
            Method which can be used to delete specific order using his id

            Expects: order id : int
            Modifies: order with specified id
            Returns: deleted order
        """

        order = Order.query.get(id)
        if not order:
            abort(404)

        db.session.delete(order)
        db.session.commit()

        return order

    @marshal_with(resource_order_fields)
    def put(self, id):
        """
            Method which can be used to edit specific order using his id

            Expects: order id : int
            Modifies: order with specified id
            Returns: edited order
        """

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

        tour = Tour.query.get(id)
        if not tour:
            abort(404)

        db.session.delete(tour)
        db.session.commit()

        return tour

    @marshal_with(resource_tour_fields)
    def put(self, id):
        """
            Method which can be used to edit specific tour using his id

            Expects: tour id : int
            Modifies: tour with specified id
            Returns: edited tour
        """

        tour = Tour.query.get(id)
        if not tour:
            abort(404)

        args = tour_put_args.parse_args()

        name = args.get('name', None)
        if name:
            tour.name = name

        country = args.get('country', None)
        if country:
            tour.country = country

        hotel = args.get('hotel', None)
        if hotel:
            tour.hotel = hotel

        tour_includes = args.get('tour_includes', None)
        if tour_includes:
            tour.tour_includes = tour_includes

        day_cost = args.get('day_cost', None)
        if day_cost:
            tour.day_cost = day_cost

        db.session.commit()

        return tour


api.add_resource(GetJsonClient, '/json_clients/<string:passport>')
api.add_resource(GetJsonOrder, '/json_orders/<int:id>')
api.add_resource(GetJsonTour, '/json_tours/<int:id>')
