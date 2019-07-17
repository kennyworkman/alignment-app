FROM python:3.7
ADD . /alignment-app
WORKDIR /alignment-app

RUN pip install -r requirements.txt
# Instantiate the sqlite3 database
RUN flask init-db



CMD ["gunicorn", "--workers", "3", "--bind", "unix:alignment.sock", "-m", "007", "wsgi:app"]
