FROM python:3.11.3-slim-bullseye
RUN adduser --disabled-password --gecos "" anna-api && \
    chown -R anna-api /home/anna-api
USER anna-api
WORKDIR /home/anna-api
COPY requirements.txt requirements.txt
RUN pip install --no-warn-script-location -r requirements.txt
COPY . .
CMD ["python", "run.py"]