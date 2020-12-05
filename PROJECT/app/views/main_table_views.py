from datetime import date, timedelta

from flask import render_template, request
from flask.views import MethodView

from app import app
from app.models import Client, Order, Tour


# Get All Entities
class GetAllOrdersView(MethodView):
    def get(self):
        return render_template('tables/orders.html', **self.prepare_context(request.args))

    @staticmethod
    def prepare_context(filters=None):
        title = 'Orders'
        add_button = 'add_order'

        if filters:
            s_from_date = filters['tour_date_from']
            s_by_date = filters['tour_date_by']

            if s_from_date and s_by_date:
                from_date = date.fromisoformat(s_from_date)
                by_date = date.fromisoformat(s_by_date)

                by_date += timedelta(days=1)
                from_date -= timedelta(days=1)

                orders = Order.query.filter(Order.tour_date > from_date).filter(by_date > Order.tour_date)
            elif s_from_date:
                from_date = date.fromisoformat(s_from_date)
                from_date -= timedelta(days=1)

                orders = Order.query.filter(Order.tour_date >= from_date)
            elif s_by_date:
                by_date = date.fromisoformat(s_by_date)
                by_date += timedelta(days=1)

                orders = Order.query.filter(by_date >= Order.tour_date)
            else:
                orders = Order.query.all()
        else:
            orders = Order.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'orders': orders,
            'sort_from': filters.get('tour_date_from', None),
            'sort_by': filters.get('tour_date_by', None)
        }


class GetAllClientsView(MethodView):
    def get(self):
        return render_template('tables/clients.html', **self.prepare_context(request.args))

    @staticmethod
    def prepare_context(filters=None):
        title = 'Clients'
        add_button = 'add_client'

        if filters:
            sort_by = filters['sort-input']
            desc = filters.get('desc', False)

            if sort_by and desc:
                if sort_by == 'first_name':
                    clients = list(Client.query.order_by(Client.first_name))
                    clients.reverse()
                elif sort_by == 'last_name':
                    clients = list(Client.query.order_by(Client.last_name))
                    clients.reverse()
                elif sort_by == 'num_orders':
                    clients = list(Client.query.all())
                    clients.sort(key=lambda c: c.number_of_orders, reverse=True)
                else:
                    clients = Client.query.all()

            elif sort_by and not desc:
                if sort_by == 'first_name':
                    clients = Client.query.order_by(Client.first_name)
                elif sort_by == 'last_name':
                    clients = Client.query.order_by(Client.last_name)
                elif sort_by == 'num_orders':
                    clients = list(Client.query.all())
                    clients.sort(key=lambda c: c.number_of_orders)
                else:
                    clients = Client.query.all()
            else:
                clients = Client.query.all()
        else:
            clients = Client.query.all()

        sorting = filters.get('sort-input', None)

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

        return {
            'title': title,
            'add_button': add_button,
            'clients': clients,
            'sort_by': sort_list_variants,
            'desc': filters.get('desc', False)
        }


class GetAllToursView(MethodView):
    def get(self):
        return render_template('tables/tours.html', **self.prepare_context(request.args))

    @staticmethod
    def prepare_context(filters=None):
        title = 'Tours'
        add_button = 'add_tour'

        if filters:
            str_from_price = filters.get('from_price', None)
            str_by_price = filters.get('by_price', None)

            if not str_by_price:
                str_by_price = 10e10

            if not str_from_price:
                str_from_price = '0'

            from_price = float(str_from_price) - 1
            by_price = float(str_by_price) + 1

            if from_price and by_price:
                tours = Tour.query.filter(Tour.day_cost > int(from_price)).filter(by_price > Tour.day_cost)
            elif from_price:
                tours = Tour.query.filter(Tour.day_cost >= from_price)
            elif by_price:
                tours = Tour.query.filter(by_price >= Tour.day_cost)
            else:
                tours = Tour.query.all()
        else:
            tours = Tour.query.all()

        return {
            'title': title,
            'add_button': add_button,
            'tours': tours,
            'from_price': filters.get('from_price', None),
            'by_price': filters.get('by_price', None)
        }
# End Get All Entities


app.add_url_rule('/orders', view_func=GetAllOrdersView.as_view('get_all_orders'), methods=['GET', 'POST'])
app.add_url_rule('/clients', view_func=GetAllClientsView.as_view('get_all_clients'), methods=['GET', 'POST'])
app.add_url_rule('/tours', view_func=GetAllToursView.as_view('get_all_tours'), methods=['GET', 'POST'])
