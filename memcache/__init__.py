from flask import Flask

webapp = Flask(__name__)

from flask_apscheduler import APScheduler

global memcache  # memcache
global memcache_stat  # statistic of the memcache
global memcache_config  # configuration of the memcache

memcache = {}  # memcache format:
# # {'key': {'file': encoded base64 file, 'size': file size in Byte, 'timestamp': timestamp}}
memcache_stat = {}  # memcache_stat format:
# {'key_count': total count of key in cache,
#  'size_count': total count of file size,
#  'request_count': total request count,
#  'miss_count': total miss request count,
#  'hit_count': total hit request count,
#  'miss_rate': miss request rate,
#  'hit_rate': hit request rate}
memcache_config = {}  # memcache_config format
# {'capacity': capacity of memcache in MB,
#  'replace_policy': replacement policy of memcache}

# initialize the memcache_stat
memcache_stat['key_count'] = 0
memcache_stat['size_count'] = 0
memcache_stat['request_count'] = 0
memcache_stat['miss_count'] = 0
memcache_stat['hit_count'] = 0
memcache_stat['miss_rate'] = 0
memcache_stat['hit_rate'] = 0

# initialize the memcache_config
memcache_config['capacity'] = 10
memcache_config['replace_policy'] = 'Random'

scheduler = APScheduler()
scheduler.init_app(webapp)
scheduler.start()

from memcache import main
