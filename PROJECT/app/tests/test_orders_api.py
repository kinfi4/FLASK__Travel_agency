import requests
from datetime import datetime

from app.models import Order
from app.tests.test_clients_api import post_client, delete_client
from app.service.READ_operators import get_orders


BASE = 'http://127.0.0.1:5000/'
DATE_FORMAT = '%Y-%m-%d'


class TestOrdersApi:
    def test_post_a_order(self):
        post_client('unique_pass')
        response = requests.post(BASE + 'json_orders', data={
            "client_pass": "unique_pass",
            "tour_id": 1,
            "days": 10,
            "tour_date": "1920-12-12"
        })

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'unique_pass'
        assert json['tour_id'] == 1
        assert json['tour_date'] == '1920-12-12'

    def test_put_a_order(self):
        order = Order.query.filter(Order.client_pass == 'unique_pass').first()

        response = requests.put(BASE + 'json_orders/' + f'{order.id}', data={
            'tour_date': '1921-12-12'
        })

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'unique_pass'
        assert json['tour_date'] == '1921-12-12'

    def test_get_new_order(self):
        order = Order.query.filter(Order.client_pass == 'unique_pass').first()

        response = requests.get(BASE + 'json_orders/' + f'{order.id}')

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'unique_pass'
        assert json['tour_date'] == '1921-12-12'
        assert json['tour_id'] == 1

    def test_delete_new_order(self):
        order = Order.query.filter(Order.client_pass == 'unique_pass').first()
        response = requests.delete(BASE + 'json_orders/' + f'{order.id}')

        delete_client('unique_pass')
        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'unique_pass'
        assert json['tour_date'] == '1921-12-12'
        assert json['tour_id'] == 1

    def test_get_orders_ordered_by_from_date(self):
        response = list(get_orders({
            'tour_date_from': '2020-12-01',
            'tour_date_by': '2020-12-31'
        }))

        for order in response:
            assert datetime.strptime('2020-12-31', DATE_FORMAT).date() >= order.tour_date >= datetime.strptime(
                '2020-12-01', DATE_FORMAT).date()

    def test_get_orders_ordered_from_date(self):
        response = list(get_orders({
            'tour_date_from': '2020-12-01',
        }))

        for order in response:
            assert order.tour_date >= datetime.strptime('2020-12-01', DATE_FORMAT).date()

    def test_get_orders_ordered_by_date(self):
        response = list(get_orders({
            'tour_date_by': '2020-11-30'
        }))

        for order in response:
            assert datetime.strptime('2020-12-31', DATE_FORMAT).date() >= order.tour_date
