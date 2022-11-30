FROM alpine:3.16.2
RUN apk add --no-cache python3 py3-pip
WORKDIR /app/
RUN pip3 install boto3
COPY process-files.py .
CMD [ "python3","process-files.py" ]
