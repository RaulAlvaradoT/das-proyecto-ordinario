FROM python:3.9.7

WORKDIR /flask_app_code
ADD . /flask_app_code

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
