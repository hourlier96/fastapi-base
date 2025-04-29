FROM python:3.13-alpine AS builder

LABEL MAINTAINER="fr.dgc.ops.dgtl@devoteamgcloud.com"

RUN pip install --no-cache-dir uv

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN uv pip compile pyproject.toml --extra dev -o requirements.txt

# ------------------------

FROM python:3.13-alpine

RUN addgroup -S appgroup && adduser -S -s /bin/ash appuser -G appgroup

# bash installed to make pre-commit runnable
RUN apk update && apk add --no-cache git bash

WORKDIR /home/appuser/code

COPY --from=builder /tmp/requirements.txt /home/appuser/code/requirements.txt

# Use pip to avoid install uv in image
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /home/appuser/code/requirements.txt

RUN chown -R appuser:appgroup /home/appuser/code

USER appuser

COPY --chown=appuser:appgroup ./ /home/appuser/code/

EXPOSE 8000
EXPOSE 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]