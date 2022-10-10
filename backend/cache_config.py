from backend.database_config import get_db

def get_cache():
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query = '''SELECT * FROM cache_properties WHERE id = (SELECT MAX(id) FROM cache_properties LIMIT 1)'''
        cursor.execute(query)
        if(cursor._rowcount):
            cache=cursor.fetchone()
            return cache
        return None
    except:
        return None

def set_cache(max_capacity, replacement_method):
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query_add = ''' INSERT INTO cache_properties (max_capacity, replacement_method) VALUES (%s,%s)'''
        cursor.execute(query_add,(max_capacity, replacement_method))
        cnx.commit()
        
        return True
    except:
        return None