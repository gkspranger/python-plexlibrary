FROM python:3.7-stretch

WORKDIR /plex

COPY requirements.txt /plex/requirements.txt

RUN /usr/local/bin/pip install -r /plex/requirements.txt

COPY config.example.yml /plex/config.example.yml
COPY recipes/ /plex/recipes/
COPY plexlibrary/ /plex/plexlibrary/

ENTRYPOINT ["/usr/local/bin/python", "plexlibrary"]

CMD ["--help"]
