import requests

from app.models import Order


BASE = 'http://127.0.0.1:5000/'


class TestOrdersApi:
    def test_post_a_order(self):
        response = requests.post(BASE + 'json_orders', data={
            'client_pass': 'TestPass',
            'tour_id': 1,
            'days': 10,
            'tour_date': '1920-12-12'
        })

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'TestPass'
        assert json['tour_id'] == 1
        assert json['tour_date'] == '1920-12-12'

    def test_put_a_order(self):
        order = Order.query.filter('client_pass' == 'TestPass' and 'tour_id' == 1 and 'tour_date' == '1920-12-12').first()

        response = requests.put(BASE + 'json_orders/' + f'{order.id}', data={
            'tour_date': '1921-12-12'
        })

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'TestPass'
        assert json['tour_date'] == '1921-12-12'

    def test_get_new_order(self):
        order = Order.query.filter('client_pass' == 'TestPass' and 'tour_id' == 1 and 'tour_date' == '1920-12-12').first()

        response = requests.get(BASE + 'json_orders/' + f'{order.id}')

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'TestPass'
        assert json['tour_date'] == '1921-12-12'
        assert json['tour_id'] == 1

    def test_delete_new_order(self):
        order = Order.query.filter('client_pass' == 'TestPass' and 'tour_id' == 1 and 'tour_date' == '1920-12-12').first()

        response = requests.delete(BASE + 'json_orders/' + f'{order.id}')

        json = response.json()

        assert response.status_code == 200
        assert json['client_pass'] == 'TestPass'
        assert json['tour_date'] == '1921-12-01'
        assert json['tour_id'] == 1

    def test_get_orders_ordered_by_from_date(self):
        response = requests.get(BASE + 'json_orders' + '?tour_date_from=2020-12-01&tour_date_by=2020-12-31')
        json = response.json()

        assert response.status_code == 200
        for order in json:
            assert '2020-12-31' >= order['tour_date'] >= '2020-12-01'
