import sqlite3

# name of db file
# assuming that db file is in the same catalogue as the main script
sqlite_file = 'apartment_db.db'

otodom_table = """
                CREATE TABLE otodom_offers
                (
                offer_title TEXT,
                offer_address TEXT,
                offer_creator TEXT,
                offer_type TEXT,
                offer_price DECIMAL(38,5),
                offer_currency TEXT,
                offer_city TEXT,
                offer_district TEXT,
                offer_voivodeship TEXT,
                offer_geo_data TEXT,
                offer_phone_number INTEGER,
                offer_description TEXT,
                offer_id INTEGER PRIMARY KEY,
                offer_pv INTEGER,
                offer_add_time INTEGER,
                offer_update_time INTEGER,
                offer_photo_links TEXT,
                offer_photo_count INTEGER,
                offer_video TEXT,
                offer_facebook_description TEXT,
                offer_cookie TEXT,
                offer_csrf_token TEXT,
                offer_url TEXT,
                offer_meta_id TEXT,
                offer_meta_type TEXT,
                offer_3d_link TEXT,
                offer_rent DECIMAL(38,5),
                offer_deposit DECIMAL(38,5),
                offer_house_type TEXT,
                offer_house_fabric TEXT,
                offer_windows TEXT,
                offer_heating_type TEXT,
                offer_house_condition TEXT,
                offer_available INTEGER ,
                offer_heating BOOLEAN,
                offer_balcony BOOLEAN,
                offer_kitchen BOOLEAN,
                offer_terrace BOOLEAN,
                offer_internet BOOLEAN,            
                offer_elevator BOOLEAN,
                offer_car_parking BOOLEAN,
                offer_dis_facilities BOOLEAN,
                offer_mezzanine BOOLEAN,
                offer_basement BOOLEAN,
                offer_duplex BOOLEAN,
                offer_garden BOOLEAN,
                offer_garage BOOLEAN,
                offer_cable_tv BOOLEAN,
                offer_surface DECIMAL(38,5),
                offer_rooms INTEGER ,
                offer_floor INTEGER ,
                offer_total_floors INTEGER,
                v_date TEXT
                )
            """

olx_table = """
                CREATE TABLE olx_offers
                (
                offer_title TEXT,
                offer_id INTEGER PRIMARY KEY,
                offer_price DECIMAL(38,5),
                offer_currency TEXT,
                offer_city TEXT,
                offer_district TEXT,
                offer_voivodeship TEXT,
                offer_geo_data TEXT,
                offer_description TEXT,
                offer_creator TEXT,
                offer_url TEXT,
                offer_add_time INTEGER,
                offer_photo_links TEXT,
                offer_photo_count INTEGER,
                offer_type TEXT,
                offer_floor INTEGER,
                offer_rooms INTEGER,
                offer_house_type TEXT,
                offer_furniture BOOLEAN,
                offer_surface TEXT,
                offer_rent DECIMAL(38,5),
                v_date TEXT
                )
            """

domiporta_table = """
                CREATE TABLE domiporta_offers
                (
                offer_market TEXT,
                offer_page_type TEXT,
                offer_web TEXT,
                offer_id INTEGER PRIMARY KEY,
                offer_type TEXT,
                offer_creator INTEGER,
                offer_category TEXT,
                offer_transaction_type TEXT,
                offer_region TEXT,
                offer_city TEXT,
                offer_district TEXT,
                offer_advert_type TEXT,
                offer_price DECIMAL(38,5),
                offer_surface DECIMAL(38,5),
                offer_house_type TEXT,
                offer_house_fabric TEXT,
                offer_rooms DECIMAL(38,5),
                offer_floors DECIMAL(38,5),
                offer_url TEXT,
                offer_photo_links TEXT,
                offer_photo_count INTEGER,
                v_date TEXT
                )
            """

# Connecting to the database file
connection = sqlite3.connect(sqlite_file)
cursor = connection.cursor()

# Creating tables
cursor.execute(otodom_table)
cursor.execute(olx_table)
cursor.execute(domiporta_table)

# commiting changes ans closing connection
connection.commit()
connection.close()
