from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Routes
@app.route('/')
def index():
    globalSummary = getGlobalStatistics()
    countryList = getAllCountries()
    countryList.sort(key=lambda x: x['Country'])
    return render_template('index.html', datas=globalSummary, countries=countryList)


# Helper Functions
def getGlobalStatistics():
    return requests.get('https://api.covid19api.com/summary').json()['Global']


def getAllCountries():
    return requests.get('https://api.covid19api.com/countries').json()


if __name__ == '__main__':
    app.run(debug=True)
