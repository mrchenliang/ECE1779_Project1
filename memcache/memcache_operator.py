"""
   @ Author: BrianQu
   @ Update_date: 2022-10-12
   @ Brief: Operator of the memcache backend
"""

import random
from flask import g
from datetime import datetime
from sys import getsizeof

import mysql.connector
from mysql.connector import errorcode

from memcache import webapp, memcache, memcache_stat, memcache_config
from backend import constants


def random_replacement():
    """
    Randomly selects a key and discards it to make space when necessary
    :return: bool
    """
    # Check if the memcache is empty
    if bool(memcache):
        # pop the random key and its value, then update the memcache_stat
        random_key = random.choice(list(memcache.keys()))
        memcache_stat['key_count'] -= 1
        memcache_stat['size_count'] -= memcache[random_key]['size']
        memcache.pop(random_key)
        return True
    else:
        print("ERROR!The memcache is EMPTY")
        return False


def lru_replacement():
    """
    Randomly selects a key and discards it to make space when necessary
    :return: bool
    """
    # Check if the memcache is empty
    if bool(memcache):
        # pop the least used key and value by its timestamp, then update the memcache_stat
        least_used_key_timestamp = min([cache['timestamp'] for cache in memcache.values()])
        for key in memcache.keys():
            if memcache[key]['timestamp'] == least_used_key_timestamp:
                memcache_stat['key_count'] -= 1
                memcache_stat['size_count'] -= memcache[key]['size']
                memcache.pop(key)
            # chen's comment, why do we need else ?
            else:
                continue
        return True
    else:
        print("ERROR!The memcache is EMPTY")
        return False


def replacement():
    """
    Using this to determine which replacement policy we will take and execute it
    :return: bool
    """
    if memcache_config['replacement_policy'] == 'Random Replacement':
        return random_replacement()
    elif memcache_config['replacement_policy'] == 'Least Recently Used':
        return lru_replacement()


def update_memcache_stat_of_statistics(existed):
    """
    Using this function to update the statistics of memcache after GET operation
    :param existed: bool
    :return: None
    """
    memcache_stat['request_count'] += 1
    if existed:
        memcache_stat['hit_count'] += 1
        memcache_stat['hit_rate'] = memcache_stat['hit_count'] / memcache_stat['request_count']
    else:
        memcache_stat['miss_count'] += 1
        memcache_stat['miss_rate'] = memcache_stat['miss_count'] / memcache_stat['request_count']


def connect_to_db():
    try:
        return mysql.connector.connect(user=constants.db_config['user'],
                                       password=constants.db_config['password'],
                                       host=constants.db_config['host'],
                                       database=constants.db_config['database'])
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("------Access Denied------")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("------Database Error------")
        else:
            print(error)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_db()
    return db


def put_into_memcache(key, file):
    """
    Set the key and value to memcache, and the value need to be encoded into Base64
    :param key: str
    :param file: str
    :return: bool
    """
    # Check memcache remains some capacity for the new value
    # Converts the image size to MB
    image_size = (getsizeof(file) - 49) / 1024 / 1024

    # Check if the image size is larger than the memcache capacity
    if image_size > memcache_config['max_capacity']:
        print("The document you have uploaded is larger than the memcache capacity")
        return False

    # Check the key is new one or existed one
    if key in memcache.keys():
        existed_file_size = memcache[key]['size']
        memcache_stat['size_count'] -= existed_file_size
    # If the size will over the capacity after put, do the replacement
    while image_size + memcache_stat['size_count'] > memcache_config['max_capacity']:
        if not bool(replacement()):
            print("The replacement process has ERROR, the memcache is EMPTY")
            return False
    # Put the value into memcache
    if key in memcache.keys():
        memcache[key]['file'] = file
        memcache[key]['size'] = image_size
        memcache[key]['timestamp'] = datetime.now()
    else:
        memcache[key] = {
            'file': file,
            'size': image_size,
            'timestamp': datetime.now()
        }
        memcache_stat['key_count'] += 1
    # Update the memcache stat
    memcache_stat['size_count'] += image_size
    return True


def get_from_memcache(key):
    """
    Using the specific key to get the value of it. If its value existed, return the base64 encoded
    value. Else return the None and print hints there is no value of this key in memcache
    :param key: str
    :return: str
    """
    # Check if the key is existed in the memcache
    if key is None:
        return None
    if key in memcache.keys():
        # Update the memcache status and return the value of the key
        memcache[key]['timestamp'] = datetime.now()
        update_memcache_stat_of_statistics(existed=True)
        return memcache[key]['file']
    else:
        # Update the memcache status
        update_memcache_stat_of_statistics(existed=False)
        return None


def clear_all_from_memcache():
    """
    Drop all the keys and values in the memcache
    :return: bool
    """
    # Drop all keys and values
    memcache.clear()
    # Update the memcache_stat
    memcache_stat['key_count'] = 0
    memcache_stat['size_count'] = 0
    print("---------Memcache is cleared---------")
    return True


def invalidate_specific_key(key):
    """
    Drop a specific key
    :param key: str
    :return: bool
    """
    if (key is not None) and (key in memcache.keys()):
        # First update the memcache status
        memcache_stat['key_count'] -= 1
        memcache_stat['size_count'] -= memcache[key]['size']
        # Then pop the corresponding key and value
        memcache.pop(key)
        print("Invalidation done")
        return True
    else:
        print("Invalidation ERROR")
        return False


def refresh_config_of_memcache():
    """
    Read memcache config details from the database and reconfigure the values
    including capacity in MB and replacement policy
    :return: bool
    """
    # Connect to the database
    cnx = get_db()
    cursor = cnx.cursor()
    # Execute the query
    query = '''SELECT * FROM cache_properties WHERE id = (SELECT MAX(id) FROM cache_properties LIMIT 1)'''
    try:
        cursor.execute(query)
        if(cursor._rowcount):
            # Get the configuration
            cache_properties = cursor.fetchone()
            max_capacity = cache_properties[1]
            replacement_policy = cache_properties[2]
            # Update the memcache_config
            memcache_config['max_capacity'] = max_capacity
            memcache_config['replacement_policy'] = replacement_policy
            return True
    except:
        print("------Get configuration failed------")
        return False


def store_statistic_into_db():
    """
    store statistics (number of items in cache, total size of items in cache,
    number of requests served, miss rate and hit rate) to database for each 5s
    :return: bool
    """
    # Get the statistics from memcache_stat
    time = datetime.now()
    size_count = memcache_stat['size_count']
    key_count = memcache_stat['key_count']
    request_count = memcache_stat['request_count']
    miss_count = memcache_stat['miss_count']
    hit_count = memcache_stat['hit_count']
    # Connect to the database
    cnx = get_db()
    cursor = cnx.cursor()
    # Execute the query
    query = "INSERT INTO cache_stats (cache_size, key_count, request_count, hit_count, miss_count, created_at)" \
            "VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (size_count, key_count, request_count, hit_count, miss_count, time))
        cursor.commit()
        print("------Memcache statistics store success------")
        return True
    except:
        print("------Memcache statistics store failed------")
        return False

