FROM python:3.9.7-slim-buster

WORKDIR /usr/src/app
# ENV DIR=/usr/local/bin/

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3550

# gunicorn --bind 0.0.0.0:5000 wsgi:app
CMD [ "gunicorn", "--bind", "0.0.0.0:3550", "wsgi:app" ]
