
from whitenoise import WhiteNoise
import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, flash, redirect
import logging

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")

URL = "https://discover.search.hereapi.com/v1/discover"
api_key = os.environ.get('API_KEY')

# Set log level
logging.getLogger().setLevel(logging.DEBUG)


@app.route('/', methods=('GET', 'POST'))
def map_func():
    if request.method == 'POST':
        logging.info('REQUEST: POST -> /')
        try:
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            query = request.form['query']
            limit = request.form['limit']

            if not latitude:
                flash('Latitude is required!')
            elif not longitude:
                flash('Longitude is required!')
            elif not query:
                flash('Query is required!')
            elif not limit:
                flash('Limit is required!')
            else:
                PARAMS = {
                    'apikey': api_key,
                    'q': query,
                    'limit': limit,
                    'at': '{},{}'.format(latitude, longitude)
                }

                # sending get request and saving the response as response object
                r = requests.get(url=URL, params=PARAMS)
                if r.status_code == 200:
                    logging.info('::: REQUEST STATUS 200 :::')
                    data = r.json()
                    return render_template('map.html',
                                           latitude=latitude,
                                           longitude=longitude,
                                           apikey=api_key,
                                           data=data['items']
                                           )
                else:
                    data = r.json()
                    logging.error(
                        '::: ERROR REQUEST STATUS NOT 200 :::')
                    logging.error('ERROR >>> {}'.format({
                        'title': data['title'],
                        'cause': data['cause'],
                        'action': data['action'],
                        'status': data['status']
                    }))
                    flash(
                        {
                            'title': data['title'],
                            'cause': data['cause'],
                            'action': data['action'],
                            'status': data['status']
                        }
                    )
        except Exception as e:
            logging.error('::: ERROR DURING POST PROCESSING :::')
            logging.error('ERROR >>> {}'.format(e))
            flash(str(e))
    logging.info('REQUEST: GET -> /')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3055, debug=False)
