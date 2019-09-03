FROM python:3.7-stretch

WORKDIR /plex

COPY requirements.txt /plex/requirements.txt

RUN /usr/local/bin/pip install -r /plex/requirements.txt

# templating binary
COPY bin/confd /usr/local/bin/confd

# example configuration
COPY config.example.yml /plex/config.yml

# example recipes
COPY recipes/ /plex/recipes/

# pylint configuration file
COPY pylintrc /plex/pylintrc

# makefile
COPY Makefile /plex/Makefile

# source code
COPY plexlibrary/ /plex/plexlibrary/

RUN /usr/bin/make checklist

ENTRYPOINT ["/usr/local/bin/python", "plexlibrary"]

CMD ["--help"]
