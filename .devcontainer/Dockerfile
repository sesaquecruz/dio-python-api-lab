FROM python:3.10.6-slim

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/pyhton/app

RUN pip install pipenv

ENV PIPENV_VENV_IN_PROJECT=true

CMD ["tail", "-f", "/dev/null"]

EXPOSE 8000
