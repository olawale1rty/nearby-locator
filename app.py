
import requests
from flask import Flask, render_template, request, url_for, flash, redirect


URL = "https://discover.search.hereapi.com/v1/discover"
api_key = 'W5vIt4K4WgyT4AbocD_1HR6GNJU_TrvV5y1mC9Zw9EY'

app = Flask(__name__)
app.config['SECRET_KEY'] = "2f05980503d030045bf70f6da1a49e78168b6dcf65275637"


@app.route('/', methods=('GET', 'POST'))
def map_func():
    if request.method == 'POST':
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
                    data = r.json()
                    return render_template('map.html',
                                           latitude=latitude,
                                           longitude=longitude,
                                           apikey=api_key,
                                           data=data['items']
                                           )
                else:
                    data = r.json()
                    flash(
                        {
                            'title': data['title'],
                            'cause': data['cause'],
                            'action': data['action'],
                            'status': data['status']
                        }
                    )
        except Exception as e:
            flash(str(e))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
