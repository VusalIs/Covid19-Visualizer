from flask import Flask, render_template, request
from datetime import datetime
import requests

# Routes


@app.route('/')
def index():
    globalSummary = getGlobalStatistics()
    countryList = getAllCountries()
    countryList.sort(key=lambda x: x['Country'])
    return render_template('index.html', datas=globalSummary, countries=countryList)


@app.route('/country-statistic')
def countryStatistics():
    country = request.args.get('country')
    dailystat = getDailyStatByCountry(country)
    summaryOfCountry = dailystat[-1]
    summaryOfPrevDay = dailystat[-2]
    newCases = {
        'NewConfirmed': summaryOfCountry['Confirmed'] - summaryOfPrevDay['Confirmed'],
        'NewDeaths': summaryOfCountry['Deaths'] - summaryOfPrevDay['Deaths'],
        'NewRecovered': summaryOfCountry['Recovered'] - summaryOfCountry['Recovered']
    }
    infectedPeopleDaily = list(map(
        lambda value: {'y': value['Confirmed'], 'x': datetime.strptime(value['Date'],
                                                                       "%Y-%m-%dT%H:%M:%SZ")}, dailystat))
    return render_template('country.html', summaryData=summaryOfCountry, country=country, infectedPeopleDaily=infectedPeopleDaily, newCases=newCases)

# Helper Functions


def getGlobalStatistics():
    return requests.get('https://api.covid19api.com/summary').json()['Global']


def getAllCountries():
    return requests.get('https://api.covid19api.com/countries').json()


def getDailyStatByCountry(country):
    return requests.get('https://api.covid19api.com/dayone/country/{}'.format(country)).json()


def create_app():
    app = Flask(__name__)
    return app
