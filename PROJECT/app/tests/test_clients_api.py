import requests
import pytest

BASE = 'http://127.0.0.1:5000/'


class TestClientApi:
    def test_post_a_client(self):
        response = requests.post(BASE + 'json_clients', data={
            'first_name': 'TestName',
            'last_name': 'TestSurname',
            'passport': 'TestPassport',
            'email': 'Test@test.net',
            'registration_date': '2020-12-31'
        })

        json = response.json()

        assert response.status_code == 200
        assert json['first_name'] == 'TestName'
        assert json['last_name'] == 'TestSurname'
        assert json['passport'] == 'TestPassport'
        assert json['email'] == 'Test@test.net'

    def test_put_a_client(self):
        response = requests.put(BASE + 'json_clients/' + 'TestPassport', data={
            'first_name': 'NewTestName',
            'last_name': 'NewTestSurname'
        })

        json = response.json()

        assert response.status_code == 200
        assert json['first_name'] == 'NewTestName'
        assert json['last_name'] == 'NewTestSurname'
        assert json['passport'] == 'TestPassport'
        assert json['email'] == 'Test@test.net'

    def test_get_new_client(self):
        response = requests.get(BASE + 'json_clients/' + 'TestPassport')

        json = response.json()

        assert response.status_code == 200
        assert json['first_name'] == 'NewTestName'
        assert json['last_name'] == 'NewTestSurname'
        assert json['passport'] == 'TestPassport'
        assert json['email'] == 'Test@test.net'

    def test_delete_new_client(self):
        response = requests.delete(BASE + 'json_clients/' + 'TestPassport')

        json = response.json()

        assert response.status_code == 200
        assert json['first_name'] == 'NewTestName'
        assert json['last_name'] == 'NewTestSurname'
        assert json['passport'] == 'TestPassport'
        assert json['email'] == 'Test@test.net'

    def test_get_one_client_pass_000001(self):
        response = requests.get(BASE + 'json_clients/' + '000001')

        assert response.status_code == 200
        assert response.json()['first_name'] == 'Marina'
        assert response.json()['last_name'] == 'Lisoviec'

    def test_get_clients_ordered_by_first_name(self):
        response = requests.get(BASE + 'json_clients' + '?sort-input=first_name')
        json = response.json()

        assert response.status_code == 200
        for client_i in range(1, len(json)):
            assert json[client_i - 1]['first_name'] <= json[client_i]['first_name']

    def test_get_clients_ordered_by_first_name_desc(self):
        response = requests.get(BASE + 'json_clients' + '?sort-input=first_name&desc=None')
        json = response.json()

        assert response.status_code == 200
        for client_i in range(1, len(json)):
            assert json[client_i - 1]['first_name'] >= json[client_i]['first_name']

    def test_get_clients_ordered_by_last_name(self):
        response = requests.get(BASE + 'json_clients' + '?sort-input=last_name')
        json = response.json()

        assert response.status_code == 200
        for client_i in range(1, len(json)):
            assert json[client_i - 1]['last_name'] <= json[client_i]['last_name']

    def test_get_clients_ordered_by_last_name_desc(self):
        response = requests.get(BASE + 'json_clients' + '?sort-input=last_name&desc=None')
        json = response.json()

        assert response.status_code == 200
        for client_i in range(1, len(json)):
            assert json[client_i - 1]['last_name'] >= json[client_i]['last_name']

    def test_get_clients_ordered_by_orders(self):
        response = requests.get(BASE + 'json_clients' + '?sort-input=num_orders')
        json = response.json()

        assert response.status_code == 200
        for client_i in range(1, len(json)):
            assert json[client_i - 1]['number_of_orders'] <= json[client_i]['number_of_orders']

    def test_get_clients_ordered_by_orders_desc(self):
        response = requests.get(BASE + 'json_clients' + '?sort-input=num_orders&desc=None')
        json = response.json()

        assert response.status_code == 200
        for client_i in range(1, len(json)):
            assert json[client_i - 1]['number_of_orders'] >= json[client_i]['number_of_orders']

