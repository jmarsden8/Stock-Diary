from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'hfouerncrfdscfun'

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Use multiple API's for each if need to avoid max calls

# Look for API to filter and show only companies in the S&P 500 with mostly strong buy signals

# Create class for api call

# Create function getting weekly price data
def get_weekly_price():
    pass

def lookup_company_overview(symbol):
    wantedData = [ 
        "Name", "Industry", "Sector", "Country", "Currency", "Description",
        "AnalystRatingBuy", "AnalystRatingHold", "AnalystRatingSell", 
        "AnalystRatingStrongBuy", "AnalystRatingStrongSell", 
        "AnalystTargetPrice", "DilutedEPSTTM", "DividendDate", 
        "DividendPerShare", "DividendYield", "EBITDA", "EPS", 
        "MarketCapitalization", "PERatio", "ProfitMargin", 
        "QuarterlyEarningsGrowthYOY", "QuarterlyRevenueGrowthYOY"
    ]
    apikey = '66RRMTXD87AVY33T'
    function = 'OVERVIEW'
    symbol = symbol.upper()
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}'

    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        if 'Error Message' in data:
            return None
        
        filtered_data = {key: data[key] for key in wantedData if key in data}
        return filtered_data

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        data = lookup_company_overview(symbol)
    
        if data:
            name = data.get('Name', 'N/A')
            description = data.get('Description', 'N/A')
            return render_template('search.html', data=data, name=name, description=description)
        else:
            error = 'No data found for given symbol, or an error occurred.'
            return render_template('search.html', error=error)
    
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/search", methods=['POST'])
def search():
    return render_template('search.html')

@app.route("/bookmarked")
def bookmarked():
    return render_template('bookmarked.html')

if __name__ == "__main__":
    app.run(debug=True)
