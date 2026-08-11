FROM python:3-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ADD . /pwdgrpd
RUN apk update && apk upgrade
RUN mkdir /wheels
RUN pip wheel \
	--no-cache-dir \
	--wheel-dir /wheels \
	--prefer-binary \
	/pwdgrpd

FROM python:3-alpine AS product
RUN --mount=type=cache,target=/var/cache/apk \
	apk update && apk upgrade
RUN --mount=type=bind,source=/wheels,target=/wheels,from=app-builder \
	pip install --no-cache --no-index /wheels/*
CMD ["pwdgrpd"]
