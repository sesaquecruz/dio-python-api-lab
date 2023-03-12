FROM python:3.10.6-slim

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/pyhton/app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]

EXPOSE 8000
