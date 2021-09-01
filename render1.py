#!/usr/bin/env python3

import json
import locale
import glob
import os

from staticjinja import Site


def format_price(value):
    if value is None or not isinstance(value, int):
        return value

    formatted_price=f'{value:n}'.replace(",", " ")
    return formatted_price


filters = {
    'format_price': format_price,
}
def collect_data_filepaths(directory_path='data', ):
    for file in os.listdir(directory_path):
        if file.endswith(".json"):
            yield os.path.join(directory_path, file)


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    data_filepaths = list(collect_data_filepaths())
    items = []
    for filename in data_filepaths:
        with open('data/item71_multicook.json', 'r') as file:
            site_market = json.loads(file.read())
            items.extend(site_market)
            count_items=len(items)


    site = Site.make_site(env_globals={
        'items': items,
        'count_items':count_items

    }, filters = filters)
    site.render(use_reloader=True)
