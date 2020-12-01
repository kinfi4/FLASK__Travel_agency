import requests

BASE = 'http://127.0.0.1:5000/'


class TestOrdersApi:
    def test_post_a_order(self):
        response = requests.post(BASE + 'json_orders', data={

        })

        json = response.json()

        assert response.status_code == 200

    def test_put_a_order(self):
        response = requests.put(BASE + 'json_orders/' + 'TestPassport', data={
        })

        json = response.json()

        assert response.status_code == 200

    def test_get_new_order(self):
        response = requests.get(BASE + 'json_orders/' + 'TestPassport')

        json = response.json()

        assert response.status_code == 200

    def test_delete_new_order(self):
        response = requests.delete(BASE + 'json_orders/' + 'TestPassport')

        json = response.json()

        assert response.status_code == 200

    def test_get_one_order_pass_000001(self):
        response = requests.get(BASE + 'json_orders/' + '000001')

        assert response.status_code == 200

    def test_get_orders_ordered_by_first_name(self):
        response = requests.get(BASE + 'json_orders' + '?sort-input=first_name')
        json = response.json()

        assert response.status_code == 200

    def test_get_orders_ordered_by_first_name_desc(self):
        response = requests.get(BASE + 'json_orders' + '?sort-input=first_name&desc=None')
        json = response.json()

        assert response.status_code == 200
