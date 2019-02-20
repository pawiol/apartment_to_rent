#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import re

from bs4 import BeautifulSoup
from scrapper_helpers.utils import finder

import domporta
import domporta.utils


@finder(many=True, class_='features__item',)
def get_offer_features(item, *args, **kwargs):
    """ Parse information about numbers of rooms
    :param item: Tag html found by finder in html markup
    :return: Number of rooms or None if information not given
    :rtype: int, None
    """
    features = dict()

    for i,x in enumerate(item):

        f_name = x.find('dt', {"class": 'features__item_name'})
        f_value = x.find('dd', {"class": 'features__item_value'})

        try:
            if 'typ budynku' in f_name.text.lower():
                features['house_type'] = f_value.text.strip()
            elif 'materiał' in f_name.text.lower():
                features['house_fabric'] = f_value.text.strip()
            elif 'liczba pokoi' in f_name.text.lower():
                features['number_of_rooms'] = f_value.text.strip()
            elif 'liczba pięter' in f_name.text.lower():
                features['number_of_floors'] = f_value.text.strip()
            else:
                pass
        except:
            pass

    return features

    #     return None
    # return int(item.find_next_sibling().text)


@finder(many=False, class_='detail-feature__name', text='Piętro: ')
def get_floor_for_offer(item, *args, **kwargs):
    """ Parse information about number of the floor
    :param item: Tag html found by finder in html markup
    :return: Number of the floor or None if information not given
    :rtype: int, None
    """
    if not item:
        return None
    floor = item.find_next_sibling().text
    return int(floor) if floor != 'Parter' else 0


@finder(many=True, class_='gallery__item gallery__item_cover gallery__item--small js-gallery__item--open js-gallery__item--small')
def get_images_for_offer(items, *args, **kwargs):
    """ Parse images from offer
    :param item: Tag html found by finder in html markup
    :return: List of image urls
    :rtype: list
    """
    images_links = []

    if items:

        for item in items:

            if item['style'] and 'url' in item['style']:
                try:
                    get_url = re.search(r'url\((.*)\)', str(item['style']))
                    images_links.append(get_url.group(1))
                except:
                    pass

    return images_links


@finder(many=False, class_='details-description__full')
def get_description_for_offer(item, *args, **kwargs):
    """ Parse description of offer
    :param item: Tag html found by finder in html markup
    :return: description of offer
    :rtype: str
    """
    return item.text


def get_meta_data(markup):
    """ Parse meta data
    :param markup: raw html
    :return: dictionary with data
    :rtype: dict
    """
    data = str(markup).split('setContactFormData(')[1].split(');')[0]
    data = json.loads(data)
    return data


def get_gps_data(content):
    """ Parse latitude and longitude
    :param content: raw html
    :return: list with geographical coordinates or None if can't find
    :rtype: list
    """
    try:
        return str(content).split('showMapDialog(')[1].split(')')[0].split(', ')[:2]
    except IndexError:
        return None

def get_offer_details(content):

    html_parser = BeautifulSoup(content, "html.parser")
    scripts = html_parser.find_all('script')

    for script in scripts:
        try:
            if "userHash" in script.string:
                data = script.string
                break
        except TypeError:
            continue
    # print((re.split('dataLayer = |;', data))[2].replace("userHash != null && userHash != '' ? userHash : ''",'""').replace("'", '"'))
    try:
        data_dict = json.loads((re.split('dataLayer = |;', data))[2].replace("userHash != null && userHash != '' ? userHash : ''",'""').replace("'", '"'))
    except json.JSONDecodeError as e:
        print('nie udalo sie')
        return None
    return data_dict



def get_offer_data(url):
    """ Parse details about given offer
    :param url: Url to offer web page
    :type url: str
    :return: Details about given offer
    :rtype: dict
    """
    print(url)
    content = domporta.utils.get_content_from_source('http://www.domiporta.pl' + url)
    markup = BeautifulSoup(content, 'html.parser')
    find_offer_details = get_offer_details(content)
    find_offer_features = get_offer_features(markup)

    offer_details = {
        'market': find_offer_details[0].get('market', None),
        'page_type': find_offer_details[0].get('pageType', None),
        'web': find_offer_details[0].get('web', None),
        'advert_id': find_offer_details[0].get('advertId', None),
        'advertiser_type': find_offer_details[0].get('advertiserType', None),
        'advertiser_id': find_offer_details[0].get('advertiserId', None),
        'category': find_offer_details[0].get('category', None),
        'transaction_type': find_offer_details[0].get('transactionType', None),
        'region': find_offer_details[0].get('region', None),
        'city': find_offer_details[0].get('city', None),
        'district': find_offer_details[0].get('district', None),
        'advertType': find_offer_details[0].get('advertType', None),
        'price': find_offer_details[0].get('price', None),
        'surface': find_offer_details[0].get('surface', None),
        'house_type': find_offer_features.get('house_type', None),
        'house_fabric': find_offer_features.get('house_fabric', None),
        'number_of_rooms': find_offer_features.get('number_of_rooms', None),
        'number_of_floors': find_offer_features.get('number_of_floors', None),
        'url': url,
        'photos_url': get_images_for_offer(markup)
    }

    return offer_details