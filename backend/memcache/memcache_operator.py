import random
from sys import getsizeof
from backend import webapp, memcache, memcache_stat, memcache_config


def random_replacement():
    # Check if the memcache is empty
    if bool(memcache):
        # pop the random key and its value, then update the memcache_stat
        random_key = random.choice(list(memcache.keys()))
        memcache_stat['key_count'] -= 1
        memcache_stat['size'] -= memcache[random_key]['size']
        memcache.pop(random_key)
        return True
    else:
        print("ERROR!The memcache is EMPTY")
        return False


def lru_replacement():
    # Check if the memcache is empty
    if bool(memcache):
        # pop the least used key and value by its timestamp, then update the memcache_stat
        least_used_key_timestamp = min([cache['timestamp'] for cache in memcache.values()])
        for key in memcache.keys():
            if memcache[key]['timestamp'] == least_used_key_timestamp:
                memcache_stat['key_count'] -= 1
                memcache_stat['size'] -= memcache[key]['size']
                memcache.pop(key)
            else:
                continue
        return True
    else:
        print("ERROR!The memcache is EMPTY")
        return False


def replacement():
    if memcache_config['replace_policy'] == 'Random':
        return random_replacement()
    else:
        return lru_replacement()


def put_into_memcache(key, file):
    """
    Set the key and value to memcache, and the value need to be encoded into Base64
    :param key: str
    :param file: str
    :return: None
    """
    # Check memcache remains some capacity for the new value
    # Converts the image size to MB
    image_size = (getsizeof(file) - 49) / 1024 / 1024

    # Check if the image size is larger than the memcache capacity
    if image_size > memcache_config['capacity']:
        print("The document you have uploaded is larger than the memcache capacity")
        return False

    # Check the key is new one or existed one
    if key in memcache.keys():
        existed_file_size = memcache[key]['size']
        memcache_stat['size'] -= existed_file_size
    # If the size will over the capacity after put, do the replacement
    while image_size + memcache_stat['size_count'] > memcache_config['capacity']:
        if not bool(replacement()):
            print("The replacement process has ERROR, the memcache is EMPTY")
            return False
    # Put the value into memcache

    # Update the memcache stat
