from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessary for flash messages

# In-memory database for inventory and orders (for simplicity)
inventory = []
orders = []

@app.route('/')
def home():
    total_amount = sum(order['total_price'] for order in orders)
    return render_template('index.html', inventory=inventory, orders=orders, total_amount=total_amount)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    item = {'name': item_name, 'quantity': quantity, 'price': price}
    inventory.append(item)
    
    flash('Item added successfully!')
    return redirect(url_for('home'))

@app.route('/purchase', methods=['POST'])
def purchase():
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    total_price = 0

    for item in inventory:
        if item['name'] == item_name:
            total_price = item['price'] * quantity
            order = {
                'item_name': item_name,
                'quantity': quantity,
                'total_price': total_price
            }
            orders.append(order)
            flash(f'Purchased {quantity} of {item_name} for KES {total_price:.2f}')
            break
    else:
        flash('Item not found in inventory!')

    return redirect(url_for('home'))

@app.route('/print_receipt')
def print_receipt():
    total_amount = sum(order['total_price'] for order in orders)
    return render_template('receipt.html', orders=orders, total_amount=total_amount)

def get_mpesa_access_token():
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    return mpesa_access_token['access_token']

@app.route('/mpesa_payment', methods=['POST'])
def mpesa_payment():
    access_token = get_mpesa_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    payload = {
        'BusinessShortCode': '174379',
        'Password': 'YOUR_PASSWORD',
        'Timestamp': 'YOUR_TIMESTAMP',
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': '1',  # Amount to be charged
        'PartyA': 'PHONE_NUMBER',  # Customer's phone number
        'PartyB': '174379',
        'PhoneNumber': 'PHONE_NUMBER',
        'CallBackURL': 'YOUR_CALLBACK_URL',
        'AccountReference': 'YOUR_ACCOUNT_REFERENCE',
        'TransactionDesc': 'Payment for item'
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    return response.text

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, flash
# import requests
# from requests.auth import HTTPBasicAuth
# import json

# app = Flask(__name__)
# app.secret_key = 'supersecretkey'  # Necessary for flash messages

# # In-memory database for inventory and orders (for simplicity)
# inventory = []
# orders = []

# @app.route('/')
# def home():
#     return render_template('index.html', inventory=inventory, orders=orders)

# @app.route('/add_item', methods=['POST'])
# def add_item():
#     item_name = request.form['item_name']
#     quantity = int(request.form['quantity'])
#     price = float(request.form['price'])
    
#     item = {'name': item_name, 'quantity': quantity, 'price': price}
#     inventory.append(item)
    
#     flash('Item added successfully!')
#     return redirect(url_for('home'))

# @app.route('/purchase', methods=['POST'])
# def purchase():
#     item_name = request.form['item_name']
#     quantity = int(request.form['quantity'])
#     total_price = 0

#     for item in inventory:
#         if item['name'] == item_name:
#             total_price = item['price'] * quantity
#             order = {
#                 'item_name': item_name,
#                 'quantity': quantity,
#                 'total_price': total_price
#             }
#             orders.append(order)
#             flash(f'Purchased {quantity} of {item_name} for KES {total_price:.2f}')
#             break
#     else:
#         flash('Item not found in inventory!')

#     return redirect(url_for('home'))

# @app.route('/print_receipt')
# def print_receipt():
#     return render_template('receipt.html', orders=orders)

# def get_mpesa_access_token():
#     consumer_key = 'YOUR_CONSUMER_KEY'
#     consumer_secret = 'YOUR_CONSUMER_SECRET'
#     api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
#     r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     return mpesa_access_token['access_token']

# @app.route('/mpesa_payment', methods=['POST'])
# def mpesa_payment():
#     access_token = get_mpesa_access_token()
#     api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#     headers = {'Authorization': 'Bearer {}'.format(access_token)}
#     payload = {
#         'BusinessShortCode': '174379',
#         'Password': 'YOUR_PASSWORD',
#         'Timestamp': 'YOUR_TIMESTAMP',
#         'TransactionType': 'CustomerPayBillOnline',
#         'Amount': '1',  # Amount to be charged
#         'PartyA': 'PHONE_NUMBER',  # Customer's phone number
#         'PartyB': '174379',
#         'PhoneNumber': 'PHONE_NUMBER',
#         'CallBackURL': 'YOUR_CALLBACK_URL',
#         'AccountReference': 'YOUR_ACCOUNT_REFERENCE',
#         'TransactionDesc': 'Payment for item'
#     }
    
#     response = requests.post(api_url, json=payload, headers=headers)
#     return response.text

# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, render_template, request, redirect, url_for, flash
# import requests
# from requests.auth import HTTPBasicAuth
# import json


# app = Flask(__name__)
# app.secret_key = 'supersecretkey'  # Necessary for flash messages

# # In-memory database (for simplicity)
# inventory = []

# @app.route('/')
# def home():
#     return render_template('index.html', inventory=inventory)

# @app.route('/add_item', methods=['POST'])
# def add_item():
#     item_name = request.form['item_name']
#     quantity = request.form['quantity']
#     price = request.form['price']
    
#     item = {'name': item_name, 'quantity': quantity, 'price': price}
#     inventory.append(item)
    
#     flash('Item added successfully!')
#     return redirect(url_for('home'))



# def get_mpesa_access_token():
#     consumer_key = 'YOUR_CONSUMER_KEY'
#     consumer_secret = 'YOUR_CONSUMER_SECRET'
#     api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
#     r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     return mpesa_access_token['access_token']

# @app.route('/mpesa_payment', methods=['POST'])
# def mpesa_payment():
#     access_token = get_mpesa_access_token()
#     api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
#     headers = {'Authorization': 'Bearer {}'.format(access_token)}
#     payload = {
#         'BusinessShortCode': '174379',
#         'Password': 'YOUR_PASSWORD',
#         'Timestamp': 'YOUR_TIMESTAMP',
#         'TransactionType': 'CustomerPayBillOnline',
#         'Amount': '1',  # Amount to be charged
#         'PartyA': 'PHONE_NUMBER',  # Customer's phone number
#         'PartyB': '174379',
#         'PhoneNumber': 'PHONE_NUMBER',
#         'CallBackURL': 'YOUR_CALLBACK_URL',
#         'AccountReference': 'YOUR_ACCOUNT_REFERENCE',
#         'TransactionDesc': 'Payment for item'
#     }
    
#     response = requests.post(api_url, json=payload, headers=headers)
#     return response.text    

# if __name__ == '__main__':
#     app.run(debug=True)
