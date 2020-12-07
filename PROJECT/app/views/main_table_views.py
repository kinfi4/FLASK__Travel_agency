from datetime import date, timedelta

import requests
from flask import render_template, request
from flask.views import MethodView

from app import app
from app.models import Client, Order, Tour
from app.tests.test_clients_api import BASE


# Get All Entities
class GetAllOrdersView(MethodView):
    def get(self):
        return render_template('tables/orders.html', **self.prepare_context(request.args))

    @staticmethod
    def prepare_context(filters=None):
        title = 'Orders'
        add_button = 'add_order'

        if not filters:
            data = requests.get(BASE + 'json_orders')
        else:
            data = requests.get(BASE + 'json_orders' + '?' + request.url.split('?')[-1])

        return {
            'title': title,
            'add_button': add_button,
            'orders': data.json(),
            'sort_from': filters.get('tour_date_from', None),
            'sort_by': filters.get('tour_date_by', None)
        }


class GetAllClientsView(MethodView):
    def get(self):
        return render_template('tables/clients.html', **self.prepare_context(request.args))

    def prepare_context(self, filters=None):
        title = 'Clients'
        add_button = 'add_client'

        if not filters:
            data = requests.get(BASE + 'json_clients')
        else:
            data = requests.get(BASE + 'json_clients' + '?' + request.url.split('?')[-1])

        return {
            'title': title,
            'add_button': add_button,
            'clients': data.json(),
            'sort_by': self.get_sorting_for_html(filters.get('sort-input', None)),
            'desc': filters.get('desc', False)
        }

    @staticmethod
    def get_sorting_for_html(sorting):
        if sorting == 'first_name':
            sort_list_variants = [
                ('First name', 'first_name'),
                ('Last name', 'last_name'),
                ('Number of orders', 'num_orders')
            ]
        elif sorting == 'last_name':
            sort_list_variants = [
                ('Last name', 'last_name'),
                ('First name', 'first_name'),
                ('Number of orders', 'num_orders')
            ]
        else:
            sort_list_variants = [
                ('Number of orders', 'num_orders'),
                ('Last name', 'last_name'),
                ('First name', 'first_name')
            ]

        return sort_list_variants


class GetAllToursView(MethodView):
    def get(self):
        return render_template('tables/tours.html', **self.prepare_context(request.args))

    @staticmethod
    def prepare_context(filters=None):
        title = 'Tours'
        add_button = 'add_tour'

        if not filters:
            data = requests.get(BASE + 'json_tours')
        else:
            data = requests.get(BASE + 'json_tours' + '?' + request.url.split('?')[-1])

        return {
            'title': title,
            'add_button': add_button,
            'tours': data.json(),
            'from_price': filters.get('from_price', None),
            'by_price': filters.get('by_price', None)
        }
# End Get All Entities


app.add_url_rule('/orders', view_func=GetAllOrdersView.as_view('get_all_orders'), methods=['GET', 'POST'])
app.add_url_rule('/clients', view_func=GetAllClientsView.as_view('get_all_clients'), methods=['GET', 'POST'])
app.add_url_rule('/tours', view_func=GetAllToursView.as_view('get_all_tours'), methods=['GET', 'POST'])
