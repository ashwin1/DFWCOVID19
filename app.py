from flask import Flask, render_template
from flask_cors import CORS, cross_origin
import csv
from flask import render_template, url_for, request, redirect

current_cache = {}

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'application/json'


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)


current_cache['about'] = {}

@app.route('/about', methods=['GET','POST'])
@cross_origin(origins='*')
@cross_origin(supports_credentials=True)
def getData():
    print(request.get_json())
    if request.get_json().get('placeValue'):
        placeValue = request.get_json().get('placeValue')
        print("place value if", placeValue)
    else:
        placeValue = "Dallas"
    print("### ABOUT API --> Place value => ", placeValue)
    returnObject = {}

    if current_cache.get('about', None) and current_cache.get('about', None).get(placeValue, None):
        print("Fetching from cache")
        return current_cache['about'][placeValue]
    print("Fetching from file")
    current_cache['about'][placeValue] = {}
    current_cache['about'][placeValue]['confirmed'] = []
    current_cache['about'][placeValue]['deaths'] = []

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Admin2']:
                returnObject['confirmed'] = row
                current_cache['about'][placeValue]['confirmed'] = row

    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Admin2']:
                returnObject['deaths'] = row
                current_cache['about'][placeValue]['deaths'] = row

    import json
    print("Updated current_cache value ", json.dumps(current_cache))
    return returnObject

current_cache['texasData'] = {}
@app.route('/texasData', methods=['GET','POST'])
@cross_origin(origins='*')
@cross_origin(supports_credentials=True)
def getTexasData():
    print(request.get_json())
    if request.get_json().get('placeValue'):
        placeValue = request.get_json().get('placeValue')
        print("place value TexasConfirmedDeaths", placeValue)
    else:
        placeValue = "Texas"
    print("Place value TexasConfirmedDeaths=>  ", placeValue)
    returnObject = {}
    returnObject['texasDataRows'] =[]
    returnObject['texasDeathsCardRow'] = []


    if current_cache.get('texasData', None):
        return current_cache['texasData']
    current_cache['texasData'] = {}
    current_cache['texasData']['texasDataRows'] = []
    current_cache['texasData']['texasDeathsCardRow'] = []

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                returnObject['texasDataRows'].append(row)
                current_cache['texasData']['texasDataRows'].append(row)

    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                returnObject['texasDeathsCardRow'].append(row)
                current_cache['texasData']['texasDeathsCardRow'].append(row)
    return returnObject



current_cache['DFWData'] = {}
@app.route('/DFWData', methods=['GET','POST'])
@cross_origin(origins='*')
@cross_origin(supports_credentials=True)
def getDFWData():
    print(request.get_json())
    if request.get_json().get('placeValue','counties'):
        placeValue = request.get_json().get('placeValue')
        counties = request.get_json().get('counties')
        print("place value DFWdConfirmed", placeValue)
        print(len(counties))
        print("counties---inPy", counties)
    else:
        placeValue = "Texas"
        counties = ["Collin","Dallas","Denton","Ellis","Hood","Hunt","Johnson","Kaufman","Parker","Rockwall","Somervell","Tarrant","Wise"]

    print("Place value DFW=>  ", placeValue)
    returnObject = {}
    returnObject['dfwDataRows'] =[]
    returnObject['dfwDataDeathRows'] =[]

    if current_cache.get('DFWData', None):
        return current_cache['DFWData']

    current_cache['DFWData']['dfwDataRows'] = []
    current_cache['DFWData']['dfwDataDeathRows'] = []

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                for i in range(len(counties)):
                    if counties[i] == row['Admin2']:
                        returnObject['dfwDataRows'].append(row)
                        current_cache['DFWData']['dfwDataRows'].append(row)


    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                for i in range(len(counties)):
                    if counties[i] == row['Admin2']:
                        returnObject['dfwDataDeathRows'].append(row)
                        current_cache['DFWData']['dfwDataDeathRows'].append(row)
    return returnObject

current_cache['hospitalBedInfo'] = {}
@app.route('/hospitalBedInfo', methods=['GET','POST'])
@cross_origin(origins='*')
@cross_origin(supports_credentials=True)
def getDataHospital():
    print(request.get_json())
    if request.get_json().get('placeValue'):
        placeValue = request.get_json().get('placeValue')
        print("place value if", placeValue)
    else:
        placeValue = "Texas"
    print("US => ", placeValue)
    returnObject = {}
    returnObject['USBeds'] = []

    if current_cache.get('hospitalBedInfo', None) and current_cache.get('about', None).get(placeValue, None):
        return current_cache['hospitalBedInfo']
    current_cache['hospitalBedInfo'][placeValue] = {}
    current_cache['hospitalBedInfo'][placeValue]['USBeds'] = []

    with open('Hospitalization_all_locs.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['location_name']:
                returnObject['USBeds'].append(row)
                current_cache['hospitalBedInfo'][placeValue]['USBeds'].append(row)
    return returnObject

if __name__ == '__main__':
    app.run(debug = True)
