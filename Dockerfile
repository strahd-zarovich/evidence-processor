FROM debian:stable-slim

ARG VERSION=0.0.1
LABEL version="${VERSION}"

# UnRAID-friendly defaults
ENV PUID=99 \
    PGID=100 \
    EP_CONFIG=/data/config/config.yaml

WORKDIR /app

# Core runtime
RUN apt-get update && apt-get install -y \
    bash \
    python3 \
    python3-pip \
    python3-yaml \
    python3-pymysql \
    python3-dotenv \
    mariadb-client \
    gosu \
  && rm -rf /var/lib/apt/lists/*

# App files
COPY entrypoint.sh /app/
COPY scripts/ /app/scripts/
COPY defaults/ /app/defaults/

RUN chmod -R a+rX /app && \
    chmod +x /app/entrypoint.sh && \
    find /app/scripts -type f -exec chmod +x {} \; && \
    find /app/defaults -type f -name "*.sh" -exec chmod +x {} \; && \
    chown -R ${PUID}:${PGID} /app

VOLUME ["/data", "/tmp"]

ENTRYPOINT ["/app/entrypoint.sh"]