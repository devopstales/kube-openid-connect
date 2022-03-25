ARG ARCH
FROM ${ARCH}python:3.8-alpine

RUN pip3 install flask requests_oauthlib requests waitress flask_cors pyyaml

ADD server.py /opt/server.py
ADD templates /opt/templates
ADD static /opt/static

RUN addgroup -S -g 10001 server && \
    adduser -S -u 10001 server -G server

RUN chown -R 10001:10001 /opt

USER 10001:10001

CMD python3 /opt/server.py

