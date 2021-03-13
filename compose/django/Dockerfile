FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements/base.txt

