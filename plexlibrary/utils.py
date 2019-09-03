# -*- coding: utf-8 -*-
"""
The Utils Module
"""
from datetime import datetime

import ruamel.yaml

class Colors():
    """
    Colors class
    """
    RED = u'\033[1;31m'
    BLUE = u'\033[1;34m'
    CYAN = u'\033[1;36m'
    GREEN = u'\033[0;32m'
    RESET = u'\033[0;0m'
    BOLD = u'\033[;1m'
    REVERSE = u'\033[;7m'


class YAMLBase():
    """
    YAMLBase class
    """
    def __init__(self, filename):
        self.filename = filename

        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open(self.filename, 'r') as myfile:
            try:
                self.data = yaml.load(myfile)
            except ruamel.yaml.YAMLError as err:
                raise err

    def __getitem__(self, k):
        return self.data[k]

    def __iter__(self):
        return self.data.itervalues()

    def __setitem__(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        """
        get the media item
        """
        if key in self.data:
            return self.data[key]

        return default

    def save(self):
        """
        save the changes you just made
        """
        yaml = ruamel.yaml.YAML()
        with open(self.filename, 'w') as myfile:
            yaml.dump(self.data, myfile)

def add_years(years, from_date=None):
    """
    include the years you want to search
    """
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year + years)
    except ValueError:
        # Must be 2/29!
        return from_date.replace(month=2, day=28,
                                 year=from_date.year + years)
