from otodom.category import get_category as otodom_get_category
from otodom.offer import get_offer_information

from olx import BASE_URL
from olx.category import get_category as olx_get_category
from olx.offer import parse_offer

from domporta.category import get_category as domporta_get_category
from domporta.offer import get_offer_data as domporta_get_offer

import sqlite3
import re
from datetime import date


def get_sql_values(sql_value, previous_sql_value=None):
    """
    Simply converter for sql query;
    Converting input to string and adding some double quotes
    In addition we cut off some strange characters
    :param sql_value: 5
    :param previous_sql_value:
    :return: '"5","
    """
    if previous_sql_value:
        return_sql_value = str(previous_sql_value) + '"' + re.sub('"|\W+', ' ', str(sql_value)) + '",'
    else:
        return_sql_value = '"' + re.sub('"|\W+', ' ', str(sql_value)) + '",'

    return return_sql_value


def get_otodom_apartments():
    """
    Insert new offers to otodom_offers table
    :return: True
    """

    def get_values_from_list(list_, dict_value):
        """
        Searching for dictionary with proper key
        :param list_: list of dictionaries
        :param dict_value: dictionary key
        :return: {'dictionary key': value}
        """
        if len(list_) == 0:
            return ' "' + 'None' + '", '

        for value_ in range(len(list_)):

            if list_[value_].get(dict_value, False):

                return ' "' + str(list_[value_].get(dict_value)) + '", '

            else:

                return ' "' + str(None) + '", '

    sqlite_file = 'apartment_db.db'
    otodom_table = 'otodom_offers'
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()

    column_list = ('offer_title,'
               + ' ' + 'offer_address,'
                + ' ' + 'offer_creator,'
                + ' ' + 'offer_type,'
                + ' ' + 'offer_price,'
                + ' ' + 'offer_currency,'
                + ' ' + 'offer_city,'
                + ' ' + 'offer_district,'
                + ' ' + 'offer_voivodeship,'
                + ' ' + 'offer_geo_data,'
                + ' ' + 'offer_phone_number,'
                + ' ' + 'offer_description,'
                + ' ' + 'offer_id,'
                + ' ' + 'offer_pv,'
                + ' ' + 'offer_add_time,'
                + ' ' + 'offer_update_time,'
                + ' ' + 'offer_photo_links,'
                + ' ' + 'offer_photo_count,'
                + ' ' + 'offer_video,'
                + ' ' + 'offer_facebook_description,'
                + ' ' + 'offer_cookie,'
                + ' ' + 'offer_csrf_token,'
                + ' ' + 'offer_url,'
                + ' ' + 'offer_meta_id,'
                + ' ' + 'offer_meta_type,'
                + ' ' + 'offer_3d_link,'
                + ' ' + 'offer_rent,'
                + ' ' + 'offer_deposit,'
                + ' ' + 'offer_house_type,'
                + ' ' + 'offer_house_fabric,'
                + ' ' + 'offer_windows,'
                + ' ' + 'offer_heating_type,'
                + ' ' + 'offer_house_condition,'
                + ' ' + 'offer_available,'
                + ' ' + 'offer_heating,'
                + ' ' + 'offer_balcony,'
                + ' ' + 'offer_kitchen,'
                + ' ' + 'offer_terrace,'
                + ' ' + 'offer_internet,'
                + ' ' + 'offer_elevator,'
                + ' ' + 'offer_car_parking,'
                + ' ' + 'offer_dis_facilities,'
                + ' ' + 'offer_mezzanine,'
                + ' ' + 'offer_basement,'
                + ' ' + 'offer_duplex,'
                + ' ' + 'offer_garden,'
                + ' ' + 'offer_garage,'
                + ' ' + 'offer_cable_tv,'
                + ' ' + 'offer_surface,'
                + ' ' + 'offer_rooms,'
                + ' ' + 'offer_floor,'
                + ' ' + 'offer_total_floors,'
                + ' ' + 'v_date')

    parsed_category = otodom_get_category("wynajem", "mieszkanie", 'poznan')

    for offer_ in parsed_category:

        cursor.execute('SELECT * FROM {table_} WHERE offer_id={param_}'. \
                  format(table_=otodom_table, param_=str(offer_['offer_my_id'])))

        all_rows = cursor.fetchall()

        if all_rows:
            pass
        else:
            offer_temp_ = get_offer_information(offer_['detail_url'], context=offer_)

            values_text = (get_sql_values(offer_temp_.get('title', 'None'))
                           + get_sql_values(offer_temp_.get('address', 'None'))
                           + get_sql_values(offer_temp_.get('poster_name', 'None'))
                           + get_sql_values(offer_temp_.get('poster_type', 'None'))
                           + get_sql_values(offer_temp_.get('price', 'None'))
                           + get_sql_values(offer_temp_.get('currency', 'None'))
                           + get_sql_values(offer_temp_.get('city', 'None'))
                           + get_sql_values(offer_temp_.get('district', 'None'))
                           + get_sql_values(offer_temp_.get('voivodeship', 'None'))
                           + '"' + str(offer_temp_['geographical_coordinates'][0]) + '|' + str(
                        offer_temp_['geographical_coordinates'][1]) + '"' + ', '
                           + '"' + '|'.join(offer_temp_.get('phone_numbers', ['None'])) + '"' + ', '
                           + get_sql_values(offer_temp_.get('description', 'None'))
                           + get_values_from_list(offer_temp_.get('offer_details', []), 'Nr oferty w Otodom')
                           + get_values_from_list(offer_temp_.get('offer_details', []), 'Liczba wyświetleń strony')
                           + get_values_from_list(offer_temp_.get('offer_details', []), 'Data dodania')
                           + get_values_from_list(offer_temp_.get('offer_details', []), 'Data aktualizacji')
                           + '"' + '|'.join(offer_temp_.get('photo_links', ['None'])) + '"' + ', '
                           + '"' + str(len(offer_temp_.get('photo_links', []))) + '"' + ', '
                           + '"' + offer_temp_.get('video_link', 'None') + '"' + ', '
                           + get_sql_values(offer_temp_.get('facebook_description', 'None'))
                           + '"' + offer_temp_['meta'].get('cookie', 'None') + '"' + ', '
                           + '"' + offer_temp_['meta'].get('csrf_token', 'None') + '"' + ', '
                           + '"' + offer_temp_['meta']['context'].get('detail_url', 'None') + '"' + ', '
                           + get_sql_values(offer_temp_['meta']['context'].get('offer_id', 'None'))
                           + get_sql_values(offer_temp_['meta']['context'].get('poster', 'None'))
                           + '"' + offer_temp_.get('3D_walkaround_link', 'None') + '"' + ', '
                           + re.sub(' |zł', '',
                                    get_values_from_list(offer_temp_.get('apartment_details', []), 'Czynsz - dodatkowo'))
                           + re.sub(' |zł', '', get_values_from_list(offer_temp_.get('apartment_details', []), 'Kaucja'))
                           + get_values_from_list(offer_temp_.get('apartment_details', []), 'Rodzaj zabudowy')
                           + get_values_from_list(offer_temp_.get('apartment_details', []), 'Materiał budynku')
                           + get_values_from_list(offer_temp_.get('apartment_details', []), 'Okna')
                           + get_values_from_list(offer_temp_.get('apartment_details', []), 'Ogrzewanie')
                           + get_values_from_list(offer_temp_.get('apartment_details', []), 'Stan wykończenia')
                           + get_values_from_list(offer_temp_.get('apartment_details', []), 'Dostępne od')
                           + get_sql_values(offer_temp_['additional_assets'].get('heating', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('balcony', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('kitchen', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('terrace', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('internet', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('elevator', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('car_parking', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('disabled_facilities', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('mezzanine', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('basement', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('duplex_apartment', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('garden', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('garage', 'None'))
                           + get_sql_values(offer_temp_['additional_assets'].get('cable_tv', 'None'))
                           + '"' + str(offer_temp_.get('surface', 'None')) + '",'
                           + get_sql_values(offer_temp_.get('rooms', 'None'))
                           + get_sql_values(offer_temp_.get('floor', 'None'))
                           + get_sql_values(offer_temp_.get('total_floors', 'None'))
                           + '"' + str(date.today()) + '"'
                           )

            try:

                cursor.execute("INSERT INTO {table_name} ({table_columns}) VALUES ({table_values})". \
                          format(table_name=otodom_table, table_columns=column_list, table_values=values_text))

                connection.commit()
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(column_list))

    connection.close()

    return True

def get_olx_apartmenrs():
    """
        Insert new offers to olx table
        :return: True
    """

    sqlite_file = 'apartment_db.db'
    olx_table = 'olx_offers'
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()

    column_list = ('offer_title,'
                   + ' ' + 'offer_id,'
                   + ' ' + 'offer_price,'
                   + ' ' + 'offer_currency,'
                   + ' ' + 'offer_city,'
                   + ' ' + 'offer_district,'
                   + ' ' + 'offer_voivodeship,'
                   + ' ' + 'offer_geo_data,'
                   + ' ' + 'offer_description,'
                   + ' ' + 'offer_creator,'
                   + ' ' + 'offer_url,'
                   + ' ' + 'offer_add_time,'
                   + ' ' + 'offer_photo_links,'
                   + ' ' + 'offer_photo_count,'
                   + ' ' + 'offer_type,'
                   + ' ' + 'offer_floor,'
                   + ' ' + 'offer_rooms,'
                   + ' ' + 'offer_house_type,'
                   + ' ' + 'offer_furniture,'
                   + ' ' + 'offer_surface,'
                   + ' ' + 'offer_rent,'
                   + ' ' + 'v_date')

    parsed_urls = olx_get_category("nieruchomosci", "mieszkania", "wynajem", "Poznań")

    for offer_ in parsed_urls:

        if offer_ and BASE_URL in offer_[0]:

            cursor.execute('SELECT * FROM {table_} WHERE offer_id={param_}'. \
                           format(table_=olx_table, param_=str(offer_[1])))

            all_rows = cursor.fetchall()

            if all_rows:
                pass
            else:
                offer_temp_ = parse_offer(offer_[0])

                if offer_temp_:

                    values_text = (get_sql_values(offer_temp_.get('title', 'None'))
                                   + get_sql_values(offer_temp_.get('add_id', 'None'))
                                   + re.sub(' ', '.',get_sql_values(offer_temp_.get('price', 'None')))
                                   + get_sql_values(offer_temp_.get('currency', 'None'))
                                   + get_sql_values(offer_temp_.get('city', 'None'))
                                   + get_sql_values(offer_temp_.get('district', 'None'))
                                   + get_sql_values(offer_temp_.get('voivodeship', 'None'))
                                   + '"' + str(offer_temp_['gps'][0]) + '|' + str(
                                offer_temp_['gps'][1]) + '"' + ', '
                                   + get_sql_values(offer_temp_.get('description', 'None'))
                                   + get_sql_values(offer_temp_.get('poster_name', 'None'))
                                   + '"' + str(offer_temp_.get('url', 'None')) + '"' + ', '
                                   + get_sql_values(offer_temp_.get('date_added', 'None'))
                                   + '"' + '|'.join(offer_temp_.get('images', 'None')) + '"' + ', '
                                   + '"' + str(len(offer_temp_.get('images', []))) + '"' + ', '
                                   + get_sql_values(offer_temp_.get('private_business', 'None'))
                                   + get_sql_values(offer_temp_.get('floor', 'None'))
                                   + get_sql_values(offer_temp_.get('rooms', 'None'))
                                   + get_sql_values(offer_temp_.get('built_type', 'None'))
                                   + get_sql_values(offer_temp_.get('furniture', 'None'))
                                   + get_sql_values(offer_temp_.get('surface', 'None'))
                                   + get_sql_values(offer_temp_.get('additional_rent', 'None'))
                                   + '"' + str(date.today()) + '"'
                                   )

                    try:
                        cursor.execute("INSERT INTO {table_name} ({table_columns}) VALUES ({table_values})". \
                                       format(table_name=olx_table, table_columns=column_list, table_values=values_text))

                        connection.commit()
                    except sqlite3.IntegrityError:
                        print('ERROR: ID already exists in PRIMARY KEY column {}'.format(column_list))

    connection.close()

    return True

def get_domporta_apartments():
    """
        Insert new offers to domiporta table
        :return: True
    """

    sqlite_file = 'apartment_db.db'
    domiporta_table = 'domiporta_offers'
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()

    column_list = ('offer_market,'
                   + ' ' + 'offer_page_type,'
                   + ' ' + 'offer_web,'
                   + ' ' + 'offer_id,'
                   + ' ' + 'offer_type,'
                   + ' ' + 'offer_creator,'
                   + ' ' + 'offer_category,'
                   + ' ' + 'offer_transaction_type,'
                   + ' ' + 'offer_region,'
                   + ' ' + 'offer_city,'
                   + ' ' + 'offer_district,'
                   + ' ' + 'offer_advert_type,'
                   + ' ' + 'offer_price,'
                   + ' ' + 'offer_surface,'
                   + ' ' + 'offer_house_type,'
                   + ' ' + 'offer_house_fabric,'
                   + ' ' + 'offer_rooms,'
                   + ' ' + 'offer_floors,'
                   + ' ' + 'offer_url,'
                   + ' ' + 'offer_photo_links,'
                   + ' ' + 'offer_photo_count,'
                   + ' ' + 'v_date')

    category_data = domporta_get_category(category='mieszkanie',
                                          transaction_type='wynajme',
                                          voivodeship='Poznań'
                                          )

    for offer_ in category_data:

        cursor.execute('SELECT * FROM {table_} WHERE offer_id={param_}'. \
                       format(table_=domiporta_table, param_=str(re.sub('\\?clickSource=.*', '', offer_.split('/')[-1]))))

        all_rows = cursor.fetchall()

        if all_rows:
            pass
        else:
            offer_temp_ = domporta_get_offer(offer_)

            values_text = (get_sql_values(offer_temp_.get('market', 'None'))
                           + get_sql_values(offer_temp_.get('page_type', 'None'))
                           + get_sql_values(offer_temp_.get('web', 'None'))
                           + get_sql_values(offer_temp_.get('advert_id', 'None'))
                           + get_sql_values(offer_temp_.get('advertiser_type', 'None'))
                           + get_sql_values(offer_temp_.get('advertiser_id', 'None'))
                           + get_sql_values(offer_temp_.get('category', 'None'))
                           + get_sql_values(offer_temp_.get('transaction_type', 'None'))
                           + get_sql_values(offer_temp_.get('region', 'None'))
                           + get_sql_values(offer_temp_.get('city', 'None'))
                           + get_sql_values(offer_temp_.get('district', 'None'))
                           + get_sql_values(offer_temp_.get('advertType', 'None'))
                           + re.sub(' ', '.', get_sql_values(offer_temp_.get('price', 'None')))
                           + get_sql_values(offer_temp_.get('surface', 'None'))
                           + get_sql_values(offer_temp_.get('house_type', 'None'))
                           + get_sql_values(offer_temp_.get('house_fabric', 'None'))
                           + get_sql_values(offer_temp_.get('number_of_rooms', 'None'))
                           + get_sql_values(offer_temp_.get('number_of_floors', 'None'))
                           + '"' + str(offer_temp_.get('url', 'None')) + '"' + ', '
                           + '"' + '|'.join(offer_temp_.get('photos_url', 'None')) + '"' + ', '
                           + '"' + str(len(offer_temp_.get('photos_url', []))) + '"' + ', '
                           + '"' + str(date.today()) + '"'
                           )

            try:
                cursor.execute("INSERT INTO {table_name} ({table_columns}) VALUES ({table_values})". \
                               format(table_name=domiporta_table, table_columns=column_list, table_values=values_text))

                connection.commit()
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format(column_list))

    connection.close()

    return True

def get_new_offers():
    oto_dom_list = get_otodom_apartments()
    olx_list = get_olx_apartmenrs()
    domiporta = get_domporta_apartments()
