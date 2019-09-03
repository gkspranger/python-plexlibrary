# -*- coding: utf-8 -*-
"""
TraktUtils module
"""
import datetime
import json

import requests
import trakt

from utils import add_years

class Trakt():
    """
    Trakt class
    """
    def __init__(self, username, client_id='', client_secret='',
                 oauth_token='', oauth=False, config=None):
        self.config = config
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth_token
        self.oauth = oauth
        if oauth:
            if not self.oauth_token:
                self.oauth_auth()
        else:
            trakt.core.pin_auth(username, client_id=client_id,
                                client_secret=client_secret)
        self.trakt = trakt
        self.trakt_core = trakt.core.Core()

    def oauth_auth(self):
        """
        verify authentication via oauth
        """
        store = False
        self.oauth_token = trakt.core.oauth_auth(
            self.username, client_id=self.client_id,
            client_secret=self.client_secret, store=store)
        # Write to the file
        if self.config:
            self.config['trakt']['oauth_token'] = self.oauth_token
            self.config.save()
            print(u"Added new OAuth token to the config file under trakt:")
            print(u"    oauth_token: '{}'".format(self.oauth_token))

    def _handle_request(self, method, url, data=None):
        """Stolen from trakt.core to support optional OAUTH operations
        :todo: Fix trakt
        """
        headers = {'Content-Type': 'application/json',
                   'trakt-api-version': '2'}
        # self.logger.debug('%s: %s', method, url)
        headers['trakt-api-key'] = self.client_id
        if self.oauth:
            headers['Authorization'] = 'Bearer {0}'.format(self.oauth_token)
        # self.logger.debug('headers: %s', str(headers))
        # self.logger.debug('method, url :: %s, %s', method, url)
        if method == 'get':  # GETs need to pass data as params, not body
            response = requests.request(method, url, params=data,
                                        headers=headers)
        else:
            response = requests.request(method, url, data=json.dumps(data),
                                        headers=headers)
        # self.logger.debug('RESPONSE [%s] (%s): %s',
        #     method, url, str(response))
        if response.status_code in self.trakt_core.error_map:
            if response.status_code == \
                    trakt.core.errors.OAuthException.http_code:
                # OAuth token probably expired
                print(u"Trakt OAuth token invalid/expired")
                self.oauth_auth()
                return self._handle_request(method, url, data)
            raise self.trakt_core.error_map[response.status_code]()
        if response.status_code == 204:  # HTTP no content
            return None

        return json.loads(response.content.decode('UTF-8', 'ignore'))

    def add_movies(self, url, movie_list=[], movie_ids=[], max_age=0):
        """
        add movies to list
        """
        max_date = add_years(max_age * -1)
        print(u"Retrieving the trakt list: {}".format(url))
        data = {}
        if max_age != 0:
            data['extended'] = 'full'
        movie_data = self._handle_request('get', url, data=data)
        for meta in movie_data:
            if 'movie' not in meta:
                meta['movie'] = meta
            # Skip already added movies
            if meta['movie']['ids']['imdb'] in movie_ids:
                continue
            if not meta['movie']['year']:
                continue
            # Skip old movies
            if max_age != 0 \
                    and (max_date > datetime.datetime.strptime(
                            meta['movie']['released'], '%Y-%m-%d')):
                continue
            movie_list.append({
                'id': meta['movie']['ids']['imdb'],
                'tmdb_id': meta['movie']['ids'].get('tmdb', ''),
                'title': meta['movie']['title'],
                'year': meta['movie']['year'],
            })
            movie_ids.append(meta['movie']['ids']['imdb'])
            if meta['movie']['ids'].get('tmdb'):
                movie_ids.append('tmdb' + str(meta['movie']['ids']['tmdb']))

        return movie_list, movie_ids

    def add_shows(self, url, show_list=[], show_ids=[], max_age=0):
        """
        add shows to list
        """
        curyear = datetime.datetime.now().year
        print(u"Retrieving the trakt list: {}".format(url))
        data = {}
        if max_age != 0:
            data['extended'] = 'full'
        show_data = self._handle_request('get', url, data=data)
        for meta in show_data:
            if 'show' not in meta:
                meta['show'] = meta
            # Skip already added shows
            if meta['show']['ids']['imdb'] in show_ids:
                continue
            if not meta['show']['year']:
                continue
            # Skip old shows
            if max_age != 0 \
                    and (curyear - (max_age - 1)) > int(meta['show']['year']):
                continue
            show_list.append({
                'id': meta['show']['ids']['imdb'],
                'tmdb_id': meta['show']['ids'].get('tmdb', ''),
                'tvdb_id': meta['show']['ids'].get('tvdb', ''),
                'title': meta['show']['title'],
                'year': meta['show']['year'],
            })
            show_ids.append(meta['show']['ids']['imdb'])
            if meta['show']['ids'].get('tmdb'):
                show_ids.append('tmdb' + str(meta['show']['ids']['tmdb']))
            if meta['show']['ids'].get('tvdb'):
                show_ids.append('tvdb' + str(meta['show']['ids']['tvdb']))
        return show_list, show_ids

    def add_items(self, item_type, url, item_list=None, item_ids=None,
                  max_age=0):
        """
        add items to the list
        """
        if item_type == 'movie':
            return self.add_movies(url, movie_list=item_list,
                                   movie_ids=item_ids, max_age=max_age)
        if item_type == 'tv':
            return self.add_shows(url, show_list=item_list,
                                  show_ids=item_ids, max_age=max_age)
        return None
