import psycopg2
import os

print("test")
conn = psycopg2.connect(
	host = "localhost", 
	port = 5432, 
	dbname = "gis_tatry", 
	user = "martusia")

cur = conn.cursor()

cur.execute(
	'''drop table if exists osm_nodes;
	create temporary table osm_nodes as
	select 
		id, 
		st_transform(
			ST_GeomFromText('POINT(' || lon::numeric/10000000 || ' '|| lat::numeric/10000000 || ')',
			4326),			 
		2180) 
		geom 
	from 
		planet_osm_nodes;'''
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

with open('malopolskie.txt', 'r') as f:
	cur.copy_from(f, 'nmt_100', sep=' ')
	
conn.commit()

query = '''drop table if exists nmt_100_geom;
			create table nmt_100_geom as
			select
				ST_GeomFromText('POINT('||x||' '||y||')', 2180) as geom,	
				h
			from nmt_100;'''

cur.execute(query)

conn.commit()

cur.execute('''drop table if exists osm_nmt_hights;
			create table osm_nmt_hights as
			select			
				distinct on (n.geom) n.geom,
				n.id,
				p.h				
			from 
				osm_nodes n, 
				nmt_100_geom p
			where 
				st_dwithin(n.geom, p.geom, 100);'''
)	
			
			
cur.execute("SELECT * FROM osm_nmt_hights")
test = cur.fetchone()
print(test)

cur.close()
conn.close()

