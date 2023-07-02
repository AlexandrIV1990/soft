FROM python:3.8

ENV PYTHONUNBUFFERED 1


RUN mkdir -p /code && \
    mkdir -p /code/public/static && \
    mkdir -p /code/public/media

WORKDIR /code

COPY Pipfile Pipfile.lock /code/
COPY app /code/app/

RUN apt-get update && apt-get install -y git python3-pip locales
RUN pip3 install --no-cache-dir pipenv==2022.1.8
RUN pipenv install --system --ignore-pipfile

COPY ./run.sh /code/

CMD ["bash", "/code/run.sh" ]

EXPOSE 8080
