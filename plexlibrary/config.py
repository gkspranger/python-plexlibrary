# -*- coding: utf-8 -*-
"""
Config module
"""
import os

from utils import YAMLBase

class ConfigParser(YAMLBase):
    """
    ConfigParser Class
    """
    def __init__(self, filepath=None):
        if not filepath:
            parent_dir = (os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.path.pardir)))
            filepath = os.path.join(parent_dir, 'config.yml')

        super(ConfigParser, self).__init__(filepath)
