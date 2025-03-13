FROM python:3.13-alpine
LABEL org.opencontainers.image.authors="Hiago <https://github.com/HiagoAC>"

WORKDIR /app

COPY ./requirements.txt tmp/requirements.txt

RUN pip install --upgrade pip
RUN apk update && apk add --no-cache bash
RUN pip install --no-cache-dir -r tmp/requirements.txt

COPY ./src/ /app/src/

ARG ARG DEV=false
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./.env /app/.env
COPY tests/ tests/
RUN if [ $DEV = "true" ]; \
    then pip install --no-cache-dir -r /tmp/requirements.dev.txt ; \
else \
    rm -rf /tmp/requirements.dev.txt tests/ .env; \
fi

RUN addgroup -S nonroot \
    && adduser -S nonroot -G nonroot \
    && chown -R nonroot:nonroot /app \
    && chmod -R 755 /app
USER nonroot

CMD ["python", "main.py"]
