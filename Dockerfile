FROM python:3.7

# The way that docker copy works demands seperate layers for each directory.
COPY README.md requirements.txt setup.py .env wsgi.py /alignment-app/
COPY instance/config.py /alignment-app/instance/config.py
COPY tests/*.py /alignment-app/tests/
COPY alignment /alignment-app/alignment
WORKDIR /alignment-app

# Download precompiled binary and make it executable.
RUN curl -L http://www.clustal.org/omega/clustalo-1.2.4-Ubuntu-x86_64 > /bin/clustalo &&\
  chmod +x /bin/clustalo

RUN pip install -r requirements.txt

# Instantiate the sqlite3 database.
RUN flask init-db

# Build project as package for testing.
# Make sure tests work in built container.
RUN pip install -e . &&\
    pytest

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "wsgi:app"]
