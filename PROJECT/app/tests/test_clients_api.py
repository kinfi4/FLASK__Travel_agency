import requests
from app.rest.get_all__API import GetJsonClients
BASE = 'http://127.0.0.1:5000/'


def post_client(password):
    return requests.post(BASE + 'json_clients', data={
            'first_name': 'TestName',
            'last_name': 'TestSurname',
            'passport': password,
            'email': 'Test@test.net',
            'registration_date': '2020-12-31'
        })


def delete_client(password):
    return requests.delete(BASE + 'json_clients/' + password)


class TestClientApi:
    def test_post_a_client(self):
        response = post_client('TestPassport')
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
        response = delete_client('TestPassport')
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
        response = list(GetJsonClients.filter_clients({
            'sort-input': 'first_name'
        }))

        for client_i in range(1, len(response)):
            assert response[client_i - 1].first_name <= response[client_i].first_name

    def test_get_clients_ordered_by_first_name_desc(self):
        response = list(GetJsonClients.filter_clients({
            'sort-input': 'first_name',
            'desc': True
        }))

        for client_i in range(1, len(response)):
            assert response[client_i - 1].first_name >= response[client_i].first_name

    def test_get_clients_ordered_by_last_name(self):
        response = list(GetJsonClients.filter_clients({
            'sort-input': 'last_name'
        }))

        for client_i in range(1, len(response)):
            assert response[client_i - 1].last_name <= response[client_i].last_name

    def test_get_clients_ordered_by_last_name_desc(self):
        response = list(GetJsonClients.filter_clients({
            'sort-input': 'last_name',
            'desc': True
        }))

        for client_i in range(1, len(response)):
            assert response[client_i - 1].last_name >= response[client_i].last_name

    def test_get_clients_ordered_by_orders(self):
        response = list(GetJsonClients.filter_clients({
            'sort-input': 'num_orders'
        }))

        for client_i in range(1, len(response)):
            assert response[client_i - 1].number_of_orders <= response[client_i].number_of_orders

    def test_get_clients_ordered_by_orders_desc(self):
        response = list(GetJsonClients.filter_clients({
            'sort-input': 'num_orders',
            'desc': True
        }))

        for client_i in range(1, len(response)):
            assert response[client_i - 1].number_of_orders >= response[client_i].number_of_orders

