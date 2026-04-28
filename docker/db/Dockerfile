FROM postgres:16

ARG DEMO_DB_URL=https://edu.postgrespro.com/demo-small-en.zip

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl unzip ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/demodb /docker-entrypoint-initdb.d \
    && curl -L "$DEMO_DB_URL" -o /tmp/demodb/demo-small-en.zip \
    && unzip /tmp/demodb/demo-small-en.zip -d /tmp/demodb/unpacked \
    && SQL_FILE=$(find /tmp/demodb/unpacked -type f \( -name "*.sql" -o -name "*.sql.gz" \) | head -n 1) \
    && if [ -z "$SQL_FILE" ]; then echo "SQL dump not found in archive"; exit 1; fi \
    && cp "$SQL_FILE" /docker-entrypoint-initdb.d/01-demo.sql$( [ "${SQL_FILE##*.}" = "gz" ] && echo ".gz" ) \
    && rm -rf /tmp/demodb
