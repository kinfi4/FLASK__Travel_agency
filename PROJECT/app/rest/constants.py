from datetime import datetime
from flask_restful import fields, reqparse

client_put_args = reqparse.RequestParser()
client_put_args.add_argument('passport', type=str, help='Passport of the client')
client_put_args.add_argument('first_name', type=str, help='First client`s name')
client_put_args.add_argument('last_name', type=str, help='Last client`s name')
client_put_args.add_argument('email', type=str, help='Client`s email')
client_put_args.add_argument('registration_date', type=str, help='Client`s registration date')

order_put_args = reqparse.RequestParser()
order_put_args.add_argument('tour_id', type=int)
order_put_args.add_argument('client_pass', type=str)
order_put_args.add_argument('tour_date', type=str)
order_put_args.add_argument('days', type=int)

tour_put_args = reqparse.RequestParser()
tour_put_args.add_argument('name', type=str)
tour_put_args.add_argument('country', type=str)
tour_put_args.add_argument('hotel', type=str)
tour_put_args.add_argument('tour_includes', type=str)
tour_put_args.add_argument('day_cost', type=float)


resource_client_fields = {
    'passport': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'registration_date': fields.String
}

resource_order_fields = {
    'id': fields.Integer,
    'tour_id': fields.Integer,
    'client_pass': fields.String,
    'tour_date': fields.String,
    'days': fields.Integer
}

resource_tour_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'country': fields.String,
    'hotel': fields.String,
    'tour_includes': fields.String,
    'day_cost': fields.Float
}
