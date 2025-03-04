FROM python:3.13-alpine
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

WORKDIR /app

COPY ./requirements.txt tmp/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r tmp/requirements.txt

COPY ./src/ /src/

ARG ARG DEV=false
COPY requirements.dev.txt /tmp/requirements.dev.txt
COPY tests/ tests/
RUN if [ $DEV = "true" ]; \
    then pip install --no-cache-dir -r /tmp/requirements.dev.txt ; \
else \
    rm -rf /tmp/requirements.dev.txt tests/; \
fi

CMD ["python", "main.py"]
