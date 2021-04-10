.echo on
.headers on

-- Name: us-counties_recent.sql
-- Author: Charles Carter
-- Date: April 5, 2021
-- Purpose: Creates table for us_counties_recent.csv data file
-- Database: covidproj.db

drop table if exists us_counties_recent;

create table us_counties_recent (
    date text,
    county text,
    state text,
    fips integer,
    cases integer,
    deaths integer
);

.mode csv us_counties_recent
.import --skip 1 us-counties-recent.csv us_counties_recent

drop index if exists us_counties_recent_fips_idx;
create index if not exists us_counties_recent_fips_idx on us_counties_recent (fips);
drop index if exists us_counties_recent_state_idx;
create index if not exists us_counties_recent_state_idx on us_counties_recent (fips);
drop index if exists us_counties_recent_county_idx;
create index if not exists us_counties_recent_county_idx on us_counties_recent (fips);
