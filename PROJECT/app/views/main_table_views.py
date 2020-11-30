from datetime import date

from flask import render_template, request
from flask.views import MethodView

from app import app
from app.models import Client, Order, Tour


# Get All Entities
class GetAllOrdersView(MethodView):
    def get(self):
        return render_template('tables/orders.html', **self.prepare_context(request.args))

    def prepare_context(self, filters=None):
        title = 'Orders'
        add_button = 'add_order'

        if filters:
            s_from_date = filters['tour_date_from']
            s_by_date = filters['tour_date_by']

            if s_from_date and s_by_date:
                from_date = date.fromisoformat(s_from_date)
                by_date = date.fromisoformat(s_by_date)

                by_date.replace(by_date.year, by_date.month, by_date.day + 1)
                from_date.replace(from_date.year, from_date.month, from_date.day - 1)

                orders = Order.query.filter(Order.tour_date > from_date).filter(by_date > Order.tour_date)
            elif s_from_date:
                from_date = date.fromisoformat(s_from_date)
                from_date.replace(from_date.year, from_date.month, from_date.day - 1)

                orders = Order.query.filter(Order.tour_date >= from_date)
            elif s_by_date:
                by_date = date.fromisoformat(s_by_date)
                by_date.replace(by_date.year, by_date.month, by_date.day + 1)

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

    def prepare_context(self, filters=None):
        title = 'Clients'
        add_button = 'add_client'

        if filters:
            sort_by = filters['sort-input']
            desc = filters.get('desc', False)

            # desc = True if desc == 'on' else False
            print(desc, sort_by)
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

        return {
            'title': title,
            'add_button': add_button,
            'clients': clients,
            'sort_by': filters.get('sort-input', None),
            'desc': filters.get('desc', None)
        }


class GetAllToursView(MethodView):
    def get(self):
        return render_template('tables/tours.html', **self.prepare_context(request.args))

    def prepare_context(self, filters=None):
        title = 'Tours'
        add_button = 'add_tour'

        if filters:
            from_price = float(filters['from_price']) - 1
            by_price = float(filters['by_price']) + 1

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

