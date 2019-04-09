FROM ubuntu:16.04

ENV GOSU_VERSION 1.9
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates wget \
 && wget -O /usr/local/bin/gosu \
        "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-$(dpkg --print-architecture)" \
 && wget -O /usr/local/bin/gosu.asc \
        "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-$(dpkg --print-architecture).asc" \
 && chmod +x /usr/local/bin/gosu \
 && gosu nobody true \
 && apt-get auto-remove -y wget \
 && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]



