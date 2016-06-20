import psycopg2

params = {
        'dbname': 'smartcapstone',
        'user': 'postgres',
        'password': 'postgres',
        'host': '128.199.91.96',
        'port': 5432,
        'sslmode': 'require'
    }

def register(user_email):
	if (user_email):
	    conn = psycopg2.connect(**params)
	    cur = conn.cursor()
	    cur.execute("SELECT fms_id FROM AppUser WHERE email='"+user_email+"'")
	    return cur.fetchone()

def add_node(node):
    # print 'Adding node to database'
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    select_string = "SELECT id FROM Node WHERE lat=%s AND lng=%s;"
    cur.execute(select_string, [node['lat'], node['lon']])
    if not cur.rowcount:
        insert_string = "INSERT INTO Node (lat, lng, name) VALUES ("+node['lat']+","+node['lon']+",'"+node['name']+"');"
        # print insert_string
        cur.execute(insert_string, [node['lat'], node['lon'], node['name']])
        print 'row inserted'
        cur.close()
        conn.commit()
    conn.close()     

def check_route_exists():
    pass


# print register('tanhq646@gmail.com')
# print register('lol')
