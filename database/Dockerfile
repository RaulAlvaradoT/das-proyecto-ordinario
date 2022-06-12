FROM python:3.9.7

WORKDIR /mongo_database
ADD . /mongo_database

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "mongo_db.py"]
