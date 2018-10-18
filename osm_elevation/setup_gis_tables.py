import psycopg2


def docstring():
	"""Setup GIS tables.
	
	This script sets up Digital Elevation Model data prepared in .txt file 
	('example data source is provided in readme for the whole project'). 
	Then it joins the preexisting OSM-based data with elevation data imported from the file. 
	Database connection parameters are obtained in the run-time 
	(password can (and should) be skipped if using .pgpass file). 
	"""
	
help(docstring)

host = input("host = ")
port = input("port = ")
dbname = input("db_name = ")
user = input("user = ")
password = input("password (skip while using .pgpass) = ")
print("Info about altitude file, set d = 100 and srid = 2180, if you use CODGIK data")
file_name = input("name of file with altitudes (with .txt)= ")
d = input("mesh distance = ")
srid = input("mesh coordinate system = ")



conn = psycopg2.connect(
	host = host, 
	port = port, 
	dbname = dbname, 
	user = user,
	password = password
)

cur = conn.cursor()

cur.execute(
	'''drop table if exists osm_nodes;
	create temporary table osm_nodes as
	select 
		id, 
		st_transform(
			ST_GeomFromText('POINT(' || lon::numeric/10000000 || ' '|| lat::numeric/10000000 || ')',
			4326),			 
		{}) geom 
	from 
		planet_osm_nodes;'''.format(srid)
) 
conn.commit()

cur.execute(
	'''drop table if exists nmt_100;
		create temporary table nmt_100(
		x numeric,
		y numeric,
		h numeric
	);'''
)

conn.commit()

with open(file_name, 'r') as f:
	cur.copy_from(f, 'nmt_100', sep=' ')
	
conn.commit()

query = '''drop table if exists nmt_100_geom;
			create temporary table nmt_100_geom as
			select
				ST_GeomFromText('POINT('||x||' '||y||')', {}) as geom,	
				h
			from nmt_100;'''.format(srid)

cur.execute(query)

conn.commit()

cur.execute('''create index on osm_nodes using gist(geom)''')
conn.commit()
cur.execute('''create index on nmt_100_geom using gist(geom)''')
conn.commit()

	
cur.execute('''drop table if exists osm_nmt_altitude;
			create table osm_nmt_altitude as
			select			
				distinct on (n.id) n.id,
				n.geom,
				p.h				
			from 
				osm_nodes n, 
				nmt_100_geom p
			where 
				st_dwithin(n.geom, p.geom, {})
			order by			
				n.id, st_distance(n.geom, p.geom);'''.format(d)
)	
conn.commit()			


cur.close()
conn.close()

