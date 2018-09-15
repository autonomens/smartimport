FROM python:3
WORKDIR /code
EXPOSE 8080

COPY apt.txt ./
RUN apt install -y $(grep -vE "^\s*#" apt.txt  | tr "\n" " ")
RUN pip install gunicorn

COPY . .

RUN python setup.py install

CMD ["gunicorn", "smartimport.api:app", "--bind=0.0.0.0:8080"]
