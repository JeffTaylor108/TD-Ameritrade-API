import requests
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
import datetime
# pip install finnhub-python
import finnhub

load_dotenv()

app = Flask(__name__)
base_url = 'https://finnhub.io/api/v1/'
api_key = os.getenv('API_KEY')

current_date = datetime.date.today()

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
    url = f"{base_url}/company-news?symbol={stock_symbol}&from={current_date}&to={current_date}&token={api_key}"

    response = requests.get(url)
    stock_news = response.json()
    if stock_news:
        print('successfully retrieved stock_news')

    return render_template('index.html', stock_news=stock_news, stock=stock_symbol, date=current_date)

# compares two companies for stock prices and recommendation trends
@app.route('/stock-comparison', methods=['GET'])
def compare_stocks():
    stock_symbol1 = request.args.get('stock1').upper()
    stock_symbol2 = request.args.get('stock2').upper()

    stock1_price_url = f"{base_url}/quote?symbol={stock_symbol1}&token={api_key}"
    stock2_price_url = f"{base_url}/quote?symbol={stock_symbol2}&token={api_key}"
    stock1_recc_url = f"{base_url}/stock/recommendation?symbol={stock_symbol1}&token={api_key}"
    stock2_recc_url = f"{base_url}/stock/recommendation?symbol={stock_symbol2}&token={api_key}"

    stock1_prices = requests.get(stock1_price_url).json()
    stock2_prices = requests.get(stock2_price_url).json()
    stock1_reccs = requests.get(stock1_recc_url).json()
    stock2_reccs = requests.get(stock2_recc_url).json()

    result = {
        'stock1': {
            'symbol': stock1_reccs[0]['symbol'],
            'current_price': stock1_prices['c'],
            'change_in_price': stock1_prices['d'],
            'daily_volatility': stock1_prices['h'] - stock1_prices['l'],
            'recommended_to_buy': stock1_reccs[0]['buy'],
            'recommended_to_hold': stock1_reccs[0]['hold'],
            'recommended_to_sell': stock1_reccs[0]['sell']
        },
        'stock2': {
            'symbol': stock2_reccs[0]['symbol'],
            'current_price': stock2_prices['c'],
            'change_in_price': stock2_prices['d'],
            'daily_volatility': stock2_prices['h'] - stock2_prices['l'],
            'recommended_to_buy': stock2_reccs[0]['buy'],
            'recommended_to_hold': stock2_reccs[0]['hold'],
            'recommended_to_sell': stock2_reccs[0]['sell']
        }
    }
    print(result)

    return render_template('index.html', comparison=result, stock1=stock_symbol1, stock2=stock_symbol2)

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)