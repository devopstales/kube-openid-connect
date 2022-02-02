ARG ARCH
FROM ${ARCH}python:3.8-alpine

RUN pip3 install flask requests_oauthlib requests waitress flask_cors pyyaml

COPY server.py /server.py

RUN addgroup -S -g 10001 server && \
    adduser -S -u 10001 server -G server

USER 10001:10001

CMD python3 /server.py --log-format=full

