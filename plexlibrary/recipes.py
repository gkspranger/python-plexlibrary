# -*- coding: utf-8 -*-
"""
recipes module
"""
import glob
import os

from utils import YAMLBase


class RecipeParser(YAMLBase):
    """
    RecipeParser class
    """
    def __init__(self, name, directory=None):
        self.name = os.path.splitext(name)[0]
        recipe_file = self.name + '.yml'
        if not directory:
            parent_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.path.pardir))
            directory = os.path.join(parent_dir, 'recipes')

        filepath = os.path.join(directory, recipe_file)

        super(RecipeParser, self).__init__(filepath)

    def dump(self):
        """
        show all the data we have
        """
        print(self.data)


def get_recipes(directory=None):
    """
    get all valid recipes
    """
    if not directory:
        parent_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir))
        directory = os.path.join(parent_dir, 'recipes')

    recipes = []
    for path in glob.glob(os.path.join(directory, '*.yml')):
        _, filename = os.path.split(path)
        recipe_name = os.path.splitext(filename)[0]
        recipes.append(recipe_name)
    recipes.sort()

    return recipes
