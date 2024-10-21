create table completa (
	list_num integer,
	artist_name varchar(5000),
	track_name varchar(5000),
	release_date integer,
	genre varchar(10),
	lyrics varchar (1000000),
	len integer,
	dating float,
	violence float,
	world_life float,
	night_time float,
	shake_the_audience float,
	family_gospel float,
	romantic float,
	communication float,
	obscene float,
	music float,
	movement_places float,
	light_visual_perceptions float,
	family_spiritual float,
	like_girls float,
	sadness float,
	feelings float,
	danceability float,
	loudness float,
	acousticness float,
	instrumentalness float,
	valence float,
	energy float,
	topic varchar (1500),
	age float
);

\COPY completa FROM 'C:\tcc_ceds_music.csv' DELIMITER ',' CSV HEADER;

select * from completa
