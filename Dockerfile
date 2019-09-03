FROM python:3.7-stretch

WORKDIR /plex

COPY requirements.txt /plex/requirements.txt

RUN /usr/local/bin/pip install -r /plex/requirements.txt

COPY recipes/ /plex/recipes/
COPY plexlibrary/ /plex/plexlibrary/

CMD ["/bin/bash"]
