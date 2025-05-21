from App.view.resources.utility.srcs import BED, BOOK_BIBLE, BOOK, CART, CROSS, DUMBBELL, FOOD_DINNER, SLEEP_MOON, UNTENSILS, WORKOUT
from App.view.resources.utility.colors import CTHEME_1

import random

NAMES = ['Food', 'WorkOut', 'Sleep', 'Read', 'Curch', 'Dinner']
BACKGROUNDS = [None, '#ffd366', '#ff0000', '#6141ac', '#c7d0d8', '#316832', '#1358d0']
SOURCES = [BED, BOOK_BIBLE, BOOK, CART, CROSS, DUMBBELL, FOOD_DINNER, SLEEP_MOON, UNTENSILS, WORKOUT]

#icons in taskcreator:
def get_radon_icon(function):
    random_name = random.choice(NAMES)
    random_colors = random.choice(BACKGROUNDS)
    random_src = random.choice(SOURCES)

    # icon(self, color, src, name):
    return function(random_colors, random_src, random_name)

#icons2 in taskcreator:
def get_radon_icon2(function):
    random_src = random.choice(SOURCES)

    # icon2(self, src, name=None):
    return function(random_src)