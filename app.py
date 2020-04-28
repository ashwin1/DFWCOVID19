from flask import Flask, render_template
#from data import Articles
from flask_cors import CORS, cross_origin
import csv
from flask import render_template, url_for, request, redirect

# current_cache = {}

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


# @app.route('/about')
# def getData(county = 'Austin'):
#     with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
#             datareader = csv.DictReader(csvfile)
#             for row in datareader:
#                 #print(row['Admin2'])
#                 if county == row['Admin2']:
#                     return {'confirmed':row,
#                     'deaths':{'4/4/20':'32'},
#                     'recovered':{'4/4/20':'12'}}
#             return 'no data found'
 # bring all the 3 deaths and recovered csvs and fetch the data


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
    print("Place value => ", placeValue)
    returnObject = {}
    # if current_cache.get('about', None):
        # return current_cache['about']
    # current_cache['about'] = {}
    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Admin2']:
                returnObject['confirmed'] = row
                # current_cache['about']['confirmed'] = row
    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Admin2']:
                returnObject['deaths'] = row
                # current_cache['about']['deaths'] = row
    # with open('RECOVERED FILE NAME.csv', newline='') as csvfile:
    #     datareader = csv.DictReader(csvfile)
    #     for row in datareader:
    #         if county == row['Admin2']:
    #             returnObject['recovered'] = row
    #             break
    return returnObject

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


    # if current_cache.get('texasData', None):
    #     return current_cache['texasData']
    # current_cache['texasData'] = {}
    # current_cache['texasData']['texasDataRows'] = []
    # current_cache['texasData']['texasDeathsCardRow'] = []

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                returnObject['texasDataRows'].append(row)
                # current_cache['texasData']['texasDataRows'].append(row)

    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                returnObject['texasDeathsCardRow'].append(row)
                # current_cache['texasData']['texasDeathsCardRow'].append(row)

        # with open('Hospitalization_all_locs.csv', newline='') as csvfile:
        #     datareader = csv.DictReader(csvfile)
        #     for row in datareader:
        #         if placeValue == row['location']:
        #             returnObject['USBeds'].append(row)

    # with open('RECOVERED FILE NAME.csv', newline='') as csvfile:
    #     datareader = csv.DictReader(csvfile)
    #     for row in datareader:
    #         if county == row['Admin2']:
    #             returnObject['recovered'] = row
    #             break
    return returnObject

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
    #
    # if current_cache.get('DFWData', None):
    #     return current_cache['DFWData']
    # current_cache['DFWData'] = {}
    # current_cache['DFWData']['dfwDataRows'] = []
    # current_cache['DFWData']['dfwDataDeathRows'] = []

    with open('time_series_covid19_confirmed_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                for i in range(len(counties)):
                    if counties[i] == row['Admin2']:
                        returnObject['dfwDataRows'].append(row)
                        # current_cache['DFWData']['dfwDataRows'].append(row)


    with open('time_series_covid19_deaths_US.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['Province_State']:
                for i in range(len(counties)):
                    if counties[i] == row['Admin2']:
                        returnObject['dfwDataDeathRows'].append(row)
                        # current_cache['DFWData']['dfwDataDeathRows'].append(row)
    return returnObject

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

    # if current_cache.get('hospitalBedInfo', None):
    #     return current_cache['hospitalBedInfo']
    # current_cache['hospitalBedInfo'] = {}
    # current_cache['hospitalBedInfo']['USBeds'] = []

    with open('Hospitalization_all_locs.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if placeValue == row['location_name']:
                returnObject['USBeds'].append(row)
                # current_cache['hospitalBedInfo']['USBeds'].append(row)
    return returnObject

if __name__ == '__main__':
    app.run(debug = True)
