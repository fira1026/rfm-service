import os
import csv
from datetime import datetime
from django.conf import settings


def load_csv(file_path='', delimiter=',', quote_char='"', with_header=False):

    with open(file_path, 'r', encoding="utf8") as csv_file:
        csv_file_object = csv.reader(csv_file, delimiter=delimiter, quotechar=quote_char)

        if not with_header:
            next(csv_file_object)

        for row in csv_file_object:
            yield [_.strip() for _ in row]


def compose_rfm_input(row_data):
    # sum(Quantity*UnitPrice) over same InvoiceNo -> grand_total
    # InvoiceNo -> order_id
    # CustomerID -> customer
    # InvoiceDate -> order_date (remove time, take note of date format)
    # Assume one order_id can only in one invoice_date

    customer_id = row_data.get('CustomerID')
    order_id = row_data.get('InvoiceNo')

    quantity = row_data.get('Quantity')
    unit_price = row_data.get('UnitPrice')
    grand_total = int(quantity) * float(unit_price)

    date_str = row_data.get('InvoiceDate')
    date_obj = datetime.strptime(date_str, '%m/%d/%Y %H:%M')
    date_str = date_obj.strftime("%m/%d/%Y")

    data = {
        'customer': customer_id,
        'order_id': order_id,
        'grand_total': grand_total,
        'order_date': date_str,
    }

    return data


def transfer_kaggle_data(file_path='./data.csv'):
    # Step 1: get data from kaggle data
    csv_rows = load_csv(file_path=file_path)

    fields = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
              'UnitPrice', 'CustomerID', 'Country',]

    rfm_data = {}

    for row_index, row in enumerate(csv_rows, 1):
        row_data = dict(zip(fields, row))
        data = compose_rfm_input(row_data)
        customer = data['customer']
        order_id = data['order_id']
        grand_total = int(data['grand_total'])
        order_date = data['order_date']

        if customer not in rfm_data:
            rfm_data[customer] = {
                order_id: {
                    'grand_total': grand_total,
                    'order_date': order_date,
                }
            }
        elif order_id not in rfm_data[customer]:
            rfm_data[customer][order_id] = {
                'grand_total': grand_total,
                'order_date': order_date,
            }
        else:
            rfm_data[customer][order_id]['grand_total'] += grand_total

    rows = []
    for customer in rfm_data:
        for order_id in rfm_data[customer]:
            # Only process grand_total > 0
            if rfm_data[customer][order_id]['grand_total'] > 0:
                rows.append(
                    [
                        rfm_data[customer][order_id]['order_date'],
                        order_id,
                        customer,
                        rfm_data[customer][order_id]['grand_total'],
                    ]
                )

    if not rows:
        return

    # step 2: compose csv file for RFM-analysis.py input
    file_path = '/home/vscode/miniproj/api/results/sample-orders.csv'

    if os.path.exists(file_path):
        os.unlink(file_path)

    fields = ['order_date', 'order_id', 'customer', 'grand_total']
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(rows)

    return file_path


def handle_uploaded_file(f):
    file_name = 'data1.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if os.path.exists(file_path):
        os.unlink(file_path)

    with open(file_path, "wb+") as destination:
        for chunk in f:
            destination.write(chunk)

    return file_path
