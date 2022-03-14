FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -U pip

RUN pip3 install -r requirements.txt

COPY /ppr_project .

CMD ["gunicorn", "ppr_project.wsgi:application", "--bind", "0:8000"]
