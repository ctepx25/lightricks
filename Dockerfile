FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV OBSERVABILITY_ENDPOINT="https://pub-6c2184153f6d479eacc33cee5c12ce64.r2.dev/payload"
ENV CORALOGIX_ENDPOINT="https://ingress.eu2.coralogix.com/logs/v1/bulk"
ENV CORALOGIX_SUBSYSTEM_NAME="logs"
ENV INFULXDB_ENDPOINT="eu-central-1-1.aws.cloud2.influxdata.com"
ENV INFLUXDB_DATABASE="lightricks"

RUN echo "OBSERVABILITY_ENDPOINT: $OBSERVABILITY_ENDPOINT"
RUN echo "CORALOGIX_ENDPOINT: $CORALOGIX_ENDPOINT"
RUN echo "CORALOGIX_SUBSYSTEM_NAME: $CORALOGIX_SUBSYSTEM_NAME"
RUN echo "INFULXDB_ENDPOINT: $INFULXDB_ENDPOINT"
RUN echo "INFLUXDB_DATABASE: $INFLUXDB_DATABASE"

CMD [ "python", "./observability_data.py" ]
