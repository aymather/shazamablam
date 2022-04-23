-- Init

create schema if not exists shazamablam;

-- Songs
create table if not exists shazamablam.songs (
    song_id bigserial primary key not null,
    title text,
    subtitle text,
    background text,
    song_image text,
    shazam_url text,
    explicit boolean
);

create index if not exists shazamablam_songs_idx
on shazamablam.songs(song_id, title, subtitle);

-- Artists
create table if not exists shazamablam.artists (
    artist_id bigserial primary key not null,
    name text   
);

create index if not exists shazamablam_artists_idx
on shazamablam.artists(artist_id, name);

-- City Map
create table if not exists shazamablam.city_map (
    city_id bigserial primary key not null,
    city_name text,
    state_id text
);

create index if not exists shazamablam_city_map_idx
on shazamablam.city_map(city_id);

-- Artist songs refs
create table if not exists shazamablam.artist_songs_refs (
    artist_id bigserial not null,
    foreign key (artist_id) references shazamablam.artists(artist_id),
    song_id bigserial not null,
    foreign key (song_id) references shazamablam.songs(song_id)
);

create index if not exists shazamablam_artist_songs_refs_idx
on shazamablam.artist_songs_refs(artist_id, song_id);

-- Records
create table if not exists shazamablam.records (
    song_id bigserial not null,
    foreign key (song_id) references shazamablam.songs(song_id),
    city_id bigserial not null,
    foreign key (city_id) references shazamablam.city_map(city_id),
    rank int,
    date date not null default current_date
);

create index if not exists shazamablam_records_idx
on shazamablam.records(song_id, city_id, date);