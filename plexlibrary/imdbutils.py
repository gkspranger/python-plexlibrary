# -*- coding: utf-8 -*-
"""
IMDB utils module
"""
import datetime
import requests
from lxml import html
from utils import add_years

class IMDb():
    """
    IMDb class
    """
    def __init__(self, tmdb, tvdb):
        self.tmdb = tmdb
        self.tvdb = tvdb

    @classmethod
    def _handle_request(cls, url):
        resp = requests.get(url)
        tree = html.fromstring(resp.content)

        # Dict of the IMDB top 250 ids in order
        titles = tree.xpath("//table[contains(@class, 'chart')]"
                            "//td[@class='titleColumn']/a/text()")
        years = tree.xpath("//table[contains(@class, 'chart')]"
                           "//td[@class='titleColumn']/span/text()")
        ids = tree.xpath("//table[contains(@class, 'chart')]"
                         "//td[@class='ratingColumn']/div//@data-titleid")

        return ids, titles, years

    def add_movies(self, url, movie_list=None, movie_ids=None, max_age=0):
        """
        add movies to your list
        """
        if not movie_list:
            movie_list = []
        if not movie_ids:
            movie_ids = []
        max_date = add_years(max_age * -1)
        print(u"Retrieving the IMDB list: {}".format(url))

        (imdb_ids, imdb_titles, imdb_years) = self._handle_request(url)
        for i, imdb_id in enumerate(imdb_ids):
            # Skip already added movies
            if imdb_id in movie_ids:
                continue

            if self.tmdb:
                tmdb_data = self.tmdb.get_tmdb_from_imdb(imdb_id, 'movie')

            if tmdb_data and tmdb_data['release_date']:
                date = datetime.datetime.strptime(tmdb_data['release_date'],
                                                  '%Y-%m-%d')
            elif imdb_years[i]:
                date = datetime.datetime(int(str(imdb_years[i]).strip("()")),
                                         12, 31)
            else:
                date = datetime.date.today()

            # Skip old movies
            if max_age != 0 and (max_date > date):
                continue
            movie_list.append({
                'id': imdb_id,
                'tmdb_id': tmdb_data['id'] if tmdb_data else None,
                'title': tmdb_data['title'] if tmdb_data else imdb_titles[i],
                'year': date.year,
            })
            movie_ids.append(imdb_id)
            if tmdb_data and tmdb_data['id']:
                movie_ids.append('tmdb' + str(tmdb_data['id']))

        return movie_list, movie_ids

    def add_shows(self, url, show_list=[], show_ids=[], max_age=0):
        """
        add a show to the list of shows
        """
        curyear = datetime.datetime.now().year
        print(u"Retrieving the IMDb list: {}".format(url))
        data = {}
        if max_age != 0:
            data['extended'] = 'full'
        (imdb_ids, imdb_titles, imdb_years) = self._handle_request(url)
        for i, imdb_id in enumerate(imdb_ids):
            # Skip already added shows
            if imdb_id in show_ids:
                continue

            tvdb_data = self._get_tvdb_data(imdb_id)
            tmdb_data = self._get_tmdb_data(imdb_id)
            year = self._get_show_year(tvdb_data, tmdb_data, imdb_years[i])

            # Skip old shows
            if max_age != 0 and (curyear - (max_age - 1)) > year:
                continue

            title = self._get_show_title(tvdb_data, tmdb_data, imdb_titles[i])

            show_list.append({
                'id': imdb_id,
                'tvdb_id': tvdb_data['id'] if tvdb_data else None,
                'tmdb_id': tmdb_data['id'] if tmdb_data else None,
                'title': title,
                'year': year,
            })
            show_ids.append(imdb_id)
            if tmdb_data and tmdb_data['id']:
                show_ids.append('tmdb' + str(tmdb_data['id']))
            if tvdb_data and tvdb_data['id']:
                show_ids.append('tvdb' + str(tvdb_data['id']))

        return show_list, show_ids

    def _get_tvdb_data(self, imdb_id):
        tvdb_data = None

        if self.tvdb:
            tvdb_data = self.tvdb.get_tvdb_from_imdb(imdb_id)

        return tvdb_data

    def _get_tmdb_data(self, imdb_id):
        tmdb_data = None

        if self.tmdb:
            tmdb_data = self.tmdb.get_tmdb_from_imdb(imdb_id, 'tv')

        return tmdb_data

    @classmethod
    def _get_show_year(cls, tvdb_data, tmdb_data, imdb_years):
        if tvdb_data and tvdb_data['firstAired'] != "":
            year = datetime.datetime.strptime( \
                tvdb_data['firstAired'], '%Y-%m-%d').year
        elif tmdb_data and tmdb_data['first_air_date'] != "":
            year = datetime.datetime.strptime( \
                tmdb_data['first_air_date'], '%Y-%m-%d').year
        elif imdb_years:
            year = str(imdb_years).strip("()")
        else:
            year = datetime.date.today().year

        return year

    @classmethod
    def _get_show_title(cls, tvdb_data, tmdb_data, imdb_titles):
        if tvdb_data:
            title = tvdb_data['seriesName']
        elif tmdb_data:
            title = tmdb_data['name']
        else:
            title = imdb_titles

        return title

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
