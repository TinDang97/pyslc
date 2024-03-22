FROM postgres:15.5-bookworm
# Set the pgvector version
ARG PGVECTOR_VERSION=0.5.1
ARG POSTGRES_DATABASE=postgres
ARG POSTGRES_SCHEMA=postgres
ARG POSTGRES_USER=postgres
ARG POSTGRES_PASSWORD=postgres

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        build-essential \
        curl \
        postgresql-server-dev-15

RUN echo "CREATE USER IF NOT EXISTS ${POSTGRES_USER};  \
    CREATE DATABASE IF NOT EXISTS ${POSTGRES_DATABASE};  \
    CREATE SCHEMA AUTHORIZATION IF NOT EXISTS ${POSTGRES_SCHEMA};  \
    ALTER USER ${USER} WITH PASSWORD '${POSTGRES_PASSWORD}';  \
    GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DATABASE} TO ${POSTGRES_USER};"  \
    > /docker-entrypoint-initdb.d/init.sql

# Download and extract the pgvector release, build the extension, and install it.
RUN curl -f -L -o pgvector.tar.gz "https://github.com/pgvector/pgvector/archive/refs/tags/v${PGVECTOR_VERSION}.tar.gz" && \
    tar -xzf pgvector.tar.gz && \
    cd "pgvector-${PGVECTOR_VERSION}" && \
    make OPTFLAGS="" && \
    make install && \
    mkdir -p /usr/share/doc/pgvector && \
    cp LICENSE README.md /usr/share/doc/pgvector


# Clean up build dependencies and temporary files
RUN apt-get remove -y build-essential curl postgresql-server-dev-15 && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /pgvector.tar.gz /pgvector-${PGVECTOR_VERSION}
