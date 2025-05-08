import requests
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
# pip install finnhub-python
import finnhub

load_dotenv()

app = Flask(__name__)
base_url = 'https://finnhub.io/api/v1/'
api_key = os.getenv('API_KEY')

# client imported from github page for accessing API:
# finnhub_client = finnhub.Client(api_key=os.getenv('API_KEY'))
# print(finnhub_client.quote('AAPL'))

# checks which button was pressed so server knows which API endpoint to call
@app.route('/form-action', methods=['POST'])
def form_action():
    stock_symbol = request.form.get('stock').upper()
    action = request.form.get('action')

    if action == "Check Price":
        return redirect(url_for('get_stock_price', stock=stock_symbol))

    elif action == "Check Stock News":
        return redirect(url_for('get_stock_news', stock=stock_symbol))

    return render_template('index.html')

# gets current stock price for stock symbol queried
@app.route('/stock-price', methods=['GET'])
def get_stock_price():
    stock_symbol = request.args.get('stock')
    url = f"{base_url}/quote?symbol={stock_symbol}&token={api_key}"

    response = requests.get(url)
    stock_prices = response.json()
    print(stock_prices)

    return render_template('index.html', prices=stock_prices, stock=stock_symbol)

# gets current news for stock symbol queried
@app.route('/stock-news', methods=['GET'])
def get_stock_news():
    stock_symbol = request.args.get('stock')
    url = f"{base_url}/company-news?symbol={stock_symbol}&from=2025-05-08&to=2025-05-08&token={api_key}"

    response = requests.get(url)
    stock_news = response.json()
    if stock_news:
        print('successfully retrieved stock_news')

    return render_template('index.html', stock_news=stock_news, stock=stock_symbol)

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)