FROM python:3.9

WORKDIR /app

COPY ./csvutil.py .
COPY ./constants.py .
COPY ./isoform_mapper.py .
COPY ./run-isoform-mapper.py .
COPY ./requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

RUN mkdir -p /data


