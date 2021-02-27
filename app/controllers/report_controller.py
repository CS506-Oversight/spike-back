"""Implementation for controlling the user data."""
import csv
from app.config import fb_db
from datetime import date
import datetime

"""Controller for usage_reports."""
__all__ = ('ReportController',)


class ReportController:
    """Controller for usage_reports."""

    @staticmethod
    def test_report():
        """Get Menu."""
        final_menu = {'menu': []}
        col_ref = fb_db.collection('Menu')
        doc_ref = col_ref.get()
        for doc in doc_ref:
            final_menu['menu'].append(doc.to_dict())

        """Get orders"""
        orders = {'orders': []}
        order_ref = fb_db.collection('Orders')
        orders_docs = order_ref.get()
        for order in orders_docs:
            orders['orders'].append(order.to_dict())

        """date data"""
        date_data_ref = fb_db.collection('Orders')
        query = date_data_ref.order_by(
            'order_date'
        ).stream()
        unique_dates = []
        unique_weeks = []
        unique_months = []
        unique_years = []
        for item in query:
            order = item.to_dict()
            order_date = order['order_date'].date().strftime("%x")
            if order_date not in unique_dates:
                unique_dates.append(order_date)
            order_week = order['order_date'].date().strftime("%U")
            if order_week not in unique_weeks:
                unique_weeks.append(order_week)
            order_month = order['order_date'].date().strftime("%B")
            if order_month not in unique_months:
                unique_months.append(order_month)
            order_year = order['order_date'].date().strftime("%Y")
            if order_year not in unique_years:
                unique_years.append(order_year)


        """DAY REPORT"""
        """header row"""
        row1 = []
        row1.append("Day")
        row1.append("Total Profit")
        row1.append("Number of Orders")
        row1.append("Number of Customers")
        food_menu = final_menu['menu']

        with open('./app/templates/days_report.csv', mode='w') as csvfile:
            test_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            for item in food_menu:
                row1.append(item["name"])
            test_writer.writerow(row1)
            for date in unique_dates:
                food_nums = []
                for i in range(0, len(food_menu)):
                    food_nums.append(0)
                row = []
                total_profit = 0
                num_orders = 0
                unique_customers = []
                row.append(date)
                query = date_data_ref.order_by(
                    'order_date'
                ).stream()
                for item in query:
                    order = item.to_dict()
                    if date == order['order_date'].date().strftime("%x"):
                        num_orders += 1
                        total_profit += order['order_total']
                        if order['customer_id'] not in unique_customers:
                            unique_customers.append(order['customer_id'])
                        for product in order['items_ordered']:
                            units = product.split(' | ')
                            for x in range(0, len(food_menu)):
                                if units[0] == food_menu[x]['item_id']:
                                    food_nums[x] += int(units[1])
                row.append(round(total_profit, 2))
                row.append(num_orders)
                row.append(len(unique_customers))
                row += food_nums
                test_writer.writerow(row)

        """WEEK REPORT"""
        """header row"""
        row1 = []
        row1.append("Week")
        row1.append("Total Profit")
        row1.append("Number of Orders")
        row1.append("Number of Customers")
        food_menu = final_menu['menu']

        with open('./app/templates/weeks_report.csv', mode='w') as csvfile:
            test_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            for item in food_menu:
                row1.append(item["name"])
            test_writer.writerow(row1)
            for date in unique_weeks:
                food_nums = []
                for i in range(0, len(food_menu)):
                    food_nums.append(0)
                row = []
                total_profit = 0
                num_orders = 0
                unique_customers = []
                row.append(date)
                query = date_data_ref.order_by(
                    'order_date'
                ).stream()
                for item in query:
                    order = item.to_dict()
                    if date == order['order_date'].date().strftime("%U"):
                        num_orders += 1
                        total_profit += order['order_total']
                        if order['customer_id'] not in unique_customers:
                            unique_customers.append(order['customer_id'])
                        for product in order['items_ordered']:
                            units = product.split(' | ')
                            for x in range(0, len(food_menu)):
                                if units[0] == food_menu[x]['item_id']:
                                    food_nums[x] += int(units[1])
                row.append(round(total_profit, 2))
                row.append(num_orders)
                row.append(len(unique_customers))
                row += food_nums
                test_writer.writerow(row)

        """MONTH REPORT"""
        """header row"""
        row1 = []
        row1.append("Month")
        row1.append("Total Profit")
        row1.append("Number of Orders")
        row1.append("Number of Customers")
        food_menu = final_menu['menu']

        with open('./app/templates/months_report.csv', mode='w') as csvfile:
            test_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            for item in food_menu:
                row1.append(item["name"])
            test_writer.writerow(row1)
            for date in unique_months:
                food_nums = []
                for i in range(0, len(food_menu)):
                    food_nums.append(0)
                row = []
                total_profit = 0
                num_orders = 0
                unique_customers = []
                row.append(date)
                query = date_data_ref.order_by(
                    'order_date'
                ).stream()
                for item in query:
                    order = item.to_dict()
                    if date == order['order_date'].date().strftime("%B"):
                        num_orders += 1
                        total_profit += order['order_total']
                        if order['customer_id'] not in unique_customers:
                            unique_customers.append(order['customer_id'])
                        for product in order['items_ordered']:
                            units = product.split(' | ')
                            for x in range(0, len(food_menu)):
                                if units[0] == food_menu[x]['item_id']:
                                    food_nums[x] += int(units[1])
                row.append(round(total_profit, 2))
                row.append(num_orders)
                row.append(len(unique_customers))
                row += food_nums
                test_writer.writerow(row)

        """YEAR REPORT"""
        """header row"""
        row1 = []
        row1.append("Year")
        row1.append("Total Profit")
        row1.append("Number of Orders")
        row1.append("Number of Customers")
        food_menu = final_menu['menu']

        with open('./app/templates/years_report.csv', mode='w') as csvfile:
            test_writer = csv.writer(csvfile, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            for item in food_menu:
                row1.append(item["name"])
            test_writer.writerow(row1)
            for date in unique_years:
                food_nums = []
                for i in range(0, len(food_menu)):
                    food_nums.append(0)
                row = []
                total_profit = 0
                num_orders = 0
                unique_customers = []
                row.append(date)
                query = date_data_ref.order_by(
                    'order_date'
                ).stream()
                for item in query:
                    order = item.to_dict()
                    if date == order['order_date'].date().strftime("%Y"):
                        num_orders += 1
                        total_profit += order['order_total']
                        if order['customer_id'] not in unique_customers:
                            unique_customers.append(order['customer_id'])
                        for product in order['items_ordered']:
                            units = product.split(' | ')
                            for x in range(0, len(food_menu)):
                                if units[0] == food_menu[x]['item_id']:
                                    food_nums[x] += int(units[1])
                row.append(round(total_profit, 2))
                row.append(num_orders)
                row.append(len(unique_customers))
                row += food_nums
                test_writer.writerow(row)



