import sqlite3
import pandas as pd
from datetime import date


def generate_report(apartment_price=1500, v_date=str(date.today())):
    """
    Generate .html report with nice offers

    :param apartment_price: 1500
    :param v_date: '2018-12-29'
    :return: True
    """
    pd.set_option('display.max_colwidth', -1)

    sqlite_file = 'apartment_db.db'
    connection = sqlite3.connect(sqlite_file)


    otodom_select = """SELECT 
                        offer_title,
                        offer_district,
                        (offer_price+offer_rent) offer_price,
                        offer_description,
                        offer_url,
                        'oto_dom' serwis
                       from {table_1}
                       where v_date = '{date_}' and (offer_price + offer_rent) <= {price_}
                       UNION ALL
                       SELECT 
                        offer_title,
                        offer_district,
                        (offer_price+offer_rent) offer_price,
                        offer_description,
                        offer_url,
                        'olx' serwis
                       from {table_2}
                       where v_date = '{date_}' and (offer_price + offer_rent) <= {price_}
                       UNION ALL
                       SELECT 
                        offer_url,
                        offer_district,
                        offer_price,
                        'None' offer_description,
                        ('https://www.domiporta.pl' || offer_url) offer_url,
                        'domiporta' serwis
                       from {table_3}
                       where v_date = '{date_}' and (offer_price) <= {price_}
                       """ \
                    .format(table_1='otodom_offers',
                            table_2='olx_offers',
                            table_3='domiporta_offers',
                            date_=v_date,
                            price_=apartment_price)

    sql_df = pd.read_sql_query(otodom_select, connection)

    sql_df['offer_title'] = sql_df['offer_title'].apply(lambda x: x.encode('utf-8', 'ignore').decode('utf-8'))
    sql_df['offer_district'] = sql_df['offer_district'].apply(lambda x: x.encode('utf-8', 'ignore').decode('utf-8'))
    sql_df['offer_description'] = sql_df['offer_description'].apply(lambda x: x.encode('utf-8', 'ignore').decode('utf-8'))

    sql_df.to_html('apartment_report.html', render_links=True)

    return True
