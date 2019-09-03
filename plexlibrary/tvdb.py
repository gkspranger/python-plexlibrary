# -*- coding: utf-8 -*-
"""
The TVDB Module
"""
import json
import requests

class TheTVDB():
    """
    The TVDB Class
    """
    token = None

    def __init__(self, username, api_key, user_key):
        self.username = username
        self.api_key = api_key
        self.user_key = user_key

    def get_imdb_id(self, tvdb_id):
        """
        get item's IMDB ID
        """
        if not self.token:
            self._refresh_token()

        url = "https://api.thetvdb.com/series/{tvdb_id}".format(
            tvdb_id=tvdb_id)
        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.token)
        }
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            tv_show = resp.json()
            return tv_show['data']['imdbId']

        return None

    def _refresh_token(self):
        data = {
            'apikey': self.api_key,
            'userkey': self.user_key,
            'username': self.username,
        }

        url = "https://api.thetvdb.com/login"
        resp = requests.post(url, json=data)

        if resp.status_code == 200:
            result = resp.json()
            self.token = result['token']

    def get_tvdb_from_imdb(self, imdb_id):
        """
        get item's TVDB ID from IMDB
        """
        if not self.token:
            self._refresh_token()

        params = {
            'imdbId': imdb_id
        }

        url = "https://api.thetvdb.com/search/series"
        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.token)
        }
        resp = requests.get(url, headers=headers, params=params)

        if resp.status_code == 200:
            item = json.loads(resp.text)
            return item.get('data')[0] if item and item.get('data') else None

        return None
