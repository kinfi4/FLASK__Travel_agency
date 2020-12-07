import requests

from app.models import Tour
from app.rest.get_all__API import GetJsonTours

BASE = 'http://127.0.0.1:5000/'


class TestToursApi:
    def test_post_a_tour(self):
        response = requests.post(BASE + 'json_tours', data={
            'name': 'TestName',
            'country': 'TestCountry',
            'hotel': 'TestHotel',
            'tour_includes': 'TestTourIncludes',
            'day_cost': 100
        })
        json = response.json()

        assert response.status_code == 200
        assert json['name'] == 'TestName'
        assert json['country'] == 'TestCountry'
        assert json['hotel'] == 'TestHotel'
        assert json['tour_includes'] == 'TestTourIncludes'
        assert json['day_cost'] == 100

    def test_put_a_tour(self):
        my_tour = Tour.query.filter(
            Tour.name == 'TestName' and Tour.hotel == 'TestHotel' and Tour.country == 'TestCountry').first()

        response = requests.put(BASE + 'json_tours/' + str(my_tour.id), data={
            'name': 'NewTestName',
            'day_cost': 150
        })

        json = response.json()

        assert response.status_code == 200
        assert json['name'] == 'NewTestName'
        assert json['country'] == 'TestCountry'
        assert json['hotel'] == 'TestHotel'
        assert json['day_cost'] == 150

    def test_get_a_tour(self):
        my_tour = Tour.query.filter(
            Tour.name == 'NewTestName' and Tour.hotel == 'TestHotel' and Tour.country == 'TestCountry').first()

        response = requests.get(BASE + 'json_tours/' + f'{my_tour.id}')

        json = response.json()

        assert response.status_code == 200
        assert json['name'] == 'NewTestName'
        assert json['country'] == 'TestCountry'
        assert json['hotel'] == 'TestHotel'
        assert json['day_cost'] == 150

    def test_delete_a_tour(self):
        my_tour = Tour.query.filter(
            Tour.name == 'NewTestName' and Tour.hotel == 'TestHotel' and Tour.country == 'TestCountry').first()

        response = requests.delete(BASE + 'json_tours/' + f'{my_tour.id}')

        json = response.json()

        assert response.status_code == 200
        assert json['name'] == 'NewTestName'
        assert json['country'] == 'TestCountry'
        assert json['hotel'] == 'TestHotel'
        assert json['day_cost'] == 150

    def test_filter_tours_from_by(self):
        response = list(GetJsonTours.filter_tours({
            'from_price': 150,
            'by_price': 250
        }))

        for tour in response:
            assert 250 >= tour.day_cost >= 150

    def test_filter_tours_from(self):
        response = list(GetJsonTours.filter_tours({
            'from_price': 150
        }))

        for tour in response:
            assert tour.day_cost >= 150

    def test_filter_tours_by(self):
        response = list(GetJsonTours.filter_tours({
            'by_price': 200
        }))

        for tour in response:
            assert 200 >= tour.day_cost


