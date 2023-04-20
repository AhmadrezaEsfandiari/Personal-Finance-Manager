import re
import shelve
import datetime
import argparse


class PersonalFinanceManager:
    path = 'F:\Didex\Python\week 11\HW'

    def __init__(self, type, date, amount, category, description):
        self.type = type
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, d):
        if re.search('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$', d):

            self._date = d
        else:
            raise ValueError('the date is not valid!')

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, a):
        if int(a) and a > 0:
            self._amount = a
        else:
            raise ValueError('the amount is not valid!')

    def add_new_finance(self):
        with shelve.open(PersonalFinanceManager.path) as pfm:
            key_id = 1
            if pfm.items():
                for key, value in pfm.items():
                    key_id = int(key)
                finance_dict = {'Type': self.type, 'Amount': self._amount,
                                'Date': self._date, 'Category': self.category,
                                'Description': self.description}
                key_id += 1
                pfm[str(key_id)] = finance_dict
                print('Transaction added successfully...')
            else:
                finance_dict = {'Type': self.type, 'Amount': self._amount,
                                'Date': self._date, 'Category': self.category,
                                'Description': self.description}
                pfm[str(key_id)] = finance_dict
                print('Transaction added successfully...')

    @staticmethod
    def view_finance(start_date_in, end_date_in):
        start_date = re.match('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$', start_date_in)
        end_date = re.match('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$', end_date_in)
        convert_start_date = datetime.datetime.strptime(start_date_in, "%Y-%m-%d").date()
        convert_end_date = datetime.datetime.strptime(end_date_in, "%Y-%m-%d").date()
        if start_date and end_date:
            with shelve.open(PersonalFinanceManager.path) as pfm:
                if pfm.items():
                    item_value_finance = dict(pfm.items()).values()
                    filter_finance = filter(lambda x: convert_start_date <= datetime.datetime.strptime(x['Date'],
                                            "%Y-%m-%d").date() < convert_end_date, item_value_finance)

                    list_filter_finance = list(filter_finance)
                    return list_filter_finance
                else:
                    return 'the file is empty!'
        else:
            return 'the date input is not valid!'

    @staticmethod
    def report_finance(start_date_in, end_date_in):
        start_date = re.match('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$', start_date_in)
        end_date = re.match('^20[0-2][0-9]-((0[1-9])|(1[0-2]))-([0-2][1-9]|3[0-1])$', end_date_in)
        convert_start_date = datetime.datetime.strptime(start_date_in, "%Y-%m-%d").date()
        convert_end_date = datetime.datetime.strptime(end_date_in, "%Y-%m-%d").date()
        if start_date and end_date:
            with shelve.open(PersonalFinanceManager.path) as pfm:
                if pfm.items():
                    item_value_finance = dict(pfm.items()).values()
                    filter_finance = filter(lambda x: convert_start_date < datetime.datetime.strptime(x['Date'],
                                            "%Y-%m-%d").date() < convert_end_date, item_value_finance)

                    list_filter_finance = list(filter_finance)
                    print(list_filter_finance)
                    total_incom = 0
                    total_expenses = 0
                    expenses_by_category = {}
                    for i in list_filter_finance:
                        if i['Type'] == 'income':
                            total_incom += i['Amount']
                        elif i['Type'] == 'expens':
                            total_expenses += i['Amount']
                            expenses_by_category[i['Category']] = (i['Amount'])
                    return f'total income:{total_incom}, total expenses:{total_expenses},' \
                           f' balance:{total_incom-total_expenses}, expenses by category:{expenses_by_category}'
                else:
                    return 'the file is empty!'
        else:
            return 'the date input is not valid!'


parser = argparse.ArgumentParser()

parser.add_argument('func', type=str, choices=['add', 'view', 'report'])
parser.add_argument('--type', type=str)
parser.add_argument('--date', type=str, default=datetime.date.today())
parser.add_argument('--amount', type=int)
parser.add_argument('--category', type=str)
parser.add_argument('--description', type=str)
parser.add_argument('--start_date', type=str, default=datetime.date.today())
parser.add_argument('--end_date', type=str, default=datetime.date.today())

args = parser.parse_args()
result = args.func

if result == 'add':
    pfm = PersonalFinanceManager(args.type, args.date, args.amount, args.category, args.description)
    pfm.add_new_finance()
elif result == 'view':
    print(*PersonalFinanceManager.view_finance(args.start_date, args.end_date))
elif result == 'report':
    print(PersonalFinanceManager.report_finance(args.start_date, args.end_date))